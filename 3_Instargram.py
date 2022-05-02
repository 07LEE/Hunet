# %%
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
import datetime
import random


def scroll_down(driver):
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    time.sleep(3)


def listToString(str_list):
    result = ""
    for s in str_list:
        result += s + " "
    return result.strip()

#%%


time_local = time.localtime()
time_name = ('%d.%d.%d_' % (time_local.tm_year,
             time_local.tm_mon, time_local.tm_mday))

name = input('결과를 저장할 파일 명을 쓰세요 : ')  # 저장할 파일명

ft_name = (time_name + name + '_IS' + '.txt')
fc_name = (time_name + name + '_IS' + '.csv')
fx_name = (time_name + name + '_IS' + '.xls')

# 경로 설정
username = getpass.getuser()    # getpass 모듈로 username 불러오기
# username = 'yzz07'
save_location = 'C:\\Users\\' + username + '\\Desktop'
save_name = save_location + '\\' + 'DATA'

if os.path.exists(save_name) == False:
    os.mkdir(save_name)
    os.chdir(save_name)
else:
    os.chdir(save_name)

# 기간 설정
format = '%Y-%m-%d'

day_start = input('조회 시작일을 입력해주세요 (예 : 2021-01-01) : ')
day_end = input('조회 종료일을 입력해주세요 (예 : 2021-12-31) : ')

if day_start == '':
    day_start = '2018-01-01'
if day_end == '':
    day_end = '2019-12-31'

day_start = datetime.datetime.strptime(day_start, format)
day_end = datetime.datetime.strptime(day_end, format)

cnt_instar = int(input('해당 기간으로 몇건? : '))

#%%
c_driver = save_location + '\\chromedriver.exe'
s = Service(c_driver)
driver = webdriver.Chrome(service=s)

#%% 로그인

url = 'https://www.instagram.com/'
driver.get(url)
time.sleep(2)

try:
    driver.maximize_window()
except:
    time.sleep(0.1)

user_id = input('아이디를 입력해주세요 : ')
if user_id == '':
    user_id = 'gachilabs'

user_pass = input('비밀번호를 입력해주세요 : ')
if user_pass == '':
    user_pass = 'gachilabs123'

id_input = driver.find_element(By.NAME, 'username')
for i in user_id:
    id_input.send_keys(i)
    time.sleep(0.1)

pass_input = driver.find_element(By.NAME, 'password')
for i in user_pass:
    pass_input.send_keys(i)
    time.sleep(0.2)

pass_input.send_keys('\n')
pass_input.send_keys('\n')
time.sleep(1)

#%%

driver.execute_script('window.open("https://www.instagram.com/");')

_keyword = '국내여행'
url = 'https://www.instagram.com/explore/tags/' + _keyword + '/'
driver.get(url)
time.sleep(2)

try:
    driver.maximize_window()
except:
    time.sleep(0.1)

#%% 데이터 수집

cnt_num = 0

ist_url = []
ist_date = []         # 날짜
ist_tit = []          # 제목 저장
ist_body = []         # 내용 저장
ist_tag = []

driver.switch_to.window(driver.window_handles[0])
driver.find_element(
    By.XPATH, '//*[@id="react-root"]/section/main/article/div[2]/div/div[1]/div[1]').click()

while cnt_num < cnt_instar:

    try:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        ist_url_1 = driver.current_url
        ist_url.append(ist_url_1)

        driver.switch_to.window(driver.window_handles[1])
        driver.get(ist_url_1)
        time.sleep(random.uniform(1, 3))

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        ist_date_1 = soup.find('time', 'FH9sR RhOlS')['datetime']
        str_datetime = ist_date_1[:10]
        ist_date_1 = datetime.datetime.strptime(str_datetime, format)

        if ist_date_1 >= day_start and ist_date_1 <= day_end:
            cnt_num += 1
        else:
            time.sleep(0.1)

        ist_date.append(ist_date_1)

        ist_body_1 = soup.find('div', 'MOdxS').text
        ist_body.append(ist_body_1)

        ist_tag_1 = re.findall(r'#[^s#,\\]+', ist_body_1)
        ist_tag_1 = listToString(ist_tag_1)
        ist_tag.append(ist_tag_1)
        time.sleep(0.5)

        driver.switch_to.window(driver.window_handles[0])
        time.sleep(0.1)

    except:
        time.sleep(0.1)

    driver.switch_to.window(driver.window_handles[0])
    driver.find_element(
        By.XPATH, '/html/body/div[6]/div[2]/div/div[2]/button').click()
    time.sleep(random.uniform(0.1, 2))

#%%
df = pd.DataFrame()
df['주소'] = pd.Series(ist_url)
df['날짜'] = pd.Series(ist_date)
df['내용'] = pd.Series(ist_body)
df['태그'] = pd.Series(ist_tag)

df.to_excel(fx_name, index=False, encoding="utf-8", engine='openpyxl')
df.to_csv(fc_name, index=False, encoding="utf-8-sig")