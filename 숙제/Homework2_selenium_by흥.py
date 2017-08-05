# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 18:13:33 2017

@author: hslee3
"""

from selenium import webdriver as wb
from bs4 import BeautifulSoup as bs
import pandas as pd
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

for i in range(1,2):
    
    html = driver.page_source
    soup = bs(html, 'lxml')
    
    date = [j.text.strip() for j in soup.find_all(attrs = {'class':'tc'}) if '/' in j.text]
    money = [j.text.strip() for j in soup.find_all(attrs = {'class':'tr'}) if '원' in j.text]
    number = soup.find_all(name = 'a', attrs = {'href' : '#'})
    number = number[1:]
    region = [j.text.strip() for j in soup.find_all(attrs = {'class':'tl'})]
    region = region[1::2]
    
    for k in range(0,30):
        money[k] = money[k].replace('원','')
    
    date_sum += date
    money_sum += money
    number_sum += number
    region_sum += region
    
    result = pd.DataFrame(data = [number_sum, region_sum, money_sum, date_sum],
                          index = ['접수번호', '발주기관', '금액', '일자']).T   
    
    if week_day_ago in date_sum:
        
#==============================================================================
#         result = result[result['발주기관'].str.contains(r'대전|충청|충북|충남|세종')]    
#==============================================================================
        result = result[result['금액'].values >= 200,000,000]
        
        
        
        break
    
    else:
        driver.find_element_by_xpath('//*[@id="pagination"]/a').click()
        



