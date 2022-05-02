#%%

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time, os, math, sys, re, csv, getpass
import urllib.request
import urllib
from tqdm.notebook import tqdm
import win32com.client as win32   
import win32api

def scroll_down(driver):
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    time.sleep(3)

#%%
# 저장할 파일명 설정

time_local = time.localtime()
time_name = ('%d.%d.%d_' %(time_local.tm_year, time_local.tm_mon, time_local.tm_mday))

name = input('결과를 저장할 파일 명을 쓰세요 : ') # 저장할 파일명

ft_name = (time_name + name + 'NB' +'.txt')
fc_name = (time_name + name + 'NB' +'.csv')
fx_name = (time_name + name + 'NB' +'.xls')

# 저장할 경로 설정 (바탕화면)
username = getpass.getuser()    # getpass 모듈로 username 불러오기
username = 'yzz07'
save_location = 'C:\\Users\\' + username + '\\Desktop'
save_name = save_location + '\\' +'DATA'

if os.path.exists(save_name) == False:
    os.mkdir(save_name)
    os.chdir(save_name)
else:
    os.chdir(save_name)

#%%

s = Service("C:/Users/yzz07/Desktop/PROGRAMMING/chromedriver.exe")
driver = webdriver.Chrome(service=s)
query_txt = "국내 관광" # 검색할 키워드

url = 'https://www.naver.com/'
driver.get(url)
time.sleep(2)
driver.maximize_window()

driver.find_element(By.ID, 'query').click()
element = driver.find_element(By.ID, 'query')
element.send_keys('%s' % query_txt)
element.send_keys('\n')
time.sleep(2)

driver.find_element(By.LINK_TEXT, 'VIEW').click()
driver.find_element(By.LINK_TEXT, '블로그').click()

day_start = input('조회 시작일을 입력해주세요 (예 : 2021-01-01) : ')
print('\n')
day_end = input('조회 종료일을 입력해주세요 (예 : 2021-12-31) : ')
print('\n')
day_s = day_start.split('-')
day_e = day_end.split('-')

time.sleep(1)
driver.find_element(By.LINK_TEXT, '옵션').click()
time.sleep(1)
driver.find_element(
    By.XPATH, '//*[@id="snb"]/div[2]/ul/li[3]/div/div[1]/a[9]').click()

driver.find_element(
    By.XPATH, '//*[@id="snb"]/div[2]/ul/li[3]/div/div[2]/div[1]/span[1]/a').click()
driver.find_element(By.LINK_TEXT, '%s' % day_s[0]).click()
driver.find_element(
    By.XPATH, '//*[@id="snb"]/div[2]/ul/li[3]/div/div[2]/div[2]/div[2]/div/div/div/ul/li[%s]/a' % day_s[1]).click()
driver.find_element(
    By.XPATH, '//*[@id="snb"]/div[2]/ul/li[3]/div/div[2]/div[2]/div[3]/div/div/div/ul/li[%s]/a' % day_s[2]).click()

driver.find_element(
    By.XPATH, '//*[@id="snb"]/div[2]/ul/li[3]/div/div[2]/div[1]/span[3]/a').click()
driver.find_element(By.LINK_TEXT, '%s' % day_e[0]).click()
driver.find_element(
    By.XPATH, '//*[@id="snb"]/div[2]/ul/li[3]/div/div[2]/div[2]/div[2]/div/div/div/ul/li[%s]/a' % day_e[1]).click()
driver.find_element(
    By.XPATH, '//*[@id="snb"]/div[2]/ul/li[3]/div/div[2]/div[2]/div[3]/div/div/div/ul/li[%s]/a' % day_e[2]).click()

driver.find_element(
    By.XPATH, '//*[@id="snb"]/div[2]/ul/li[3]/div/div[2]/div[3]/button').click()

#%%

# 검색할 정보량 입력
collect_cnt = int(input('3. 몇 건의 데이터를 수집하시겠습니까? : '))

# 네이버에서는 한번에 최대 1000개까지밖에 안됨
collect_page_cnt = math.ceil(collect_cnt / 1000)
scroll_cnt = math.ceil(collect_cnt/30)+1    # 스크롤을 몇번 돌릴지

scroll_num = 0   # 스크롤 내리기
while scroll_num < scroll_cnt:
    scroll_down(driver)
    scroll_num += 1

# %% 자료 수집할 블로그 URL 정리

html_1 = driver.page_source
soup_1 = BeautifulSoup(html_1, 'html.parser')
content_1 = soup_1.find('ul', 'lst_total').find_all('li')

data_url = []          # 주소 저장용
data_url_s = []        # 네이버 블로그 확인용
data_url_cnt = 0        # 수집한 주소 갯수
data_num = []          # 데이터 번호 저장
data_nick = []         # 작성자 닉네임 저장
data_tit = []          # 게시글 제목 저장
data_body = []         # 게시글 내용 저장

