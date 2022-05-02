#%%
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


s = Service("C:/Users/yzz07/Desktop/PROGRAMMING/chromedriver.exe")
driver = webdriver.Chrome(service=s)


url = 'https://blog.naver.com/hrlee10102/221557590260'
driver.get(url)
time.sleep(2)
driver.maximize_window()



#%%

driver.switch_to.frame('mainFrame')
html_2 = driver.page_source
soup_2 = BeautifulSoup(html_2, 'html.parser')

blog_type_1 = soup_2.find_all('div', 'se-viewer se-theme-default')



# %%
naver_body_1 = soup_2.find_all('div', 'se-section se-section-text se-l-default')
for i in naver_body_1 :
    naver_body_2 = i.text
    print(naver_body_2)

# %%
print(naver_body_1)
# %%

s = Service("C:/Users/yzz07/Desktop/PROGRAMMING/chromedriver.exe")
driver = webdriver.Chrome(service=s)


url = 'https://blog.naver.com/PostThumbnailList.nhn?isHttpsRedirect=true&blogId=the_trip&from=postList&categoryNo=94&parentCategoryNo=94'
driver.get(url)
time.sleep(2)
driver.maximize_window()


# %%
html_2 = driver.page_source
soup_2 = BeautifulSoup(html_2, 'html.parser')
# %%
naver_body_1 = soup_2.find('tbody')


# %%
