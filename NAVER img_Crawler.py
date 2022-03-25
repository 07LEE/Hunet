import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
import math
import os
import random
import urllib.request
import urllib


def scroll_down(driver):
    driver.execute_script("window.scrollBy(0,5000);")
    time.sleep(5)


def scroll_up(driver):
    driver.execute_script("window.scrollBy(0,-500);")
    time.sleep(2)


Services = Service("C:/Users/yzz07/Desktop/PROGRAMMING/chromedriver.exe")
driver = webdriver.Chrome(service=Services)


print("=" * 80)
print(" '네이버 이미지' 수집용 웹크롤러입니다.")
print("=" * 80)

url = 'https://www.naver.com/'
driver.get(url)
time.sleep(2)
driver.maximize_window()

search_query = input('검색할 이미지 키워드를 써주세요 : ')

save_name = input('결과를 저장할 파일 명을 쓰세요 : ')

os.chdir('C:/Users/yzz07/Desktop/PROGRAMMING/')
tl = time.localtime()
ti_name = ('%d-%d-%d-%d-%d' %(tl.tm_year, tl.tm_mon, tl.tm_mday, tl.tm_hour, tl.tm_min))
re_name = os.getcwd()
os_name = os.getcwd() + '/' + ti_name + ' ' + save_name

if os.path.exists(os_name) == False:
    os.mkdir(os_name)
    os.chdir(os_name)
else:
    os.chdir(os_name)