# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 17:21:15 2017

@author: Whi Kwon
"""

import urllib.request
import json

# API id,pwd
client_id = "oQdFeij_A5u21Iieg3vD"
client_secret = "reAn5vCotJ"

# 검색 text

def searchCompany(company):
    '''
    naver 검색에서 회사 찾는 함수
    
    ----parameters----
    company : 회사명
    pattern : 찾고자 하는 패턴(주소)
    '''
    # url 요청
    encText = urllib.parse.quote(company)
    url = "https://openapi.naver.com/v1/search/local?query={}&display=10".format(encText) # json 결과
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
    address = []
    company_nm = []
    
    # 지역 확인. 
    for i in range(len(j)):
        company_nm.append(j[i]['title'])
        address.append(j[i]['address'])
    return company_nm, address
        
