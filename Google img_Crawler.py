# %% 구글 이미지 수집용 크롤러
import pandas as pd
from bs4 import BeautifulSoup
from pyrsistent import b
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
import math
import os
import random
import urllib

def scroll_down(driver):
    driver.execute_script("window.scrollBy(0,5000);")  
    time.sleep(5)

def scroll_up(driver):
    driver.execute_script("window.scrollBy(0,-500);") 
    time.sleep(2)

# %% 기본 정보 호출
print("=" * 80)
print(" '구글 이미지' 수집용 웹크롤러입니다.")
print("=" * 80)

Services = Service("C:/Users/yzz07/Desktop/PROGRAMMING/chromedriver.exe")
driver = webdriver.Chrome(service=Services)

url = 'https://www.google.co.kr/'
driver.get(url)
time.sleep(2)
driver.maximize_window()

#%%

search_query = input('검색할 이미지 키워드를 써주세요 : ')

save_name = input('결과를 저장할 파일 명을 쓰세요 : ')
# ft_name = (save_name+'.txt')
# fc_name = (save_name+'.csv')
# fx_name = (save_name+'.xls')

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

driver.find_element(
    By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').click()
element = driver.find_element(
    By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
element.send_keys('%s' % search_query)
element.send_keys('\n')
time.sleep(2)
driver.find_element(
    By.XPATH, '//*[@id="hdtb-msb"]/div[1]/div/div[2]/a').click()

# %%

craw_img = int(input('해당 주제로 크롤링할 이미지는 몇 건입니까? : '))

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
content = soup.find('div', 'mJxzWe')
cnt_get = content.find_all('div','isv-r PNCib MSM1fd BUooTd')

while len(cnt_get) < craw_img :
    
    scroll_down(driver)
    save_img = len(cnt_get)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find('div', 'islrc')
    cnt_get = content.find_all('div','isv-r PNCib MSM1fd BUooTd')

    print('지금까지 %s 건의 이미지를 불러왔습니다.' %len(cnt_get))
    load_img = len(cnt_get)

    if save_img == load_img :
        try :
            driver.find_element(By.XPATH, ' //*[@id="islmp"]/div/div/div/div[1]/div[2]/div[2]/input').click()
            load_img += 1
        except :
            print('이미지를 더 이상 불러올 수 없습니다. 모든 이미지를 불러왔습니다.')
            break

# %%

file_nom = 1
img_src2 = [ ]

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
imgs = driver.find_elements(By.TAG_NAME,'img')

for img in imgs:
    img_src1=img.get_attribute('src')
    img_src2.append(img_src1)

for i in range(2,len(img_src2)+1) :
    try :
            urllib.request.urlretrieve(img_src2[i],str(file_nom)+'.jpg')
    except TypeError:
            continue
            
    time.sleep(1)
    file_nom += 1

    if file_nom == craw_img :
        break
        
print('작업이 완료되었습니다.')

driver.close( )