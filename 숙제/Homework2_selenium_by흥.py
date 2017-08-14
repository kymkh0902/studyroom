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

## 최종적으로 확인할 리스트들 지정
date_sum = []
money_sum = []
number_sum = []
region_sum = []

##지역 패턴을 만들어 준다
pattern = re.compile(r'대전|충청|충북|충남|세종')
### re.search(pattern, 지역명) # 해당 지역이 있으면 True, 없으면 False로 뜰 것이다.

## 총 5개의 페이지(최대)로 설정
pages = 5

## 최대 5개의 페이로 지정한 부분을 for문으로 돌림
## 물론 전체 페이지를 돌리지 않고, 일정 조건에 부합하면 break 할 예정
for i in range(pages):
    
    ## 소스를 가져와 soup으로 정리
    html = driver.page_source
    soup = bs(html, 'lxml')
    
    ## '클릭' 포함하여 총 6개의 원하는 '일회성' 정보를 가져옴
    ## 추가적으로 date 라는 리스트를 생성하여, 원하는 날짜까지의 정보만 필터
    ## ex) date_tem이 30개라도 date는 원하는 날짜에 멈추므로 17개가 되면, 그 17개에 한해서
    ## 2억 또는 그 외 다른 조건들을 탐색
    date_tem = [j.text.strip() for j in soup.find_all(attrs = {'class':'tc'}) if '/' in j.text]
    money = [j.text.strip() for j in soup.find_all(attrs = {'class':'tr'}) if '원' in j.text]
    money = [int(i.replace('원','').replace(',','')) for i in money]
    number = [j.text.strip() for j in soup.find_all(name = 'a', attrs = {'href' : '#'})][1:]
    region = [j.text.strip() for j in soup.find_all(attrs = {'class':'tl'})][1::2]
    click = [j.text.strip() for j in soup.find_all(attrs = {'class':'default'}) if '더보기' in j.text]
    date = [] 
    
    ## for 문을 통해서 1페이지씩 멈추고 싶은 날짜가 있는지 확인
    ## 확인하여, 원하는 날짜까지만의 정보를 다시 가져올 예정
    ## 기존의 date를 date_tem으로 바꾸고, 다시 date라는 List 생성
    ## date라는 리스트에 원하는 조건까지만 추가!
#==============================================================================
#     for k in range(len(date_tem)):
#         
#         if date_tem[k] == '2017/07/19':
#             break
#         date.append(date_tem[k])
#==============================================================================
    
    ## 조건을 하나로 합쳐본다 : 날짜가 원하는 날짜가 안나오고, 금액이 1억이 넘으면 클릭
    ## 클릭해서 원하는 지역의 조건이 맞는지 확인해본다(매번 클릭할 때마다 html 새로 지정)
    for k in range(len(date_tem)):
        
        if date_tem[k] != '2017/07/19' and money[k] >= 1e8:
            
            driver.find_element_by_link_text(number[k]).click()
            html = driver.page_source
            soup = bs(html, 'lxml')
            
            ## 첫번째로 '납품장소'를 확인한다
            ## 지역이름이 들어갔는지 확인한다
            ## 우선 if문으로 re 함수를 쓸 수 있는 방법이 안떠올라, 각각 or로 입력한다.
            ## 'class'가 'tl'일 때 가장 첫번 째 나오는 값이 '납품장소'의 값이므로 아래와 같이 입력한다
            if '대전'or'충청'or'충북'or'충남'or'세종' in soup.find(attrs = {'class':'tl'}).text.strip():
                
            ## 그다음 두번째로는 '공사명'을 확인한다
            ## 이 또한 지역이름이 들어갔는지 확인한다
            ## '공사명'의 값은 colspan:5 인 유일한 값이므로 아래와 같이 입력한다
            else if '대전'or'충청'or'충북'or'충남'or'세종' in soup.find(attrs = {'colspan':'5'}).text.strip():
            
            ## 마지막으로 '발주(공고)기관'의 전화번호를 확인한다
            
            else if 
                
                
        else if date_tem[k] == '2017/07/19':
            break
    
    ## '클릭(+더보기)' 버튼을 누름
    ## 단, 클릭 버튼이 없으면 error가 뜨기 때문에(page 수를 최대 5로 지정했으나, 그보다 적을 경우)
    ## 클릭 버튼이 없을 경우 break를 할 수 있는 조건문 생성
    if click != []:
        driver.find_element_by_link_text(click[0]).click()
    else:
        break


            
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


                    


