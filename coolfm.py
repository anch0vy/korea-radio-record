# coding=utf-8
import urllib2
import json
from urlparse import urljoin
from tendo import singleton
from radio_util import RADIO

me = singleton.SingleInstance()
IPHONE_USER_AGENT = 'AppleCoreMedia/1.0.0.12B435 (iPhone; U; CPU OS 8_1_1 like Mac OS X; ko_kr)'
radio = RADIO('/radio/coolfm')
req = urllib2.Request('http://kongapi.kbs.co.kr/api/kp_cms/live_stream','beta=0&is_bora=N&device_type=iphone&welcome=1_1985_1_1_0_1&channel_code=25')
req.add_header('User-Agent','Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12B435 mobile/iPhone OS/iPhone/iPhone6,1/8.1.1/KBS kong/1.0.8')
js = json.load(urllib2.urlopen(req))
m3 = radio.getM3U8withUseragent(js['real_service_url'],IPHONE_USER_AGENT)
infoUrl = urljoin(m3.base_uri,m3.data['playlists'][0]['uri'])
radio.mediaDownLoop(None,IPHONE_USER_AGENT,infoUrl = infoUrl)