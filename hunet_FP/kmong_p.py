# %%
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time, math, os, random, urllib, urllib.request, getpass, re, datetime

# %%
Services = Service("C:/Users/yzz07/Desktop/PROGRAMMING/chromedriver.exe")
driver = webdriver.Chrome(service=Services)

name = 'kmong'  # 저장할 파일명
time_local = time.localtime()
time_name = ('%d.%d.%d_' % (time_local.tm_year,
             time_local.tm_mon, time_local.tm_mday))

username = getpass.getuser()    # getpass 모듈로 username 불러오기
username = 'yzz07'
save_location = 'C:\\Users\\' + username + '\\Desktop'
save_name = save_location + '\\' + name

if os.path.exists(save_name) == False:
    os.mkdir(save_name) 
    os.chdir(save_name)
else:
    os.chdir(save_name)

today = datetime.datetime.today()


# %%
url = 'https://kmong.com/category/1?page=1&sort=ranking_points&company=false&is_prime=false&has_portfolio=false&is_contactable=false&is_fast_reaction=false&ratings=&meta='
driver.get(url)
time.sleep(2)

driver.find_element(By.XPATH, '//*[@id="__next"]/div[3]/div/div/main/div/div[1]/div[1]/div/div[1]/label/span/input').click()
time.sleep(1)

# %%

# [크몽 프라임 컬럼]
# 대분류 / 중분류 / 소분류 / 작업갯수
# 평가갯수 / 찜갯수
# STANDARD가격 / DELUXE가격 / PREMIUM가격
# 제목 / 기업명 / 링크

data_main = []  # 대분류
data_middle = []  # 중분류

data_type = []  # 고용형태
data_budget = []  # 예산 
data_period = []  # 작업기간
data_proposal = []  # 받은 제안

data_evaluation = [] # 평가 갯수
data_title = []  # 제목
data_name = [] # 기업명 
data_url = []  # 링크 

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
soups = soup.find('div', 'css-1xaekgw e19f3kve0')
num = soup.find('div', 'css-qzjq2k e19f3kve6').find_all('li', 'css-w119tg etp7mg1')[-2].text
num = int(num)
# %%

for j in range (2, num+2) :

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    soups = soup.find('div', 'css-1xaekgw e19f3kve0')
    content = soups.find_all('article', 'css-0 e19f3kve2')

    for i in content :
        data_url_ = i.find('a', 'css-j9gtx5 eu87mqk0')['href']
        data_url_ = 'https://kmong.com' + data_url_
        data_url.append(data_url_) # URL 

        data_title_ = i.find('h3', 'css-10894jy eu87mqk7').text
        data_title.append(data_title_) # 제목 

        data_evaluation_ = i.find('div', 'css-0 eu87mqk15').text
        data_evaluation_ = re.sub('[^0-9]', '', data_evaluation_)
        data_evaluation.append(data_evaluation_) # 평가 건수 

        data_name_ = i.find('span', 'css-3eiwm9 eu87mqk6').text
        data_name.append(data_name_) # 기업명

    driver.find_element(By.XPATH, '//*[@id="__next"]/div[3]/div/div/main/div/div[2]/div[2]/ul/li[%s]/button/span' %j).click()
    time.sleep(1)

# %%
for i in data_url :
    driver.get(i)
    time.sleep(0.3)

    break
# %%
