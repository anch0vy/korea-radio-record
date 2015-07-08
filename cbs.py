# coding=utf-8
import urllib2
from tendo import singleton
from radio_util import RADIO

me = singleton.SingleInstance()
IPHONE_USER_AGENT = 'AppleCoreMedia/1.0.0.12B435 (iPhone; U; CPU OS 8_1_1 like Mac OS X; ko_kr)'
radio = RADIO('/radio/cbs')
radio.mediaDownLoop('http://101.79.254.171/cbs939/_definst_/cbs939.stream/playlist.m3u8',IPHONE_USER_AGENT)