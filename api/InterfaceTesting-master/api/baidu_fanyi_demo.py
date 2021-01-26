# /usr/bin/env python
# coding=utf8

import httplib2
import hashlib
import urllib
import random
from urllib.parse import quote

appid = ''  # 你的appid
secretKey = ''  # 你的密钥

httpClient = None
myurl = '/api/trans/vip/translate'
q = 'apple'
fromLang = 'en'
toLang = 'zh'
salt = random.randint(32768, 65536)

sign = appid + q + str(salt) + secretKey
m1 = hashlib.md5()
# m1.update(sign)
m1 = hashlib.md5(sign.encode(encoding='UTF-8'))
sign = m1.hexdigest()
myurl = myurl + '?appid=' + appid + '&q=' + quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
    salt) + '&sign=' + sign

try:
    httpClient = httplib2.HTTPConnection('api.fanyi.baidu.com')
    httpClient.request('GET', myurl)

    # response是HTTPResponse对象
    response = httpClient.getresponse()
    print(response.read())
except Exception as e:
    print(e)
finally:
    if httpClient:
        httpClient.close()
