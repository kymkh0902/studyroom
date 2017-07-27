# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 23:38:12 2017

@author: hslee3
"""

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


local_sum = []
name_sum = []
num_sum = []
month_sum = []
year_sum = []


year = 2018


for mon in range(6, 13):
    for page in range(0, 200, 50):
        
        
        url = 'http://www.drapt.com/theme/theme_special/index.htm?page_name=movedate&\
        page_name=movedate&menu_key=&view_count=50&sort_gubun=&sort_stat=DESC&\
        year=2018&cmonth={}&start={}'.format(mon, page)
        
        
        req = requests.get(url)
        req = req.text
        
        
        soup = bs(req, 'lxml')
        
        
        local = [page.text for page in soup.find_all(attrs = {'class' : 'ffdu ls-2 fs11 tal'})]
        name = [page.text for page in soup.find_all(attrs = {'class' : "c0e5a97"})]
        num = [page.text for page in soup.find_all(attrs = {'width' : "60"})]
        
#==============================================================================
#         m = [mon] * len(local)
#         y = [year] * len(local)
#==============================================================================

        for month_count in range(0, len(local)):
            month_sum.append(mon)
            year_sum.append(year)

        
        local_sum += local
        name_sum += name
        num_sum += num
        
        
        if local == None:
            break
        

result = pd.DataFrame(data = [year_sum, month_sum, name_sum, local_sum, num_sum],
                      index = ['년도', '월', '아파트명', '위치', '가구수']).T


result = result[result['위치'].str.contains(r'대전광역시|경기도|서울특별|세종특별|신도시|인천광역시|충청남도|충청북도|강원도')]
result['가구수'] = pd.to_numeric(result['가구수'], errors='coerce')
result = result[result['가구수'] >=500]


result.to_excel('C:/Users/hslee3/Desktop/개인용/과외/수업자료/studyroom/숙제/2018년 입주 아파트(6월~12월,500세대)(2).xls', index = False)



        
        
               