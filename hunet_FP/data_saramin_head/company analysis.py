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

df = pd.read_csv('C:\\Users\\yzz07\\Desktop\\git\\Hunet\\hunet_FP\\data_saramin_head\\고객상담·TM_2022.6.10_saramin_head.csv')
sf = df['company']
sf = list(set(sf))

Services = Service("C:/Users/yzz07/Desktop/PROGRAMMING/chromedriver.exe")
driver = webdriver.Chrome(service=Services)
today = datetime.datetime.today()

name = 'saramin_head'  # 저장할 파일명
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

기업업종 = []
기업형태 = []
기업명 = []

for i in sf :
    url = 'https://www.saramin.co.kr/zf_user/company-search'
    driver.get(url)
    time.sleep(2)

    driver.find_element(By.XPATH, '//*[@id="tab_section_keyword"]').click()
    driver.find_element(By.XPATH, '//*[@id="total_ipt_keyword"]').click()
    element = driver.find_element(By.XPATH, '//*[@id="total_ipt_keyword"]')
    a = i.replace('(주)', '').replace('㈜', '').replace('(유)', '').replace('유한회사', '').replace('주식회사', '')
    time.sleep(2)
    for j in a :
        element.send_keys(j)
        time.sleep(0.1)
    element.send_keys('\n')
    
    try :
        time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        content = soup.find('div', 'text_info').find_all('span')

        기업명.append(i)
        기업업종.append(content[0].text)
        기업형태.append(content[1].text)

    except :
        print('찾지 못하였습니다.', a)
        기업명.append(i)
        기업업종.append('-')
        기업형태.append('-')

df = pd.DataFrame()
df['기업명'] = pd.Series(기업명)
df['기업업종'] = pd.Series(기업업종)
df['기업형태'] = pd.Series(기업형태)

fc_name = ('기업정보' + '_' + time_name + name + '.csv')
df.to_csv(fc_name, index=False, encoding="utf-8-sig")

print('-' * 50)

print('작업이 완료되었습니다.')
# %%
