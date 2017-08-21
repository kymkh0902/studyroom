# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 21:46:02 2017

@author: Whi Kwon
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# 대전만 가져오기
pattern = re.compile('대전광역시.*')

# 빈 List 생성
loc_sum = []
apart_nm_sum = []
house_num_sum = []
size_sum = []
m_sum = []
y_sum = []

# 년도, 월, 페이지 별로 for loop
for year in [2016, 2017]:
    for month in range(1,13):
        for page in [i*50 for i in range(0,5)]:
            
            # url 가져오기 (year, month, page만 변함)
            url = 'http://www.drapt.com/theme/theme_special/index.htm?page_name=movedate&page_name=movedate&\
                    menu_key=&view_count=50&sort_gubun=&sort_stat=DESC&year={}&cmonth={}&start={}'.format(year, month, page)
            
            # url html데이터 가져오기
            req = requests.get(url)
            req = req.text
            
            # BeautifulSoup로 읽기
            soup = BeautifulSoup(req, 'lxml')
            
            # 위치 가져오기
            loc = [i.text for i in soup.find_all(attrs = {'class' : 'ffdu ls-2 fs11 tal'})]
            
            # loc 개수가 0이면 page에 아무것도 없으니 다음 month로
            if len(loc) == 0:
                break
            
            # 빈 list 생성
            index = []     

            # loc에 대전만 찾아서 해당되는 순서 index list에 추가한다.                             
            for i,j in enumerate(loc):
                try:
                    re.match(pattern, j).group(0)
                    index.append(i)
                except AttributeError:
                    continue
                                                        
            # 아파트명, 세대수, 면적, 월, 년 찾고 입력
            apart_nm = [i.text for i in soup.find_all(attrs = {'class' : 'c0e5a97'})]
            house_num = [int(i.text) for i in soup.find_all('td',attrs={'width':'60'})]
            size = [i.text for i in soup.find_all(attrs = {'class' : 'tal ffth fs12 wbba'})]
            m = [month] * len(index)
            y = [year] * len(index)
            
            # 대전에 해당되는 값들만 가져오기 
            loc = [loc[i] for i in index]
            apart_nm = [apart_nm[i] for i in index]
            size = [size[i] for i in index]
            house_num = [house_num[i] for i in index]
            
            
            # 위에 만들어놓은 빈 list에 값 추가하기(for loop 진행될 때마다 계속 더해짐.)
            loc_sum += loc
            apart_nm_sum += apart_nm
            house_num_sum += house_num
            size_sum += size
            m_sum += m
            y_sum += y

# 최종적으로 보기 좋게 pandas DataFrame으로 만들고 끝
result = pd.DataFrame(data = [y_sum, m_sum, loc_sum, apart_nm_sum, house_num_sum, size_sum],
                      index = ['년도','월','위치','아파트명','가구수','공급면적']).T

                     

