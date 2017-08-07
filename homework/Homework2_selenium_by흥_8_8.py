# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 18:13:33 2017

@author: hslee3
"""

from selenium import webdriver as wb
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
import datetime

driver = wb.Chrome('C:/Users/Whi Kwon/Documents/GitHub/python_script/chromedriver.exe')
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

pages = 1

for i in range(pages):
    
    html = driver.page_source
    soup = bs(html, 'lxml')
    
    date = [j.text.strip() for j in soup.find_all(attrs = {'class':'tc'}) if '/' in j.text]
    money = [j.text.strip() for j in soup.find_all(attrs = {'class':'tr'}) if '원' in j.text]
    money = [int(i.replace('원','').replace(',','')) for i in money]
    number = [j.text.strip() for j in soup.find_all(name = 'a', attrs = {'href' : '#'})][1:]
    region = [j.text.strip() for j in soup.find_all(attrs = {'class':'tl'})][1::2]
    click = [j.text.strip() for j in soup.find_all(attrs = {'class':'default'}) if '더보기' in j.text]
    # 'click' 버튼을 추가 : 이유는 밑에 설명
    
    # 우선 적으로 날짜 길이에 한해서 'J'를 2억 이상으로 제한
    for l in range(len(date)):
        
        if money[j] >= 2e8:
            # 다 클릭하는 것이 좋을 것으로 판단
            # 1) 시간이 그리 오래 걸리지 않고, 2) 실제로도 그렇게 하며, 3) 정확도를 높이는 방법
            driver.find_element_by_link_text(number[j]).click()
            # 확인하는 방법은 우선적으로 패스
            
            for k in range(len(date)):
                
                # 8일 전의 날짜가 첫 30페이지에 있었는지 확인
                # 있다면, 위에 걸렀던 정보들 중에 날짜 내에 있는 것들만 확인
                # 여기서 질문!!!
                # 위에 money[j]로 인해 number[j]가 필터가 가능하잖아?
                # 그러면 밑에 date[k]로 date를 필터하고,
                # j와 k의 공통점만 필터하고 싶으면 어떻게 해야함?
                # (그러면 원하는 값을 뽑는게 맞다고 생각함 아니면 말해주삼! ㄳㄳ)
                
                
    ### --> 내가 이해한게 맞으면 약간 로직에 대해 잘못 이해하고 있는 거 같아서 추가 설명함
    ###     지금 우리 로직은 처음에 전체적으로 보고 날짜되면 끊는게 아니라 
    ###     그냥 일단 순차적으로 보다가 중간에 끊는 거임. 전체를 먼저 봐도 되는데 그럼 date를
    ###     페이지(30개)마다 가장 처음에 한번 보고 날짜 확인을하고 만약 넘어가는 날짜가 있으면 그 index를 가져와야 됨. 
    
    ###    일단 순차적으로 보는 로직은 아래와 같음. 아래 내용으로 한다면 로직 아래처럼 순서 바꿔주면 됨. 
    ###    1) for문으로 전부다 순차적으로 볼거임
    ###    2) 날짜가 어느 날짜가 되면 더 이상 안 볼거임 (날짜가 넘었는데도 보다가 끊는 건 비효율적)
    ###    3) 2억이 넘으면 들어가서 볼거임
    ###    4) for문이 돌아갈 때 모든 index(순서)는 똑같으므로 추가적인 for문 사용 필요 없음. 
    
    ### --> 추가 사항(우선 순위 순서)
    ###    
    ###    1) 틀을 가장 먼저 짜는게 중요. 추가 조건문 위치에 대한 고민, 
    ###       확인 방법, 확인 이후에 대한 내용 업데이트 필요. 시작~끝까지 전체적인 흐름을 그려주셈. 
    ###    2) 틀을 거의다 짰다고 생각이 들면 세부 내용(unit 코드) 채우기 시작. 
    ###       내용을 채울 때는 간단한 예제로 확인하고 되면 넘어가는 식으로 진행하면 됨. 
    ###       전체 코드를 돌릴 필요는 없고 해당 부분만 다른 예제로 돌려도 되고 
    ### 
    ###       selenium 웹 확인 같은 경우에는 
    ###       chromedriver 킨 다음에 console창에서 입력해서 확인하면서 완성하면 됨. 
    ###       확인한 다음에 까먹을 수 있으니 unit 코드 구현 뒤에는 예제를 어떻게 뭘로 했는 지 항상 기록할 것. 
                
                # 날짜에 대한 로직
                if week_day_ago in date[k]:
                        ### 순차적으로 하나씩 보는거니까 == 이 좋을듯
                    # 원하는 날짜가 안에 있다면 전체 for문을 break!
                    break
                    

                # 아니면, '더보기' 클릭
                # '더보기'의 xpath가 페이지 마다 다름을 확인
                # //*[@id="pagination"]/a
                # //*[@id="pagination"]/a[3]
                # //*[@id="pagination"]/a[4]
                # 따라서 link)_text로 'click' 텍스트 클릭하도록 함
                else:
                    driver.find_element_by_link_text(click).click()


                    


