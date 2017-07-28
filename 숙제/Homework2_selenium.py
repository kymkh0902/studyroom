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

list1_sum = []
list2_sum = []
list3_sum = []

driver = webdriver.Chrome('C:/Users/Wade/Desktop/6_python 숙제 자료_170726/chromedriver.exe')
driver.get(url1)
driver.implicitly_wait(2)
driver.find_element_by_xpath('//*[@id="prodNm"]').send_keys('전반')
driver.find_element_by_xpath('//*[@id="srchFrm"]/div[2]/div/a[1]/span').click()

for i in range(0,10):    
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    
    list1 = [i.text.strip() for i in soup.find_all(attrs = {'class':'tc'})]
    list2 = [i.text.strip() for i in soup.find_all(attrs = {'class':'tl'})]
    list3 = [i.text.strip() for i in soup.find_all(attrs = {'class':'tr'})]
             
    list1_sum += list1
    list2_sum += list2
    list3_sum += list3
    
    try:
        driver.find_element_by_class_name('default').click()
    except:
        break
    
total = list1_sum[::3] + list1_sum[1::3] + list1_sum[2::3] + list2_sum[::2] + list2_sum[1::2] + list3_sum 
total = pd.DataFrame(data = [total[i*len(list3_sum):(i+1)*len(list3_sum)] for i in range(6)], 
                     index = ['접수번호','품명','발주(공고)기관','예정금액','접수일자','요청구분']).T
    
                     
                     