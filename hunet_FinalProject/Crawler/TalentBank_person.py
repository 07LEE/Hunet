# %%
from cmath import e
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time, math, os, random, urllib, urllib.request, getpass, re, datetime
# %%
today = datetime.datetime.today()
name = 'TB'  # 저장할 폴더명
time_local = time.localtime()
time_name = ('%d.%d.%d_' % (time_local.tm_year,
             time_local.tm_mon, time_local.tm_mday))

username = getpass.getuser()    # getpass 모듈로 username 불러오기
save_location = 'C:\\Users\\' + username + '\\Desktop'
save_name = save_location + '\\' + name

if os.path.exists(save_name) == False:
    os.mkdir(save_name)
    os.chdir(save_name)
else:
    os.chdir(save_name)

Services = Service("C:/Users/%s/Desktop/chromedriver.exe" %username)
driver = webdriver.Chrome(service=Services)
# %%
url = 'https://www.talentbank.co.kr/common/expertSearchList'
driver.get(url)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
min_page, max_page = soup.find('button', 'btn btn-block btn-md btn-outline-secondary').text.split('/')
min_page = int(re.sub('[^0-9]', '', min_page))
max_page = int(re.sub('[^0-9]', '', max_page))

for i in range(min_page, max_page+1) :
    driver.find_element(By.XPATH, '//*[@id="searchPage"]').click()

print('불러오기 완료')
# %%
data_url = []
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
content = soup.find('ul', 'posts-list theme-a type-a variable-a posts-list-info')
contents = content.find_all('li', 'posts-item')

for contents in contents :
    data_url_ = 'https://www.talentbank.co.kr'
    data_url_ += contents.find('div', 'posts-name').find('a')['href']
    data_url.append(data_url_)

df = pd.DataFrame()
df['data_url'] = pd.Series(data_url)
fc_name = ('Url' + time_name + name + '.csv')
df.to_csv(fc_name, index=False, encoding="utf-8-sig")

fc_name = ('0url.csv')
df.to_csv(fc_name, index=False, encoding="utf-8-sig")
# %%
nums = 2
# %%
data_name = []  # 이름
data_title = []  # 제목
data_field = [] # 전문 분야
data_tag = [] # 태그
data_fieldbody = [] # 분야 내용
data_certificate = [] # 자격증
data_pay = [] # 비용

while True:
    try:
        df = pd.read_csv('%surl.csv' % nums)
        data_url = df['data_url']
        print('Number of work to be done : ', len(data_url))
        if len(data_url) == 0 :
            break

    except:
        break

    for i in range(0, len(data_url)):
        url = data_url[i]
        try:
            driver = webdriver.Chrome(service=Services)
            driver.get(url)
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            content = soup.find('div', 'local-body')
            
        except:
            print('URL where the error occurred : ', url)
            print('Number of works : ', i)
            print('-' * 50)

            if i == 0:
                break
            
            else:
                ef = pd.DataFrame()
                ef['data_url'] = data_url[i:]
                nums += 1
                ef_name = ('%surl.csv' % nums)
                ef.to_csv(ef_name, index=False, encoding="utf-8-sig")

                data_name = []  # 이름
                data_title = []  # 제목
                data_field = [] # 전문 분야
                data_tag = [] # 태그
                data_fieldbody = [] # 분야 내용
                data_certificate = [] # 자격증
                data_pay = [] # 비용
                break

        data_name_ = content.find('span', 'info-item user-name').text
        data_title_ = content.find('span', 'text').text.replace('\n', '').replace('\t', '')
        data_field_ = content.find('div', 'my-profile-detail-content search-expert-detail profile-type').find('dd').text.replace('\n', ', ')
        data_field_= data_field_[:-2]
        data_field_ = data_field_[2:]

        data_tag_ = content.find('dd', 'tag-wrap profile-admin').text.replace('\n', ', ')
        data_tag_ = data_tag_[:-2]
        data_tag_ = data_tag_[2:]

        try:
            data_fieldbody_ = content.find('div', 'text-section').text.replace('\n', '').replace('\t', '').replace('-', ' ')
        except:
            data_fieldbody_  = content.find('div', 'specialty-field-info').find('div').text.replace('\n', '').replace('\t', '')

        data_pay_ = content.find('dd', 'bailiwick money-type').text.replace('\n', '').replace('\t', '')
        data_pay_ = data_pay_.replace('₩', ' ')
    
        data_title.append(data_title_)
        data_name.append(data_name_)
        data_field.append(data_field_)
        data_tag.append(data_tag_)
        data_fieldbody.append(data_fieldbody_)
        data_pay.append(data_pay_)
        driver.close()

        df['data_title_'] = pd.Series(data_title)
        df['data_name_'] = pd.Series(data_name)
        df['data_field_'] = pd.Series(data_field)
        df['data_tag_'] = pd.Series(data_tag)
        df['data_fieldbody_'] = pd.Series(data_fieldbody)
        df['data_pay_'] = pd.Series(data_pay)

        fc_name = (time_name + name + '%s.csv' % nums)
        df.to_csv(fc_name, index=False, encoding="utf-8-sig")

print('Working is done')

# %%
