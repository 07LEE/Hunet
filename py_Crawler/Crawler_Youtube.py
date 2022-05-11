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

ft_name = (time_name + name + '_YB' + '.txt')
fc_name = (time_name + name + '_YB' + '.csv')
fx_name = (time_name + name + '_YB' + '.xls')

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

# 검색할 키워드 설정
c_driver = save_location + '\\chromedriver.exe'
s = Service(c_driver)
driver = webdriver.Chrome(service=s)
query_txt = "국내여행"  # 검색할 키워드

url = 'https://www.youtube.com/'
driver.get(url)
time.sleep(2)
driver.maximize_window()

day_start = input('조회 시작일을 입력해주세요 (예 : 2021-01-01) : ')
day_end = input('조회 종료일을 입력해주세요 (예 : 2021-12-31) : ')

if day_start == '':
    day_start = '2018-06-01'
if day_end == '':
    day_end = '2018-12-31'

Yday_start = "after:" + day_start
Yday_end = "before:" + day_end

query_txt = query_txt + " " + Yday_start + " " + Yday_end


driver.find_element(By.NAME, 'search_query').click()
element = driver.find_element(By.NAME, 'search_query')
element.send_keys('%s' % query_txt)
element.send_keys('\n')
time.sleep(2)

cnt_ytube = int(input('해당 주제로 크롤링할 유튜브 영상은 몇 건입니까? : '))

# 동영상 갯수 확인

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
ytb_all = soup.find_all('a', {'id': 'video-title'})

while len(ytb_all) < cnt_ytube:

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    ytb_all = soup.find_all('a', {'id': 'video-title'})
    scroll_down(driver)
    scroll_down(driver)

    try:
        scroll_end = soup.find('yt-formatted-string',
                               {'id': 'message'}).get_text()
        if scroll_end == '결과가 더 이상 없습니다.':
            cnt_ytube = len(ytb_all)
            break
    except:
        scroll_down(driver)

# URL 수집

ytb_url = []
data_url_cnt = 0

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
content = soup.find(
    'div', 'style-scope ytd-search').find_all('ytd-video-renderer')

for i in content:
    url_1 = i.find(
        'a', 'yt-simple-endpoint style-scope ytd-video-renderer')['href']
    url_1 = "https://www.youtube.com/" + url_1
    ytb_url.append(url_1)
    data_url_cnt += 1

    if data_url_cnt >= cnt_ytube:
        break


#%%

# 데이터 저장

ytb_date = []         # 작성자 닉네임 저장
ytb_tit = []          # 게시글 제목 저장
ytb_body = []         # 게시글 내용 저장
ytb_tag = []

f = open(ft_name, 'a', encoding="UTF-8")

for i in tqdm(range(len(ytb_url))):
    url_2 = ytb_url[i]
    driver.get(url_2)
    try:
        driver.maximize_window()
    finally:
        time.sleep(2)
    try:
        try:
            driver.find_element(
                By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[8]/div[2]/div[2]/ytd-video-secondary-info-renderer/div/ytd-expander/tp-yt-paper-button[2]').click()
        except:
            driver.find_element(By.ID, 'more').click()

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        ytb_tit_1 = soup.find(
            'yt-formatted-string', 'style-scope ytd-video-primary-info-renderer').text
        ytb_date_1 = soup.find('div', {'id': 'info-strings'}).find(
            'yt-formatted-string', 'style-scope ytd-video-primary-info-renderer').text
        ytb_body_1 = soup.find('div', 'style-scope ytd-expander').text

        ytb_date_1 = ytb_date_1.replace('최초 공개: ', '')

        ytb_tit.append(ytb_tit_1)
        ytb_date.append(ytb_date_1)
        ytb_body.append(ytb_body_1)

        f.write('\n'+'1. 제목 : ' + ytb_tit_1)
        f.write('\n'+'2. URL 주소 : ' + ytb_url[i])
        f.write('\n'+'3. 날짜 : ' + ytb_date_1)
        f.write("\n"+'4. 내용 : ' + ytb_body_1)
        f.write("\n")
    except:
        print("shorts 영상")

df = pd.DataFrame()
df['제목'] = pd.Series(ytb_tit)
df['주소'] = pd.Series(ytb_url)
df['날짜'] = pd.Series(ytb_date)
df['내용'] = pd.Series(ytb_body)

df.to_excel(fx_name, index=False, encoding="utf-8", engine='openpyxl')
df.to_csv(fc_name, index=False, encoding="utf-8-sig")

print('작업이 완료되었습니다.')

# %%
