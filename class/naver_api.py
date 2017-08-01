# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 17:21:15 2017

@author: Whi Kwon
"""

import os
import sys
import urllib.request
import json

# API id,pwd
client_id = "oQdFeij_A5u21Iieg3vD"
client_secret = "reAn5vCotJ"

# 검색 text
encText = urllib.parse.quote("예술의전당")
# url 요청
url = "https://openapi.naver.com/v1/search/local?query={}&display=5".format(encText) # json 결과
# request와 동일
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()

#json 형식으로 받아온 데이터 변수에 저장
if(rescode==200):
    response_body = response.read()
    data = response_body.decode('utf-8')
else:
    print("Error Code:" + rescode)

# 우리는 items만 잇으면 됨. 
j = json.loads(data)['items']
result = []

# 지역 확인. 
for i in range(len(j)):
    if '서울' in j[i]['address']:
        result.append((j[i]['title'],j[i]['address']))

    
