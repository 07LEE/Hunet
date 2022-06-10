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
username = getpass.getuser()    # getpass 모듈로 username 불러오기

Services = Service("C:/Users/%s/Desktop/chromedriver.exe" %username)
driver = webdriver.Chrome(service=Services)
url = 'https://www.saramin.co.kr'
driver.get(url)
time.sleep(2)
today = datetime.datetime.today()

# %% 
name = 'saramin'  # 저장할 파일명
time_local = time.localtime()
time_name = ('%d.%d.%d_' % (time_local.tm_year, time_local.tm_mon, time_local.tm_mday))

ft_name = (time_name + name + '.txt')
fc_name = (time_name + name + '.csv')
fx_name = (time_name + name + '.xls')

# 저장할 경로 설정 (바탕화면)
username = getpass.getuser()    # getpass 모듈로 username 불러오기
# username = 'yzz07'
save_location = 'C:\\Users\\' + username + '\\Desktop'
save_name = save_location + '\\' + name

if os.path.exists(save_name) == False:
    os.mkdir(save_name)
    os.chdir(save_name)
else:
    os.chdir(save_name)

# %%

url = 'https://www.saramin.co.kr/zf_user/jobs/list/job-category?cat_mcls=10&panel_type=&search_optional_item=n&search_done=y&panel_count=y'
driver.get(url)
time.sleep(2)

# %%
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
soups = soup.find('div', 'common_recruilt_list')
content = soups.find('div', 'list_body').find_all('div')

# %%
total_count = soup.find('span', 'total_count').get_text()
total_count = re.sub('[^0-9]', '', total_count)
print('수집 가능한 게시물의 갯수 : ' + total_count)
int_total_count = int(total_count)
# %% 
content2 = soups.select('div[class="list_item"]')

# %%
data_company = [] # 기업 이름
data_career = [] # 경력
data_education = [] # 학력
data_region = [] # 지역
data_deadline = [] # 마감일
data_type = [] # 고용형태
data_title = [] # 제목
data_job = [] # 직종
data_reg = [] # 공고일
data_tag = []

# %%
sum_count = 0
page_count = 0

while True :

    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find('div', 'common_recruilt_list').find_all('div', 'list_item')

    for content in content :
        data_company_ = content.find('a', 'str_tit').text
        data_company.append(data_company_) # 회사 이름


        data_education_ = content.find('p', 'education').text
        if data_education_.find('↑') : 
            data_education_ = data_education_.replace('↑', ' 이상')
        data_education.append(data_education_) # 학력


        data_career_ = content.find('p', 'career').text
        data_career.append(data_career_) # 경력


        try :
            data_region_ = content.find('p', 'work_place').text
        except :
            data_region_ = '-'
        data_region.append(data_region_) # 지역

        try :
            data_deadline_ = content.find('p', 'deadlines').text
            data_deadline_ = data_deadline_.split('(')
            data_deadline_ = datetime.datetime.strptime(data_deadline_[0], '~ %m/%d')
            data_deadline.append(data_deadline_.strftime('2022-%m-%d')) # 마감일
        except :
            data_deadline.append('채용시')

        
        data_reg_ = content.find('p', 'deadlines').find('span', 'reg_date').text
        data_reg_1 = re.sub('[^0-9]', '', data_reg_)
        data_reg_ = today - datetime.timedelta(days=int(data_reg_1))
        data_reg.append(data_reg_.strftime('%Y-%m-%d')) # 공고일


        try :
            data_type_ = content.find('p', 'employment_type').text
        except :
            data_type_ = '-'
        data_type.append(data_type_) # 고용형태


        data_title_ = content.find('div', 'job_tit').span.text
        data_title.append(data_title_) # 제목


        data_job_ = content.find('span', 'job_sector')
        data_job_s = '' # 관련 직무
        for i in data_job_ :
            data_job_s += i.text
            data_job_s += ', '
        data_job.append(data_job_s[:-2])

        data_tag_ = '서비스'
        data_tag.append(data_tag_)

        sum_count += 1
        if int_total_count < sum_count :
            break
    
    if int_total_count < sum_count :
        break

    page_count += 1

    if page_count == 12 :
        page_count = 2

    time.sleep(0.3)
    driver.find_element(By.XPATH, '//*[@id="default_list_wrap"]/div[3]/a[%s]' %page_count).click()



# %%
df = pd.DataFrame()
df['company'] = pd.Series(data_company)
df['career'] = pd.Series(data_career)
df['education'] = pd.Series(data_education)
df['region'] = pd.Series(data_region)
df['reg'] = pd.Series(data_reg)
df['deadline'] = pd.Series(data_deadline)
df['type'] = pd.Series(data_type)
df['title'] = pd.Series(data_title)
df['job'] = pd.Series(data_job)
df['tag'] = pd.Series(data_tag)

# %%
df

# %%
df.to_excel(fx_name, index=False, encoding="utf-8", engine='openpyxl')
df.to_csv(fc_name, index=False, encoding="utf-8-sig")
# %%

