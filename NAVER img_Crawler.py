#%%
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
ti_name = ('%d-%d-%d-%d-%d' %
           (tl.tm_year, tl.tm_mon, tl.tm_mday, tl.tm_hour, tl.tm_min))
re_name = os.getcwd()
os_name = os.getcwd() + '/' + ti_name + ' ' + save_name

if os.path.exists(os_name) == False:
    os.mkdir(os_name)
    os.chdir(os_name)
else:
    os.chdir(os_name)

url = 'https://www.naver.com/'
driver.get(url)
time.sleep(2)
driver.maximize_window()

element = driver.find_element(By.ID, 'query')

element.send_keys('%s' % search_query)
element.send_keys('\n')
time.sleep(2)

driver.find_element(By.LINK_TEXT, '이미지').click()

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

hope_img = int(input('해당 주제로 크롤링할 이미지는 몇 건입니까? : '))

all_img = soup.find(
    'section', 'sc_new sp_nimage _prs_img _imageSearchPC').find_all('div', 'thumb')

while len(all_img) < hope_img:
    old_al_img = all_img
    scroll_down(driver)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    all_img = soup.find(
        'section', 'sc_new sp_nimage _prs_img _imageSearchPC').find_all('div', 'thumb')
    time.sleep(1)

    if len(old_al_img) == len(all_img):
        print('해당 키워드의 모든 이미지를 불러왔습니다.' % len(all_img))
        hope_img = len(all_img)
        break

print('이미지를 불러왔습니다.')

file_no = 1
img_src2 = []

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
imgs = driver.find_elements(By.TAG_NAME, 'img')

for img in imgs:
    img_src1 = img.get_attribute('src')
    if 'https' in img_src1:
        img_src2.append(img_src1)

for i in range(0, len(img_src2)+1):
    try:
        urllib.request.urlretrieve(img_src2[i], str(file_no)+'.jpg')
    except TypeError:
        continue
    except IndexError:
        break

    time.sleep(1)
    print("%s 번째 이미지 저장중입니다=======" % file_no)

    if file_no == hope_img:
        break
    file_no += 1

time.sleep(0.5)
print('작업이 완료되었습니다.')
# %%
