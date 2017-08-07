# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 18:13:33 2017

@author: hslee3
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

pages = 1

for i in range(pages):
    
    html = driver.page_source
    soup = bs(html, 'lxml')
    
    date = [j.text.strip() for j in soup.find_all(attrs = {'class':'tc'}) if '/' in j.text]
    money = [j.text.strip() for j in soup.find_all(attrs = {'class':'tr'}) if '원' in j.text]
    money = [int(i.replace('원','').replace(',','')) for i in money]
    number = [j.text.strip() for j in soup.find_all(name = 'a', attrs = {'href' : '#'})][1:]
    region = [j.text.strip() for j in soup.find_all(attrs = {'class':'tl'})][1::2]
    click = [j.text.strip() for j in soup.find_all(attrs = {'class':'default'}) if '더보기' in j.text]
    # 'click' 버튼을 추가 : 이유는 밑에 설명
    
    # 우선 적으로 날짜 길이에 한해서 'J'를 2억 이상으로 제한
    for l in range(len(date)):
        
        if money[j] >= 2e8:
            # 다 클릭하는 것이 좋을 것으로 판단
            # 1) 시간이 그리 오래 걸리지 않고, 2) 실제로도 그렇게 하며, 3) 정확도를 높이는 방법
            driver.find_element_by_link_text(number[j]).click()
            # 확인하는 방법은 우선적으로 패스
            
            for k in range(len(date)):
                
                # 8일 전의 날짜가 첫 30페이지에 있었는지 확인
                # 있다면, 위에 걸렀던 정보들 중에 날짜 내에 있는 것들만 확인
                # 여기서 질문!!!
                # 위에 money[j]로 인해 number[j]가 필터가 가능하잖아?
                # 그러면 밑에 date[k]로 date를 필터하고,
                # j와 k의 공통점만 필터하고 싶으면 어떻게 해야함?
                # (그러면 원하는 값을 뽑는게 맞다고 생각함 아니면 말해주삼! ㄳㄳ)
                if week_day_ago in date[k]:
                    
                    # 원하는 날짜가 안에 있다면 전체 for문을 break!
                    break
                    

                # 아니면, '더보기' 클릭
                # '더보기'의 xpath가 페이지 마다 다름을 확인
                # //*[@id="pagination"]/a
                # //*[@id="pagination"]/a[3]
                # //*[@id="pagination"]/a[4]
                # 따라서 link)_text로 'click' 텍스트 클릭하도록 함
                else:
                    driver.find_element_by_link_text(click).click()


                    


