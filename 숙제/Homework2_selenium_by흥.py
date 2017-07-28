# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 18:13:33 2017

@author: hslee3
"""

from selenium import webdriver as wb
from bs4 import BeautifulSoup as bs

driver = wb.Chrome('C:/Users/Wade/Desktop/6_python 숙제 자료_170726/chromedriver.exe')
driver.implicitly_wait(2)

#%%
#조달청계약요청
url1 = "http://www.g2b.go.kr:8091/cm/contstus/fwdPpsItemContractReqStus.do"

driver.get(url1)

driver.find_element_by_xpath('//*[@id="prodNm"]').send_keys('전반')
driver.find_element_by_xpath('//*[@id="srchFrm"]/div[2]/div/a[1]/span').click()

for i in range(1,31):
    driver.find_element_by_xpath('//*[@id="resultFrm"]/table/tbody/tr[{}]/td[1]/a'.format(i)).click()
    
    html = driver.page_source
    soup = bs(html, 'lxml')
    
    data1 = soup.
    
    
    
    