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

today = datetime.datetime.today()
time_local = time.localtime()
time_name = ('%d.%d.%d_' % (time_local.tm_year, time_local.tm_mon, time_local.tm_mday))

username = getpass.getuser()    # getpass 모듈로 username 불러오기
username = 'yzz07'
save_location = 'C:\\Users\\' + username + '\\Desktop'
save_name = save_location + '\\' + name

if os.path.exists(save_name) == False:
    os.mkdir(save_name) 
    os.chdir(save_name)
else:
    os.chdir(save_name)

# %% 
data_main = []  # 대분류
data_middle = []  # 중분류
data_type = []  # 고용형태
data_budget = []  # 예산 
data_period = []  # 작업기간
data_proposal = []  # 받은 제안
data_title = []  # 제목
data_url = []  # 링크 
data_deadline = []  # 마감일
data_notice = []  # 공고일

url = 'https://kmong.com/custom-project/requests'
driver.get(url)
time.sleep(random.uniform(3, 6)) 

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
soups = soup.find('div', 'right-menu-content-wrapper position-relative')
content = soups.find_all('div', 'request-list-group-wrapper')

page_counts = soup.find('ul','pagination').find_all('li', 'page-item')[-1].text
page_counts = int(page_counts)

for j in range(1, page_counts + 1) : 
    url = 'https://kmong.com/custom-project/requests?q=&sort=created_at&category_list=&sub_category_list=&project_type=&page=%s' %j
    driver.get(url)
    time.sleep(random.uniform(2, 6)) 

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    soups = soup.find('div', 'right-menu-content-wrapper position-relative')
    content = soups.find_all('div', 'request-list-group-wrapper')

    for i in content :
        time.sleep(0.5)
        data_temp = []
        data_main_ = i.find('div', 'CustomProjectRequestItem__breadcrumb').text.replace(' ', '').replace('\n', '')
        data_temp = data_main_.split('/')
        data_type_ = i.find('span', 'CustomProjectRequestItem__item-additional-info-text').text.replace(' ', '').replace('\n', '')

        data_budget_1 = i.find('div', 'CustomProjectRequestItem__detail-label').text.replace(' ', '').replace('\n', '')
        data_budget_2 = i.find('div', 'CustomProjectRequestItem__detail-value').text.replace(' ', '').replace('\n', '')
        data_budget_ = data_budget_1 + ' '+ data_budget_2
    
        data_period_ = i.find('div','CustomProjectRequestItem__detail-info').find_all('div', 'CustomProjectRequestItem__detail-value')[1].text
        data_proposal_ = i.find('div','CustomProjectRequestItem__detail-info').find_all('div', 'CustomProjectRequestItem__detail-value')[2].text
        data_title_ = i.find('span','CustomProjectRequestItem__title').text
        
        get_url = i.find('a', 'CustomProjectRequestItem')['href'] # url
        get_url = 'https://kmong.com' + get_url
        
        data_main.append(data_temp[0]) # 대분류
        data_middle.append(data_temp[1]) # 중분류
        data_type.append(data_type_)    # 고용형태
        data_budget.append(data_budget_)
        data_proposal.append(data_proposal_) # 받은 제안
        data_period.append(data_period_) # 작업기간
        data_title.append(data_title_) # 제목
        data_url.append(get_url)

df = pd.DataFrame()
df['main'] = pd.Series(data_main)
df['middle'] = pd.Series(data_middle)
df['type'] = pd.Series(data_type)
df['budget'] = pd.Series(data_budget)
df['period'] = pd.Series(data_period)
df['proposal'] = pd.Series(data_proposal)
df['title'] = pd.Series(data_title)
df['url'] = pd.Series(data_url)

fc_name = (time_name + name + '.csv')
fx_name = (time_name + name + '.xlsx')

df.to_csv(fc_name, index=False, encoding="utf-8-sig")

print('작업이 완료되었습니다.')
# %%