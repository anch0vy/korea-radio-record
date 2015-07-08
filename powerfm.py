# coding=utf-8
import urllib2
import re
from tendo import singleton
from Crypto.Cipher import DES
from radio_util import RADIO

me = singleton.SingleInstance()
IPHONE_USER_AGENT = 'AppleCoreMedia/1.0.0.12B435 (iPhone; U; CPU OS 8_1_1 like Mac OS X; ko_kr)'
radio = RADIO('/radio/powerfm')
encdata = radio.urlopenWithUseragent('http://gorealra.sbs.co.kr/g4/protocol/GetStream.jsp?pmDevice=ios&pmNetwork=wifi&pmChannel=RA02&pmAppver=4.5.0&from=iphone','Gorealra/4.5.4 CFNetwork/711.1.16 Darwin/14.0.0')
des = DES.new(KEY[:8], DES.MODE_ECB)
playlistUrl = des.decrypt(encdata.decode('base64'))
playlistUrl = re.sub('[\x01-\x08]','',playlistUrl)
radio.mediaDownLoop(playlistUrl,IPHONE_USER_AGENT)