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

date_sum = []
money_sum = []
number_sum = []
region_sum = []

pages = 5

for i in range(pages):
    
    html = driver.page_source
    soup = bs(html, 'lxml')
    
#==============================================================================
#     date = [j.text.strip() for j in soup.find_all(attrs = {'class':'tc'}) if '/' in j.text]
#     money = [j.text.strip() for j in soup.find_all(attrs = {'class':'tr'}) if '원' in j.text]
#     money = [int(i.replace('원','').replace(',','')) for i in money]
#     number = [j.text.strip() for j in soup.find_all(name = 'a', attrs = {'href' : '#'})][1:]
#     region = [j.text.strip() for j in soup.find_all(attrs = {'class':'tl'})][1::2]
#     click = [j.text.strip() for j in soup.find_all(attrs = {'class':'default'}) if '더보기' in j.text]
#==============================================================================
    
    # date를 원하는 곳까지 필터 못하겠습니다....
    for j in range(len(date)):
        
            date = [j.text.strip() for j in soup.find_all(attrs = {'class':'tc'}) if '/' in j.text]
            money = [j.text.strip() for j in soup.find_all(attrs = {'class':'tr'}) if '원' in j.text]
            money = [int(i.replace('원','').replace(',','')) for i in money]
            number = [j.text.strip() for j in soup.find_all(name = 'a', attrs = {'href' : '#'})][1:]
            region = [j.text.strip() for j in soup.find_all(attrs = {'class':'tl'})][1::2]
            click = [j.text.strip() for j in soup.find_all(attrs = {'class':'default'}) if '더보기' in j.text]
            
            if date[j] == '2017/07/21':
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


                    


