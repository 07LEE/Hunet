import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
import math
import os

# 파일 경로를 지금 있는 파일 위치로 변경
os.chdir(os.path.dirname(os.path.realpath(__file__)))

print("=" * 100)
print(" 이 크롤러는 RISS 논문 수집용 웹크롤러입니다.")
print("=" * 100)

query_txt = input('1.수집할 자료의 키워드는 무엇입니까? : ')

name = input('2. 결과를 저장할 파일 명을 쓰세요 : ')
ft_name = (name+'.txt')
fc_name = (name+'.csv')
fx_name = (name+'.xls')

ft_name = (name+'.txt')
fc_name = (name+'.csv')
fx_name = (name+'.xls')
os_name = (os.getcwd()+'\\'+name)

if os.path.exists(os_name) == False:
    os.mkdir(os_name)
    os.chdir(os_name)
else:
    os.chdir(os_name)

s = Service(
    'C:\\Users\\yzz07\\Desktop\\PROGRAMMING\\22_Hunet study\\Personal practice (Py)\\chromedriver.exe')
driver = webdriver.Chrome(service=s)

url = 'https://www.riss.kr/'
driver.get(url)
time.sleep(5)
driver.maximize_window()

element = driver.find_element(By.ID, 'query')
element.send_keys(query_txt)
element.send_keys("\n")

driver.find_element(By.LINK_TEXT, '학위논문').click()
time.sleep(2)

html_1 = driver.page_source
soup_1 = BeautifulSoup(html_1, 'html.parser')
content_1 = soup_1.find('div', 'srchResultListW').find_all('li')

total_cnt = soup_1.find('div', 'searchBox pd').find('span', 'num').get_text()
print('검색하신 키워드 %s (으)로 총 %s 건의 학위논문이 검색되었습니다' % (query_txt, total_cnt))
collect_cnt = int(input('이 중에서 몇 건을 수집하시겠습니까?: '))
collect_page_cnt = math.ceil(collect_cnt / 10)
print('%s 건의 데이터를 수집하기 위해 %s 페이지의 게시물을 조회합니다.' %
      (collect_cnt, collect_page_cnt))
print('=' * 80)

no2 = []  # 번호 저장
title2 = []  # 논문제목 저장
writer2 = []  # 논문저자 저장
org2 = []  # 소속기관 저장
no = 1

for a in range(1, collect_page_cnt + 1):

    html_2 = driver.page_source
    soup_2 = BeautifulSoup(html_2, 'html.parser')

    content_2 = soup_2.find('div', 'srchResultListW').find_all('li')

    for b in content_2:
        #1. 논문제목 있을 경우만
        try:
            title = b.find('div', 'cont').find('p', 'title').get_text()
        except:
            continue
        else:
            f = open(ft_name, 'a', encoding="UTF-8")
            print('1.번호:', no)
            no2.append(no)
            f.write('\n'+'1.번호:' + str(no))

            print('2.논문제목:', title)
            title2.append(title)
            f.write('\n' + '2.논문제목:' + title)

            writer = b.find('span', 'writer').get_text()
            print('3.저자:', writer)
            writer2.append(writer)
            f.write('\n' + '3.저자:' + writer)

            org = b.find('span', 'assigned').get_text()
            print('4.소속기관:', org)
            org2.append(org)
            f.write('\n' + '4.소속기관:' + org + '\n')

            f.close()

            no += 1
            print("\n")

            if no > collect_cnt:
                break

            time.sleep(1)        # 페이지 변경 전 1초 대기

    a += 1
    b = str(a)

    try:
        driver.find_element(By.LINK_TEXT, '%s' % b).click()
    except:
        driver.find_element(By.LINK_TEXT('다음 페이지로')).click()

print("요청하신 작업이 모두 완료되었습니다")

# Step 10. 수집된 데이터를 xls와 csv 형태로 저장하기

df = pd.DataFrame()
df['번호'] = no2
df['제목'] = pd.Series(title2)
df['저자'] = pd.Series(writer2)
df['소속(발행)기관'] = pd.Series(org2)

df.to_excel(fx_name, index=False, encoding="utf-8", engine='openpyxl')
df.to_csv(fc_name, index=False, encoding="utf-8-sig")

print('요청하신 데이터 수집 작업이 정상적으로 완료되었습니다')
