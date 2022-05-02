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
# username = 'yzz07'
save_location = 'C:\\Users\\' + username + '\\Desktop'
save_name = save_location + '\\' + 'DATA'

if os.path.exists(save_name) == False:
    os.mkdir(save_name)
    os.chdir(save_name)
else:
    os.chdir(save_name)

#%%

c_driver = save_location + '\\chromedriver.exe'
s = Service(c_driver)
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

driver.find_element(By.ID, 'hdtb-tls').click()
time.sleep(1)
driver.find_element(By.ID, 'ow36').click()
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

#%%
element = driver.find_element(By.ID, 'OouJcb')
element.send_keys('%s' % date_start)
time.sleep(0.5)
element.send_keys(Keys.TAB + '%s' % date_end )
time.sleep(0.1)
element.send_keys(Keys.ENTER)

# %%
# %%
