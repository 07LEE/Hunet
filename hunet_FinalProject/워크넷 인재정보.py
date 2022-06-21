# %%
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time, math, os, random, urllib, urllib.request

# %%
Services = Service("C:/Users/yzz07/Desktop/PROGRAMMING/chromedriver.exe")
driver = webdriver.Chrome(service=Services)
url = 'https://www.work.go.kr/member/bodyLogin.do?redirectUrl=/seekWantedMain.do'
driver.get(url)
time.sleep(2)

input('로그인 후 진행해 주세요.') # 로그인 진행하기

# %% 
name = 'worknet'  # 저장할 파일명
time_local = time.localtime()
time_name = ('%d.%d.%d_' % (time_local.tm_year, time_local.tm_mon, time_local.tm_mday))

ft_name = (time_name + name + '.txt')
fc_name = (time_name + name + '.csv')
fx_name = (time_name + name + '.xls')

# %%
driver.find_element(By.XPATH, '//*[@id="gnb"]/ul/li[5]/a').click()
driver.find_element(By.XPATH, '//*[@id="main_contents"]/section[1]/div[1]/ul/li[1]/p[2]/a').click()

# %%
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
content = soup.find('table', 'board-list').find_all('tr')

# %%



# %%

