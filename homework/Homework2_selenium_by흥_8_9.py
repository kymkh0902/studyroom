# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 21:03:36 2017

@author: HS
"""

from selenium import webdriver as wb
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
import datetime

driver = wb.Chrome('C:/Users/HS/Desktop/과외/studyroom/chromedriver.exe')
driver.implicitly_wait(2)

today = datetime.date.today()
week_ago = today - datetime.timedelta(7)
week_day_ago = today - datetime.timedelta(8)
today = today.strftime('%Y/%m/%d')
week_ago = week_ago.strftime('%Y/%m/%d')
week_day_ago = week_day_ago.strftime('%Y/%m/%d')

#%%
#조달청계약요청
driver.get("http://www.g2b.go.kr:8091/cm/contstus/fwdPpsItemContractReqStus.do")
driver.find_element_by_xpath('//*[@id="prodNm"]').send_keys('전반')
driver.find_element_by_xpath('//*[@id="srchFrm"]/div[2]/div/a[1]/span').click()

### 최종 결과 받을 변수들
date_sum = []
money_sum = []
number_sum = []
region_sum = []

### 넘길 페이지 지정
pages = 1

### page수 지정해서 불러오기 (충분히 많이)
for i in range(pages): ### 돌아가는 지 확인을 위해 pages = 1로 지정
    ### page source 가져오기    
    html = driver.page_source
    soup = bs(html, 'lxml')

    ### page source로부터 원하는 정보 가져오기        
    date = [j.text.strip() for j in soup.find_all(attrs = {'class':'tc'}) if '/' in j.text]
    money = [j.text.strip() for j in soup.find_all(attrs = {'class':'tr'}) if '원' in j.text]
    money = [int(i.replace('원','').replace(',','')) for i in money]
    number = [j.text.strip() for j in soup.find_all(name = 'a', attrs = {'href' : '#'})][1:]
    region = [j.text.strip() for j in soup.find_all(attrs = {'class':'tl'})][1::2]
    click = [j.text.strip() for j in soup.find_all(attrs = {'class':'default'}) if '더보기' in j.text]

    ### 데이터 가진거에 대해서 개수만큼 순차적으로 확인.
    for j in range(len(date)):
        ### date 조건 걸어서 부합하면 for문 break하기.
        ### 코드가 실행되는 지 확인하는 방법은 중간 결과를 출력해보는 거 밖에 없다. 
        ### 아래 예시로 들면 원래 변수가 들어가야 할 자리에 '2017/08/01' 값을 입력해보고
        ### 날짜가 충족했을 때 'BREAK' 과 함께 for문을 break하도록, 외에는 날짜를 출력하도록 해보면
        ### 정상적으로 작동하는 것을 확인할 수 있다. 
        if date[j] == '2017/08/01':
            print('BREAK')
            break
        print(date[j])
        
        ### 아래 xpath 같아서 생긴 문제점 해결 방안 
        ##########################################################################################
        ### find.element_by_css_selector로 확인하면 됨. 
        ### 각 항목에 해당되는 selector는 아래와 같음.
        # container > div.detail > table:nth-child(1) > tbody > tr:nth-child(2) > td.tl
        # container > div.detail > table:nth-child(1) > tbody > tr:nth-child(3) > td:nth-child(2)
        # container > div.detail > table:nth-child(1) > tbody > tr:nth-child(4) > td
        ##########################################################################################
        
        ### 지역 맞는지 확인 방법 
        ##########################################################################################
        ### pattern = re.compile(r'대전|충청|충북|충남|세종')  # 지역 확인 패턴을 만들어준다. 
        ### re.search(pattern, 지역명) # 해당 지역이 있으면 True, 없으면 False로 뜰 것이다. 
        ### 예시) 
        ### if re.search(pattern, '대전'):
        ###     ...추가 코드 ... 
        
        ##########################################################################################
        ### 전화번호는 in으로 확인하자.
        ### 네이버지도 api 사용은 naver_api.py 파일 내 함수를 참조하자. 
        ##########################################################################################
        
        ### 리스트 만들기
        ##########################################################################################
        ### 일단 조건대로 거른 결과가 있어야 함. 우리는 지금 list만 사용하고 있으니 데이터 형식은 list
        ### list는 python내에서는 괜찮지만 밖에 가지고 나가서 보기엔 불편하니 pandas dataframe으로
        ### 바꿔준 후에 excel로 내보내서 보면 될 듯.
        ### 이 작업은 excel을 만드는게 포함되므로 코드가 느려짐. 그래서 중간에 logic이 맞는지 확인할 
        ### 때에는 list로 작업해도 불편하지 않으니 검증이 끝난 후에 추가하면 될듯. 
        ##########################################################################################
        
        ### 검증
        ##########################################################################################
        ### 아주 세세하게 기존에 확인하는 logic 그대로 확인하기 위해서 컴퓨터가 중간에 확인하는 사항이
        ### 제대로 되고 있는지 체크해야 한다.
        ### 1) 결과가 맞는지 확인해야 하고 
        ### 2) 조건에 의해 탈락된 장소들은 왜 그런지 확인을 해야 한다.
        ### 3) 특정 조건이 애매하다고 생각되면 조건문 사이에 빈 list를 넣어서 빠지는 것들의 정보를 다 넣은 후에 
        ###    어떤 정보들이 빠지는 지 확인하면 되고 
        ### 4) 그렇지 않다고 하면 통과된 / 걸러진 정보를 모두 모아서 기존 사람의 방식과 동일한 
        ###    logic대로 되었는 지를 확인하면 된다. 
        
'''
    우선 if문으로 지정한 날짜가 맞으면 멈춤!
    if date[j] == week_day_ago:
        break
    
    금액이 2억이 넘으면 클릭한다!
    저번 숙제에 쓴대로 우선 2억이 넘으면 모두 클릭할 예정
    if money[j] == 2e8:
        driver.find_element_by_link_text(number[j]).click()
        
        3가지 순서대로 지역에 맞는지 확인
        납품장소 - 공사명 - 발주(공고)기관
        또한, 각 공고 내의 위 사항들은 모두 같은 xpath를 가짐을 확인

        if 납품장소 == "대전~~~":
            필요한 항목들을 끌고옴
            
        else if 공사명 == "대전~~~~":
            필요한 항목들을 끌고옴
            
        else if 발주(공고)기관 == "041", "042", "043", "044":
            필요한 항목들을 끌고옴
            
        else if 발주(공고)기관을 '네이버지도'에 검색하여 상위 3개를 확인하여 "대전~~~"이 있으면:
            필요한 항목들을 끌고옴
            
        else:
            2억 이상의 리스트를 확인할 수 있도록 엑셀로 만들어서 확인
            이건 그때 그때 마다 보고 지울 생각.
            또한, 원하는 지역이 아니었던 발주(공고)기관들은 리스트로 만들어서
            추후에 네이버 지도에 검색하는 것보다 우선적으로 리스트를 확인할 수 있도록 만들고 싶음
    
    내가 원하는 결론은
    1) 필요한 항목들을 엑셀로 만들어서 보는 것
    2) 내가 걸러낸 항목(2억 이하)에 대해서 맞는지 확인
       -> 그래서 납품장소, 공사명도 가져와야 되는지 의문..
    3) 내가 걸러낸 발주(공고)기관들은 계속 데이터로 가지고 있을 예정 '''


                    


