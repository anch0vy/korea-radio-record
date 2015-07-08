# coding=utf-8
import urllib2
import m3u8
import os
import shutil
import smtplib
import time
import traceback
import sys
import subprocess
import errno
import signal
import inspect
from glob import glob
from retrying import retry
from urlparse import urlparse,urljoin
from functools import wraps
class TimeoutError(Exception):
	pass

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
	def decorator(func):
		def _handle_timeout(signum, frame):
			raise TimeoutError(error_message)
		def wrapper(*args, **kwargs):
			signal.signal(signal.SIGALRM, _handle_timeout)
			signal.alarm(seconds)
			try:
				result = func(*args, **kwargs)
			finally:
				signal.alarm(0)
			return result
		return wraps(func)(wrapper)
	return decorator


def checkAndMakeDir(path):
	if not os.path.exists(path):
		os.makedirs(path)


class RADIO:
	def __init__(self,PATH):
		curFrame = inspect.currentframe()
		q = inspect.getouterframes(curFrame)
		self.callerPath = os.path.abspath(inspect.getfile(q[1][0]))
		del q
		del curFrame
		checkAndMakeDir(os.path.join(PATH))
		checkAndMakeDir(os.path.join(PATH,'raw'))
		self.PATH = PATH
		self.rawPath = os.path.join(self.PATH,'raw')
		checkAndMakeDir(self.rawPath)

	def getInfoUrl(self,url,useragent):
		m3 = self.getM3U8withUseragent(url,useragent)
		infoUrl = urljoin(m3.base_uri,m3.data['playlists'][0]['uri'])
		return infoUrl

	def mediaDownLoop(self,url,useragent,useragentForInfoUrl=None,infoUrl=None):
		if useragentForInfoUrl==None:
			useragentForInfoUrl = useragent
		if infoUrl is None:
			infoUrl = self.getInfoUrl(url,useragentForInfoUrl)
		while True:
			m3 = self.getM3U8withUseragent(infoUrl,useragent)
			media_seq = m3.media_sequence -1
			for mediaName in m3.files:
				media_seq+=1
				if checkSameMediaSeq(media_seq,self.rawPath):
					continue
				fileName = '%d__time__%d.%s'%(time.time(),media_seq,mediaName.split('?')[0].split('.')[-1])
				try:
					self.urlopenWithUseragent(urljoin(infoUrl,mediaName) , useragent , save = os.path.join(self.rawPath,fileName))
				except:
					global me
					try:
						del me
					except:
						pass
					cmd = [sys.executable, self.callerPath]
					try:
						subprocess.Popen(cmd)
					except:
						errortext = '[error][shutdown]%r'%cmd
						self.exceptLog(sys.exc_info(),errortext)
					finally:
						exit()
				else:
					print '[debug]save %s'%fileName
			time.sleep(5)

	@timeout(5)
	def urlopenWithUseragent(self,url,useragent,save=None):
		req = urllib2.Request(url)
		req.add_header('User-Agent',useragent)
		if save:
			load = urllib2.urlopen(req)
			loads = load.read()
			if len(loads)==0:
				raise Exception
			with open(save,'wb') as fsave:
				fsave.write(loads)
			return True
		else:
			return urllib2.urlopen(req).read()

	def getM3U8withUseragent(self,url,useragent):
		read = self.urlopenWithUseragent(url,useragent)
		m3 = m3u8.loads(read)
		m3.base_uri = url
		return m3

	def exceptLog(self,(exc_type, exc_value, exc_traceback),text):
		errorpath = os.path.join(self.PATH,'../error')
		checkAndMakeDir(errorpath)
		with open('%s/%s_%d'%(errorpath,self.PATH.split('/')[-1],time.time()) , 'a') as ferror:
			ferror.write(text)
			ferror.write('\n')
			ferror.write(str(exc_type))
			ferror.write('\n')
			ferror.write(str(exc_value))
			ferror.write('\n')
			traceback.print_tb(exc_traceback,file = ferror)

def checkSameMediaSeq(seq,savePath):
	for fileName in glob('%s/*__time__%d.*'%(savePath,seq)):
		timestamp = int(fileName.split('/')[-1].split('__time__')[0])
		if timestamp+300 > time.time():
			return True
	return False
