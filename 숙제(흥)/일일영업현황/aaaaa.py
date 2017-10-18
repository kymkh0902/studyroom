import pandas as pd
import os
import datetime
import xlwings as xw
from xlwings.constants import DeleteShiftDirection
import win32com.client

os.chdir('C:/Users/HS/Desktop/과외/studyroom/숙제(흥)/일일영업현황')

data1 = pd.read_csv('171012_미출하.xls', sep='\t',
                    encoding='euc-kr', engine='python')

data1 = data1[data1['Price List'].str.contains
(r'(전략|범용)제품.(2013|2016)')]
data1 = data1[data1['Department'].str.contains(r'대전Part')]
del data1['Unnamed: 0']
del data1['Drop Ship Flag']
del data1['Country.1']
del data1['Line Additional Remarks']
del data1['Releated Managing No.']
del data1['File Attached']
del data1['Unnamed: 77']

data1.to_excel('171012_미출하(2).xls', index=False)