for craw_data_1 in content_1:
    data_1 = craw_data_1.find('div', 'total_area').find('a', 'total_dsc')['href']
    data_url_s = data_1.split('/')

    if data_url_s[2] == 'blog.naver.com':
        data_url.append(data_1)
        data_url_cnt += 1

    if data_url_cnt >= collect_cnt:
        break
    else:
        continue

# %% 데이터의 저장

f = open(ft_name, 'a', encoding="UTF-8")
cnt_work = 1

for i in range(collect_cnt) :
    url_2 = data_url[i]
    driver.get(url_2)
    time.sleep(2)
    driver.maximize_window()

    driver.switch_to.frame('mainFrame')
    html_2 = driver.page_source
    soup_2 = BeautifulSoup(html_2, 'html.parser')

    blog_type_1 = soup_2.find_all('div', 'se-viewer se-theme-default')
    blog_type_2 = 1
    blog_type_3 = 2

    if blog_type_1:

        print('0. 번호 : %s ' % cnt_work)

        # 제목 저장
        data_tit_1 = soup_2.find('div', 'se-viewer se-theme-default').find(
            'div', 'se-module se-module-text se-title-text').get_text().replace('\n', '')
        data_tit.append(data_tit_1)
        print('1. 제목 : ' + data_tit_1)
        f.write('\n'+'1. 제목 : ' + data_tit_1)

        # 주소 저장
        print("2. URL 주소 : " + data_url[i])
        f.write('\n'+'2. URL 주소 : ' + data_url[i])

        # 작성자 이름
        data_nick_1 = soup_2.find(
            'div', 'se-viewer se-theme-default').find('span', 'nick').get_text()
        data_nick.append(data_nick_1)
        print("3. 작성자 : " + data_nick_1)
        f.write("\n"+"3. 작성자 : " + data_nick_1)

        # 내용 저장
        data_body_1 = soup_2.find('div', 'se-main-container')
        data_body_2 = data_body_1.text.replace("\n", "")
        data_body.append(data_body_2)
        print("4. 내용 : " + data_body_2)
        f.write("\n"+"4. 내용 : " + data_body_2)
        f.write("\n")

    elif blog_type_2:
        print('아직 준비 안됨')

    else:
        print("알 수 없는 방식")

    # 함수 변경
    cnt_work += 1
    i += 1
    print('\n')

print('\n')

df = pd.DataFrame()
df['번호'] = data_num
df['제목'] = pd.Series(data_tit)
df['주소'] = pd.Series(data_url)
df['작성자'] = pd.Series(data_nick)
df['내용'] = pd.Series(data_body)

df.to_excel(fx_name, index=False, encoding="utf-8", engine='openpyxl')
df.to_csv(fc_name, index=False, encoding="utf-8-sig")

#%%


#%%
# 저장할 파일명 설정

time_local = time.localtime()
time_name = ('%d.%d.%d_' %(time_local.tm_year, time_local.tm_mon, time_local.tm_mday))

name = input('결과를 저장할 파일 명을 쓰세요 : ') # 저장할 파일명

ft_name = (time_name + name + 'YB' + '.txt')
fc_name = (time_name + name + 'YB' + '.csv')
fx_name = (time_name + name + 'YB' + '.xls')

# 저장할 경로 설정 (바탕화면)
username = getpass.getuser()    # getpass 모듈로 username 불러오기
username = 'yzz07'
save_location = 'C:\\Users\\' + username + '\\Desktop'
save_name = save_location + '\\' +'DATA'

if os.path.exists(save_name) == False:
    os.mkdir(save_name)
    os.chdir(save_name)
else:
    os.chdir(save_name)

#%%

s = Service("C:/Users/yzz07/Desktop/PROGRAMMING/chromedriver.exe")
driver = webdriver.Chrome(service=s)
query_txt = "국내여행 vlog" # 검색할 키워드

url = 'https://www.youtube.com/'
driver.get(url)
time.sleep(2)
driver.maximize_window()

Yday_start = "after:" + day_start
Yday_end = "before:" + day_end
query_txt = query_txt + " " + Yday_start + " " + Yday_end

#%%

driver.find_element(By.NAME, 'search_query').click()
element = driver.find_element(By.NAME, 'search_query')
element.send_keys('%s' % query_txt)
element.send_keys('\n')
time.sleep(2)


i = 1

print('영상을 불러오는 중 입니다.')

while i < collect_page_cnt :
    scroll_down(driver)
    i += 1

print('영상 불러오기가 완료 되었습니다.')


#%%

html_1 = driver.page_source
soup_1 = BeautifulSoup(html_1, 'html.parser')
content_1 = soup_1.find('div', 'style-scope ytd-search').find_all('ytd-video-renderer')

#%% 자료 수집할 URL 정리

data_url = []
data_url_cnt = 0 

for craw_data_1 in content_1:
    data_1 = craw_data_1.find('a', 'yt-simple-endpoint style-scope ytd-video-renderer')['href']
    data_url_s = data_1.split('/')
    data_1 = "https://www.youtube.com/" + data_1
    data_url.append(data_1)
    data_url_cnt += 1

    if data_url_cnt >= collect_cnt:
        break

