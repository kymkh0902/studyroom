# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 20:35:31 2017

@author: Whi Kwon
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

# Selenium으로 해보기
url1 = 'http://www.g2b.go.kr:8091/cm/contstus/fwdPpsItemContractReqStus.do'
url2 = 'http://www.g2b.go.kr:8101/ep/tbid/tbidFwd.do?bidSearchType=2&taskClCds=1'
url3 = 'http://www.g2b.go.kr:8101/ep/tbid/tbidFwd.do?bidSearchType=1&taskClCds=1'

driver = webdriver.Chrome('C:/Users/Whi Kwon/Documents/GitHub/python_script/chromedriver.exe')
#url1은 다른 형식 
driver.get(url1)
driver.implicitly_wait(2)
driver.find_element_by_xpath('//*[@id="prodNm"]').send_keys('전반')
driver.find_element_by_xpath('//*[@id="srchFrm"]/div[2]/div/a[1]/span').click()
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')

list1 = [i.text.strip() for i in soup.find_all(attrs = {'class':'tc'})]
list2 = [i.text.strip() for i in soup.find_all(attrs = {'class':'tl'})]
list3 = [i.text.strip() for i in soup.find_all(attrs = {'class':'tr'})]
total = list1[::3] + list1[1::3] + list1[2::3] + list2[::2] + list2[1::2] + list3 
total = pd.DataFrame(data = [total[i*len(list3):(i+1)*len(list3)] for i in range(6)], 
                     index = ['접수번호','품명','발주(공고)기관','예정금액','접수일자','요청구분']).T
try:
    driver.find_element_by_xpath('//*[@id="pagination"]/a').click()
except:
    pass

#%% 
#url2, url3은 같은 형식
driver.get(url3)
driver.find_element_by_xpath('//*[@id="bidNm"]').send_keys('전반')
driver.find_element_by_xpath('//*[@id="buttonwrap"]/div/a[1]/span').click()

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
total = [i.text.strip() for i in soup.find_all('td')]
total = pd.DataFrame(data = [total[i::10] for i in range(10)], 
                     index = ['업무','공고번호,차수','분류','공고명','공고기관','수요기관',
                              '계약방법','입력일시(입찰마감일시)','공동수급','투찰']).T

    
                     
                     