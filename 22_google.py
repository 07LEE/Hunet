#%%
from dataclasses import replace
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
import os
import math
import sys
import re
import csv
import getpass
import urllib.request
import urllib
from tqdm.notebook import tqdm
import win32com.client as win32
import win32api

def scroll_down(driver):
    driver.execute_script("window.scrollBy(0,3000);")
    time.sleep(1)
    driver.execute_script("window.scrollBy(0,3000);")

def scroll_up(driver):
    driver.execute_script("window.scrollBy(0,-500);")
    time.sleep(2)


# 저장할 파일명 설정
time_local = time.localtime()
time_name = ('%d.%d.%d_' % (time_local.tm_year,
             time_local.tm_mon, time_local.tm_mday))

name = input('결과를 저장할 파일 명을 쓰세요 : ')  # 저장할 파일명

ft_name = (time_name + name + '_GG' + '.txt')
fc_name = (time_name + name + '_GG' + '.csv')
fx_name = (time_name + name + '_GG' + '.xls')

# 저장할 경로 설정 (바탕화면)
username = getpass.getuser()    # getpass 모듈로 username 불러오기
username = 'yzz07'
save_location = 'C:\\Users\\' + username + '\\Desktop'
save_name = save_location + '\\' + 'DATA'

if os.path.exists(save_name) == False:
    os.mkdir(save_name)
    os.chdir(save_name)
else:
    os.chdir(save_name)

#%%

s = Service("C:/Users/yzz07/Desktop/PROGRAMMING/chromedriver.exe")
driver = webdriver.Chrome(service=s)
query_txt = "국내여행"  # 검색할 키워드

url = 'https://www.google.com/'
driver.get(url)
time.sleep(2)
driver.maximize_window()

#%%

element = driver.find_element(By.NAME, 'q')
element.send_keys('%s' % query_txt)
element.send_keys('\n')

driver.find_element(By.LINK_TEXT, '뉴스').click()
time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="hdtb-tls"]').click()
time.sleep(1)
driver.find_element(By.XPATH, '/html/body/div[7]/div/div[4]/div/div[2]/div/span[2]/g-popup/div[1]/div/div/div').click()
time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="lb"]/div/g-menu/g-menu-item[8]/div/div/span').click()
#%%

date_start = input('조회 시작일을 입력해주세요 (예 : 2021-01-01) : ')
date_end = input('조회 종료일을 입력해주세요 (예 : 2021-12-31) : ')

if date_start == '':
    date_start = '2021-01-01'
if date_end == '':
    date_end = '2021-12-31'

date_start = date_start.split('-')
date_start = (date_start[1] + '/' + date_start[2] + '/' + date_start[0])

date_end = date_end.split('-')
date_end = (date_end[1] + '/' + date_end[2] + '/' + date_end[0])

element = driver.find_element(By.ID, 'OouJcb')
element.send_keys('%s' % date_start)
time.sleep(0.5)
element.send_keys(Keys.TAB + '%s' % date_end )
time.sleep(0.1)
element.send_keys(Keys.ENTER)

collect_cnt = int(input('몇 건의 데이터를 수집하시겠습니까? : '))
if collect_cnt > 300 :
    collect_cnt = 300

google_tit = []          # 게시글 제목 저장
google_date = []
google_body = [] 
google_url = []

f = open(ft_name, 'a', encoding="UTF-8")

while collect_cnt > len(google_tit):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find('div', 'v7W49e').find_all('g-card', 'ftSUBd')

    for i in content :
        google_tit_1 = i. find('div','mCBkyc y355M JQe2Ld nDgy9d').text
        google_tit.append(google_tit_1)

        google_body_1 = i.find('div', 'GI74Re nDgy9d').text
        google_body.append(google_body_1)

        google_date_1 = i.find('div', 'OSrXXb ZE0LJd').text
        google_date.append(google_date_1)
        
        google_url_1 = i.find('a', 'WlydOe')['href']
        google_url.append(google_url_1)
        
        
        # 텍스트 저장
        f.write('\n'+'1. 제목 : ' + google_tit_1)
        f.write('\n'+'2. URL 주소 : ' + google_url_1)
        f.write('\n'+'3. 날짜 : ' + google_date_1)
        f.write("\n"+"4. 내용 : " + google_body_1)
        f.write("\n")

    driver.find_element(By.XPATH, '//*[@id="pnnext"]/span[2]').click()

df = pd.DataFrame()
df['제목'] = pd.Series(google_tit)
df['주소'] = pd.Series(google_url)
df['날짜'] = pd.Series(google_date)
df['내용'] = pd.Series(google_body)

df.to_excel(fx_name, index=False, encoding="utf-8", engine='openpyxl')
df.to_csv(fc_name, index=False, encoding="utf-8-sig")