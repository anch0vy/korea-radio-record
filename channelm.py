# coding=utf-8
import urllib2
from tendo import singleton
from radio_util import RADIO

me = singleton.SingleInstance()
IPHONE_USER_AGENT = 'AppleCoreMedia/1.0.0.12B435 (iPhone; U; CPU OS 8_1_1 like Mac OS X; ko_kr)'
radio = RADIO('/radio/channelm')
url = radio.urlopenWithUseragent('http://miniplay.imbc.com/AACLiveUrl.ashx?channel=chm&type=iphone&agent=iphone&protocol=M3U8','iphone')
radio.mediaDownLoop(url,IPHONE_USER_AGENT)