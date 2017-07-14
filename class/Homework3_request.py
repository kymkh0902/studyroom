# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 21:35:50 2017

@author: Whi Kwon
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

item = {'전반':'%C0%FC%B9%DD','태양광':'%C5%C2%BE%E7%B1%A4'}
start_date = '20170415'
end_date = '20170714'
page_max = 10
sum1 = []
sum2 = []
sum3 = []

# url1 뭐더라..
for item in item.keys():
    for page in range(1,page_max+1):
        url = '''
            http://www.g2b.go.kr:8091/cm/contstus/listPpsItemContractReqStus.do?_stddocExistYn=on
            &bchppsNo=XX&contractClCd=&g2bProdCateNo=&instName=&prodNm=%C0%FC%B9%DD&rcptDtFrom={}%2F{}%2F{}
            &rcptDtTo={}%2F{}%2F{}&recordCountPerPage=30&searchType=1&currentPageNo={}&maxPageViewNoByWshan=2&
            '''.format(start_date[:4], start_date[4:6], start_date[6:8], end_date[:4], 
                       end_date[4:6], end_date[6:8],page)
        
        req = requests.get(url).text
        soup = BeautifulSoup(req, 'lxml')
        
        list1 = [i.text.strip() for i in soup.find_all(attrs = {'class':'tc'})]
        if len(list1) == 0:
            break
        list2 = [i.text.strip() for i in soup.find_all(attrs = {'class':'tl'})]
        list3 = [i.text.strip() for i in soup.find_all(attrs = {'class':'tr'})]
        
        sum1 += list1
        sum2 += list2
        sum3 += list3
        item_nm = [item]*len(sum3)
        
total = sum1[::3] + sum1[1::3] + sum1[2::3] + sum2[::2] + sum2[1::2] + sum3 
total = pd.DataFrame(data = [item_nm] + [total[i*len(sum3):(i+1)*len(sum3)] for i in range(6)], 
                     index = ['제품명','접수번호','품명','발주(공고)기관','예정금액','접수일자','요청구분']).T
#%%
sum4 = []
                     
# url2, 3 
for page in range(1,page_max+1):
    url = '''
        http://www.g2b.go.kr:8101/ep/tbid/tbidList.do?area=&areaNm=&bidNm=%C0%FC%B9%DD&
        bidSearchType=1&budget=&budgetCompare=UP&detailPrdnm=&detailPrdnmNo=&fromBidDt={}%2F{}%2F{}
        &fromOpenBidDt=&industry=&industryCd=&instNm=&instSearchRangeType=&intbidYn=&procmntReqNo=
        &radOrgan=1&recordCountPerPage=30&refNo=&regYn=Y&searchDtType=1&searchType=1&taskClCds=1
        &toBidDt={}%2F{}%2F{}&toOpenBidDt=&currentPageNo={}&maxPageViewNoByWshan=2&
        '''.format(start_date[:4], start_date[4:6], start_date[6:8], end_date[:4], 
                   end_date[4:6], end_date[6:8],page)
    
    req = requests.get(url).text
    soup = BeautifulSoup(req, 'lxml')
    
    total = [i.text.strip() for i in soup.find_all('td')]
    sum4 += total
total = pd.DataFrame(data = [sum4[i::10] for i in range(10)], 
                     index = ['업무','공고번호,차수','분류','공고명','공고기관','수요기관',
                              '계약방법','입력일시(입찰마감일시)','공동수급','투찰']).T



