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
today = datetime.datetime.today()

name = 'jobkorea_head'  # 저장할 폴더명
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

# %%
dic_category = {100: '경영·인사·총무·사무', 101: '재무·회계·경리', 102: '마케팅·광고·홍보·조사', 103: '교육·교사·강사·교직원', 104: '디자인', 106: '고객상담·TM ', 107: '건설·건축·토목·환경', 110: '유통·물류·운송·운전', 123: '전자·기계·기술·화학·연구개발', 210: '금융·보험·증권', 190: '의료·간호·보건·복지', 130: '전문직·법률·인문사회·임원', 140: '생산·정비·기능·노무', 170: '서비스·여행·숙박·음식·미용·보안', 150: '무역·영업·판매·매장관리', 160: '인터넷·IT·통신·모바일·게임'}

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

for key, value in dic_category.items():
    url = 'https://chief.incruit.com/jobdb_list/searchjob.asp?occ1=%s'%key
    driver.get(url)
    time.sleep(random.uniform(3, 6)) 

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find('div', 'cBbslist_contenst').find_all('li', 'c_col')

    for i in content : 
        data_url_ = i.find('div', 'cell_mid').find('div', 'cl_top').find('a')['href']
        data_url.append(data_url_)

    break

# %%

