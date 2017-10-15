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

import os
import xlwings as xw

os.chdir('C:/Users/HS/Desktop/과외/studyroom/숙제(흥)/일일영업현황')

wb8 = xw.Book('170918_DC율(2).xlsx')
wb4 = xw.Book('170918_DC율(3).xlsx')

sht11 = wb4.sheets['PriceList']
sht13 = wb8.sheets['PriceList']

for x in range(33670, 40000):
    if sht11.range('A{}'.format(x)).value == None:
        break

copy13 = sht11.range('A33670:G{}'.format(x-1)).value
sht13.range('A33670:G{}'.format(x-1)).value = copy13

