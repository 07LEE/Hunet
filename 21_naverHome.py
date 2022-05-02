# %% NAVER BLOG CRAWLER

from this import d
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
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    time.sleep(3)

#%% 저장할 파일명 설정


time_local = time.localtime()
time_name = ('%d.%d.%d_' % (time_local.tm_year,
             time_local.tm_mon, time_local.tm_mday))

name = input('결과를 저장할 파일 명을 쓰세요 : ')  # 저장할 파일명

ft_name = (time_name + name + '_NBH' + '.txt')
fc_name = (time_name + name + '_NBH' + '.csv')
fx_name = (time_name + name + '_NBH' + '.xls')

# 저장할 경로 설정 (바탕화면)
username = getpass.getuser()    # getpass 모듈로 username 불러오기
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
query_txt = "국내 여행"  # 검색할 키워드

#%%

url = 'https://section.blog.naver.com/'
driver.get(url)
time.sleep(2)
try :
    driver.maximize_window()
except :
    time.sleep(0.1)

#%%

element = driver.find_element(By.XPATH, '//*[@id="header"]/div[1]/div/div[2]/form/fieldset/div/input')
element.send_keys('%s' % query_txt)
element.send_keys('\n')
time.sleep(2)

#%%

date_start = input('조회 시작일을 입력해주세요 (예 : 2021-01-01) : ')
if date_start == '':
    date_start = '2018-01-01'

date_end = input('조회 종료일을 입력해주세요 (예 : 2021-12-31) : ')
if date_end == '':
    date_end = '2019-12-31'

driver.find_element(By.LINK_TEXT, '기간 전체').click()
element = driver.find_element(By.ID, 'search_start_date')
element.send_keys('%s' % date_start)
time.sleep(0.5)
element.send_keys(Keys.TAB + '%s' % date_end )
time.sleep(0.1)
driver.find_element(By.LINK_TEXT, '적용').click()

#%%

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
cnt = soup.find('em', 'search_number').text
cnt = cnt.replace(",", "").replace('건','')
cnt = int(cnt)

collect_cnt = int(input('몇 건의 데이터를 수집하시겠습니까? : '))

if collect_cnt > cnt :
    collect_cnt = cnt

#%%

data_url = [] 
pgnum = 1 

while len(data_url) < collect_cnt :

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find('div', 'content').find_all('div', 'list_search_post')

    for i in content :
        data_1 = i.find('a' , 'desc_inner')['href']
        data_url.append(data_1)

    pgnum += 1
    if pgnum == '10' :
        driver.find_element(By.XPATH, '//*[@id="content"]/section/div[3]/a[2]').click()
    else :
        driver.find_element(By.XPATH, '//*[@id="content"]/section/div[3]/span[%d]/a' % pgnum).click()
    
    
#%%
# 검색할 정보량 입력


# %% 자료 수집할 블로그 URL 정리



         # 주소 저장용
data_url_s = []        # 네이버 블로그 확인용
data_url_cnt = 0        # 수집한 주소 갯수

# URL 수집
for craw_data_1 in content_1:
    data_1 = craw_data_1.find('div', 'total_area').find(
        'a', 'total_dsc')['href']
    data_url_s = data_1.split('/')

    if data_url_s[2] == 'blog.naver.com':
        data_url.append(data_1)
        data_url_cnt += 1

    if data_url_cnt >= collect_cnt:
        break
    else:
        continue

#%% 데이터의 저장

naver_tit = []          # 게시글 제목 저장
naver_date = []
naver_body = []         # 게시글 내용 저장

f = open(ft_name, 'a', encoding="UTF-8")

for i in tqdm(range(collect_cnt)):
    url_2 = data_url[i]
    driver.get(url_2)
    time.sleep(2)
    try:
        driver.maximize_window()
    except:
        time.sleep(0.1)

    driver.switch_to.frame('mainFrame')
    html_2 = driver.page_source
    soup_2 = BeautifulSoup(html_2, 'html.parser')

    blog_type_1 = soup_2.find_all('div', 'se-viewer se-theme-default')
    blog_type_2 = soup_2.select('#postViewArea')
    blog_type_3 = soup_2.select(
        'div[class="se_component_wrap sect_dsc __se_component_area"]')

    if blog_type_1:

        # 제목
        naver_tit_1 = soup_2.find('div', 'se-viewer se-theme-default').find(
            'div', 'se-module se-module-text se-title-text').get_text().replace('\n', '')
        naver_tit.append(naver_tit_1)

        # 작성일자
        naver_date_1 = soup_2.select(
            "div.blog2_container > span.se_publishDate.pcol2")
        try:
            naver_date_1 = naver_date_1[0].get_text()
        except IndexError:
            naver_date_1 = ' '
        naver_date.append(naver_date_1)

        # 본문
        naver_body_1 = soup_2.find('div', 'se-main-container')
        naver_body_1 = naver_body_1.text.replace("\n", "")
        naver_body.append(naver_body_1)

        # 텍스트 저장
        f.write('\n'+'1. 제목 : ' + naver_tit_1)
        f.write('\n'+'2. URL 주소 : ' + url_2)
        f.write('\n'+'3. 날짜 : ' + naver_date_1)
        f.write("\n"+"4. 내용 : " + naver_body_1)
        f.write("\n")

    elif blog_type_2:

        # 제목
        naver_tit_1 = soup_2.find('div', 'htitle').find(
            'span').get_text().replace('\n', '')
        naver_tit.append(naver_tit_1)

        # 작성일자
        naver_date_1 = soup_2.select('p[class="date fil5 pcol2 _postAddDate"]')
        try:
            naver_date_1 = naver_date_1[0].get_text()
        except IndexError:
            naver_date_1 = ' '
        naver_date.append(naver_date_1)

        # 본문
        for i in blog_type_2:
            naver_body_1 = i.text.replace("\n", "")
            naver_body.append(naver_body_1)

        f.write('\n'+'1. 제목 : ' + naver_tit_1)
        f.write('\n' + '2. URL 주소 : ' + url_2)
        f.write("\n" + "3.날짜:" + naver_date_1)
        f.write("\n" + "4.블로그 내용:" + naver_body_1)
        f.write("\n")

    elif blog_type_3:

        # 제목
        naver_tit_1 = soup_2.find(
            'h3', 'se_textarea').get_text().replace('\n', '')
        naver_tit.append(naver_tit_1)

        # 작성일자
        naver_date_1 = soup_2.select(
            "div.blog2_container > span.se_publishDate.pcol2")
        try:
            naver_date_1 = naver_date_1[0].get_text()
        except IndexError:
            naver_date_1 = ' '
        naver_date.append(naver_date_1)

        # 본문
        for i in blog_type_3:
            naver_body_1 = i.text.replace("\n", "")
            naver_body.append(naver_body_1)

        f.write('\n'+'1. 제목 : ' + naver_tit_1)
        f.write('\n' + '2. URL 주소 : ' + url_2)
        f.write("\n" + "3.날짜:" + naver_date_1)
        f.write("\n" + "4.블로그 내용:" + naver_body_1)
        f.write("\n")


#%%

df = pd.DataFrame()
df['제목'] = pd.Series(naver_tit)
df['주소'] = pd.Series(data_url)
df['날짜'] = pd.Series(naver_date)
df['내용'] = pd.Series(naver_body)

df.to_excel(fx_name, index=False, encoding="utf-8", engine='openpyxl')
df.to_csv(fc_name, index=False, encoding="utf-8-sig")

print("=" * 100)
print('요청하신 데이터 수집 작업이 정상적으로 완료되었습니다')
print("=" * 100)

# %%
