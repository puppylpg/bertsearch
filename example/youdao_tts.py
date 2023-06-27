
# -*- coding: utf-8 -*-
import sys
import uuid
import requests
import hashlib
import time
from imp import reload


reload(sys)

YOUDAO_URL = 'https://openapi.youdao.com/ttsapi'
APP_KEY = '194b9ddcf96a4b94'
APP_SECRET = 'rGkCngBC45uVYLRozcAfVav4SVKm7XdN'


def encrypt(signStr):
    hash_algorithm = hashlib.md5()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def connect():
    q = """
        Uuhhh... hello world
        Uuummmmmmmmmmm... hello world
    """

    data = {}
    # data['langType'] = 'zh-CHS'
    salt = str(uuid.uuid1())
    signStr = APP_KEY + q + salt + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['q'] = q
    data['salt'] = salt
    data['sign'] = sign
    data['voice'] = 6
    # data['voiceName'] = 'youxiaoqin'
    data['voiceName'] = 'youxiaomei'
    # data['voiceName'] = 'weixiaomei'
    # 真人
    # data['voiceName'] = 'youyingying'
    data['speed'] = 1.0

    response = do_request(data)
    contentType = response.headers['Content-Type']
    if contentType == "audio/mp3":
        millis = int(round(time.time() * 1000))
        filePath = str(millis) + ".mp3"
        fo = open(filePath, 'wb')
        fo.write(response.content)
        fo.close()
    else:
        print(response.content)


if __name__ == '__main__':
    connect()