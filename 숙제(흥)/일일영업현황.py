# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 20:31:36 2017

@author: Wade
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 00:42:36 2017

@author: Sun
"""

import pandas as pd
import os
import datetime
import xlwings as xw
from xlwings.constants import DeleteShiftDirection
import win32com.client


os.chdir('C:/Users/hslee3/Desktop/일일영업현황')

#%%

# 엑셀 파일 열기

date = datetime.date.today()
dateYMD = date.strftime('%Y%m%d')[2:]
dateD = date.strftime('%d')


a = int(dateYMD)


if date.weekday() == 0:
    b = a-3
else : b = a-1


c = int(dateD)


data1 = pd.read_csv('{}_미출하.xls'.format(a), sep ='\t',
                    encoding = 'euc-kr', engine = 'python')

data2 = pd.read_csv('{}_출하.xls'.format(a), sep ='\t',
                    encoding = 'euc-kr', engine = 'python',)

data3 = pd.read_csv('{}_일반.xls'.format(a), sep ='\t',
                    encoding = 'euc-kr', engine = 'python',)

data4 = pd.read_csv('{}_신제품.xls'.format(a), sep ='\t',
                    encoding = 'euc-kr', engine = 'python',)


#%%

# 각 엑셀 파일 수정

# 미출하
data1 = data1[data1['Price List'].str.contains
              (r'(전략|범용)제품.(2013|2016)')]
data1 = data1[data1['Department'].str.contains(r'대전Part')]
del data1['Unnamed: 0']
del data1['Drop Ship Flag']
del data1['Releated Managing No.']
del data1['Unnamed: 74']

data1.to_excel('{}_미출하(2).xls'.format(a), index = False)

# 출하
data2 = data2[data2['Price List'].str.contains
              (r'(전략|범용)제품.(2013|2016)')]
data2 = data2[data2['Department'].str.contains(r'대전Part')]
del data2['Unnamed: 0']
del data2['Drop Ship Flag']
del data2['Releated Managing No.']
del data2['Unnamed: 74']

data2.to_excel('{}_출하(2).xls'.format(a), index = False)

# 일반
data3 = data3[~data3['Order Type'].str.contains
              (r'(Svc|svc)_')]
data3 = data3[data3['Department'].str.contains(r'대전Part')]
del data3['Unnamed: 0']
del data3['Unnamed: 35']
data3['Customer(B)'] = data3['Customer(B)'].map(lambda x: x.lstrip('A='))
data3['Customer(B)'][data3['Customer(B)'].str.contains(r'한민산전')] = '한민산전__LEL'
data3['Customer(B)'][data3['Customer(B)'].str.contains(r'신영전재')] = '신영전재__LEL'
data3['Customer(B)'][data3['Customer(B)'].str.contains(r'에이스')] = '(주)에이스산전__LEL'
data3['Customer(B)'][data3['Customer(B)'].str.contains(r'대창')] = '분전반'
data3['Customer(B)'][data3['Customer(B)'].str.contains(r'홈플러스|보령')] = 'Retrofit'
data3['Customer(B)'][data3['Customer(B)'].str.contains(r'주안전기')] = 'AMR'

data3.to_excel('{}_일반(2).xls'.format(a), index = False)

# 신제품
data4 = data4[data4['Department'].str.contains(r'대전Part')]
del data4['Unnamed: 0']
del data4['Unnamed: 35']

data4.to_excel('{}_신제품(2).xls'.format(a), index = False)


#%%

# 원본 데이터 수정하기

wb1 = xw.Book('원본_{}(by흥).xls'.format(b))
wb2 = xw.Book('{}_일반(2).xls'.format(a))
wb3 = xw.Book('{}_신제품(2).xls'.format(a))

sht1 = wb1.sheets['대전']
sht2 = wb2.sheets['Sheet1']
sht3 = wb1.sheets['원본Data']
sht4 = wb3.sheets['Sheet1']
sht5 = wb1.sheets['신제품시트']
sht6 = wb1.sheets['주문 현황']
sht7 = wb1.sheets['Sheet2']

copy1 = sht1.range('K5:K70').options(ndim=2).value
sht1.range('L5:L70').value = copy1

copy2 = sht1.range('Q5:Q70').options(ndim=2).value
sht1.range('R5:R70').value = copy2

copy3 = sht1.range('AB5:AB38').options(ndim=2).value
sht1.range('AC5:AC38').value = copy3
          
copy4 = sht1.range('AG5:AG38').options(ndim=2).value
sht1.range('AH5:AH38').value = copy4
          
copy5 = sht1.range('AL5:AL70').options(ndim=2).value
sht1.range('AM5:AM70').value = copy5
          
copy6 = sht1.range('BD5:BD38').options(ndim=2).value
sht1.range('BE5:BE38').value = copy6
               
sht3.clear_contents()
sht3.clear_contents()

copy7 = sht2.range('A1:AZ2000').value
sht3.range('A1:AZ2000').value = copy7

sht5.clear_contents()
sht5.clear_contents()

copy8 = sht4.range('A1:AZ2000').value
sht5.range('A1:AZ2000').value = copy8

copy9 = sht1.range('U38').value
          
for i in range(1, 30):
    if sht6.range('AN{}'.format(i)).value == c:
        sht7.range('D4').value = copy9
        sht6.range('AM{}'.format(i)).value = copy9
        sht7.range('C4').value = sht6.range('AP{}'.format(i)).value
        sht7.range('B4').value = sht6.range('AR{}'.format(i)).value
        sht6.range('AQ{}'.format(i)).value = sht6.range('AM{}'.format(i)).value - sht6.range('AP{}'.format(i)).value
        sht6.range('AS{}'.format(i)).value = sht6.range('AM{}'.format(i)).value - sht6.range('AR{}'.format(i)).value


wb2.close()
wb3.close()

#%%

# DC 파일 수정하기

wb4 = xw.Book('{}_DC율.xlsx'.format(b))
wb5 = xw.Book('{}_미출하(2).xls'.format(a))
wb6 = xw.Book('{}_출하(2).xls'.format(a))


sht8 = wb4.sheets['로데이터']
sht9 = wb5.sheets['Sheet1']
sht10 = wb6.sheets['Sheet1']
sht11 = wb4.sheets['PriceList']


sht9.range('A1:CC1').api.Delete(DeleteShiftDirection.xlShiftUp)
sht10.range('A1:CC1').api.Delete(DeleteShiftDirection.xlShiftUp)


copy10 = sht9.range('A1:CC5000').value
copy11 = sht10.range('A1:CC5000').value
           

sht8.range('I3:CK5002').value = copy10


for j in range(3, 5002):
    if sht8.range('I{}'.format(j)).value == None:
        sht8.range('I{}:CK5002'.format(j)).value = copy11
        break
          
    
wb4.save('{}_DC율(2).xlsx'.format(b))


copy11 = sht8.range('A3:H5002').value
sht8.range('A3:H5002').value = copy11
      

k = 3
while k < 5002:
    if sht8.range('B{}'.format(k)).value == '02. 제외':
        sht8.range('A{}:CC{}'.format(k,k)).api.delete
    elif sht8.range('B{}'.format(k)).value == '01. 포함':
        k = k+1
    else : break    
          
          
for o in range(33600, 35000):
    if sht11.range('A{}'.format(o)).value == None:
        break
    
    
for l in range(3, 5002):
    if sht8.range('E{}'.format(l)).value == '구가격없음':
        sht11.range('A{}:B{}'.format(o,o)).value = sht8.range('O{}:P{}'.format(l,l)).value
        sht11.range('D{}'.format(o)).value = sht8.range('D{}'.format(l)).value
        sht11.range('G{}'.format(o)).value = sht8.range('F{}'.format(l)).value
        o = o+1


for n in range(33600, 35000):
    if sht11.range('D{}'.format(n)).value == '전력기기_범용제품_2016_1':
        sht11.range('G{}'.format(n)).value = sht11.range('G{}'.format(n)).value/(1-0.294)


for m in range(33600, 35000):
    if sht11.range('D{}'.format(m)).value == '전력기기_범용제품_2016_1':
        sht11.range('D{}'.format(m)).value = '신규등록_범용'
    elif sht11.range('D{}'.format(m)).value == '전력기기_전략제품_2016_1':
        sht11.range('D{}'.format(m)).value = '신규등록_전략'


for p in range(3, 5002):
    if sht8.range('E{}'.format(p)).value == '구가격없음' and \
                 sht8.range('D{}'.format(p)).value == '전력기기_범용제품_2016_1':
                     sht8.range('D{}'.format(p)).value = '신규등록_범용'
                     sht8.range('E{}'.format(p)).value = '신규등록_범용'
                     sht8.range('F{}'.format(p)).value = sht8.range('F{}'.format(p)).value / (1-0.294)
                     sht8.range('G{}'.format(p)).value = sht8.range('G{}'.format(p)).value / (1-0.294)
    elif sht8.range('E{}'.format(p)).value == '구가격없음' and \
                 sht8.range('D{}'.format(p)).value == '전력기기_전략제품_2016_1':
                     sht8.range('D{}'.format(p)).value = '신규등록_전략'
                     sht8.range('E{}'.format(p)).value = '신규등록_전략'



wb4.save('{}_DC율(3).xlsx'.format(b))
wb4.close()
wb5.close()
wb6.close()


office = win32com.client.Dispatch("Excel.Application")
wb = office.Workbooks.Open(r"C:/Users/hslee3/Desktop/일일영업현황/{}_DC율(3).xlsx".format(b))


count = wb.Sheets.Count


for i in range(count):
    ws = wb.Worksheets[i]
    ws.Unprotect() # IF protected


    pivotCount = ws.PivotTables().Count
    for j in range(1, pivotCount+1):
        ws.PivotTables(j).PivotCache().Refresh()


wb.Close(True)


wb7 = xw.Book('{}_DC율(3).xlsx'.format(b))


sht12 = wb7.sheets['DC율 특약점별']


#%%

# DC 원본으로 옮기기

sht1.range('BD5:BD12').options(ndim=2).value = sht12.range('D5:D12').options(ndim=2).value
sht1.range('BD15:BD20').options(ndim=2).value = sht12.range('D13:D18').options(ndim=2).value
sht1.range('BD22:BD25').options(ndim=2).value = sht12.range('D19:D22').options(ndim=2).value
sht1.range('BD38').value = sht12.range('D23').value


dae1b = 0
dae1c = 0
dae2b = 0
dae2c = 0
dae3b = 0
dae3c = 0
          

for q in range(5, 13):
    dae1b = dae1b + float(sht12.range('B{}'.format(q)).value)


for r in range(13, 19):
    dae2b = dae2b + float(sht12.range('B{}'.format(r)).value)


for s in range(19, 23):
    dae3b = dae3b + float(sht12.range('B{}'.format(s)).value)


for t in range(5, 13):
    dae1c = dae1c + float(sht12.range('C{}'.format(t)).value)


for u in range(13, 19):
    dae2c = dae2c + float(sht12.range('C{}'.format(u)).value)


for v in range(19, 23):
    dae3c = dae3c + float(sht12.range('C{}'.format(v)).value)


sht1.range('BD14').value = float(1 - (dae1c/dae1b))
sht1.range('BD21').value = float(1 - (dae2c/dae2b))
sht1.range('BD26').value = float(1 - (dae3c/dae3b))


wb7.close()
wb1.save('원본_{}(by흥)(2).xls'.format(b))



