# coding=utf-8
import os
import time
import shutil
from glob import glob
from subprocess import call
from radio_util import checkAndMakeDir
dirs = ['1radio','cbs','channelm','coolfm','happyfm','lovefm','mbcfm4u','mbcradio','powerfm']

def convert(dir,inputList,outputName,delete=False):
	ret = call(['ffmpeg','-loglevel','warning','-y','-i','concat:%s'%('|'.join(inputList)),'-codec','copy',os.path.join(dir,outputName)])
	if ret==0 and delete:
		for fileName in inputList:
			os.remove(fileName)
		return True
	return False

def splitByTime(l,basedir):
	if len(l)==0:
		return
	findTimestamp = lambda x:int(x.split('/')[-1].split('__time__')[0])
	timeStamps = map(findTimestamp,l)
	start = timeStamps[0] - timeStamps[0]%3600
	end = timeStamps[0] - timeStamps[0]%3600 + 3600
	if time.time() < end:
		return 
	timeString = time.strftime('%y-%m-%d_%H',time.localtime(start)) + time.strftime('%H',time.localtime(end))
	dateDir = os.path.join(basedir,'raw',timeString)
	checkAndMakeDir(dateDir)
	fileList = [x.split('/')[-1] for x in l if start<=findTimestamp(x)<=end]
	for file in fileList:
		try:
			shutil.move(os.path.join(dateDir,'..',file),os.path.join(dateDir,file))
		except IOError:
			pass
	return 


def selectAndConvert(basedir):
	dirList = [x for x in glob(os.path.join(basedir,'raw','*')) if os.path.isdir(x)]
	for x in dirList:
		inputList = glob(os.path.join(x,'*__time__*.*'))
		inputList.sort()
		dir = os.path.join(x,'..','..')
		dir = os.path.normpath(dir)
		outputName = x.split('/')[-1]+ '.' + inputList[0].split('.')[-1]
		print dir,outputName
		if convert(dir,inputList,outputName,delete=True) == True:
			os.rmdir(os.path.dirname(inputList[0]))


if __name__ == '__main__':
	for basedir in dirs:
		dir = os.path.join('/radio',basedir,'raw/*__time__*.*')
		basedir = os.path.join('/radio',basedir)
		g = glob(dir)
		g.sort()
		for x in range(24):
			splitByTime(g,basedir)
		selectAndConvert(basedir)