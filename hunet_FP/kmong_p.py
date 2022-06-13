# %%
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time, math, os, random, urllib, urllib.request, getpass, re, datetime

def html_num(html_num) :
    try :
        re.sub('[^0-9]', '', html_num.text)
    except :
        re.sub('[^0-9]', '', html_num)

# %%
Services = Service("C:/Users/yzz07/Desktop/PROGRAMMING/chromedriver.exe")
driver = webdriver.Chrome(service=Services)
today = datetime.datetime.today()

name = 'kmong_p'  # 저장할 폴더명
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

dic_category = {1: '디자인', 2: '마케팅', 3: '번역·통역', 4: '문서·글쓰기', 6: 'IT·프로그래밍', 7: '영상·사진·음향', 8: '비즈니스컨설팅',
                9: '운세', 10: '직무역량', 11: '주문제작', 12: '취업·입시', 13: '투잡·노하우', 14: '세무·법무·노무', 15: '취미', 16: '생활서비스', 17: '심리상담'}

for key, value in dic_category.items() :
    categorys_num = key
    categorys_name = value

    url = 'https://kmong.com/category/%s?page=1&sort=ranking_points&company=false&is_prime=true&has_portfolio=false&is_contactable=false&is_fast_reaction=false&ratings=&meta=' %key
    driver.get(url)
    time.sleep(2)

    data_main = []      # 대분류
    data_middle = []    # 중분류
    data_sub = []       # 소분류
    data_operations = []    # 작업 횟수
    data_evaluation = []  # 평가 갯수
    data_wishlist = []  # 찜
    data_STANDARD = []  # STANDARD 가격
    data_DELUXE = []    # DELUXE 가격
    data_PREMIUM = []   # PREMIUM 가격
    data_title = []     # 제목
    data_name = []      # 기업명
    data_url = []       # 링크


    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    soups = soup.find('div', 'css-1xaekgw e19f3kve0')
    num = int(soup.find('div', 'css-qzjq2k e19f3kve6').find_all('li','css-w119tg etp7mg1')[-2].text)
    time.sleep(1)

    for j in range(2, num+2):
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        soups = soup.find('div', 'css-1xaekgw e19f3kve0')
        content = soups.find_all('article', 'css-0 e19f3kve2')
        data_main_ = soup.find('section', 'css-1t1ny2y e11lta390').find_all('a', 'css-mz86x3 e11lta392')[1].text
        
        for i in content:
            data_url_ = i.find('a', 'css-j9gtx5 eu87mqk0')['href']
            data_url_ = 'https://kmong.com' + data_url_
            data_title_ = i.find('h3', 'css-10894jy eu87mqk7').text
            data_evaluation_ = i.find('div', 'css-0 eu87mqk15').text
            data_evaluation_ = html_num(data_evaluation_)
            data_name_ = i.find('span', 'css-3eiwm9 eu87mqk6').text

            data_url.append(data_url_)  # URL
            data_main.append(data_main_)  # 대분류
            data_title.append(data_title_)  # 제목
            data_evaluation.append(data_evaluation_)  # 평가 건수
            data_name.append(data_name_)  # 기업명

        driver.find_element(By.XPATH, '//*[@id="__next"]/div[3]/div/div/main/div/div[2]/div[2]/ul/li[%s]/button/span' %j).click()
        time.sleep(1)

    time.sleep(3)

    for pages in data_url :
        driver.get(pages)
        time.sleep(1)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        content = soup.find('div', 'css-533jkm el1ngz10')

        price_1 = content.find('section', 'css-16df71f e12i9j8n0')
        price_2 = content.find('div', 'css-1it4gjn ea0crmh2')
        
        if price_1 :
            price = content.find('section', 'css-16df71f e12i9j8n0').find_all('div', 'css-d0415h e12i9j8n1')
            data_STANDARD_ = html_num(price[0])
            data_DELUXE_ =  html_num(price[1])
            data_PREMIUM_ = html_num(price[2])

        elif price_2:
            price = content.find('div', 'css-1it4gjn ea0crmh2')
            data_STANDARD_ = html_num(price)
            data_DELUXE_ =  '가격 없음'
            data_PREMIUM_ = '가격 없음'

        data_wishlist_ = html_num(content.find('section', 'css-29iuxd e1stf3gr4').find('span', 'css-1oteowz eklkj753'))
        data_operations_ = html_num(content.find('span', 'css-8ioq0m ec3naz84'))

        data_wishlist.append(data_wishlist_)
        data_STANDARD.append(data_STANDARD_)
        data_DELUXE.append(data_DELUXE_)
        data_PREMIUM.append(data_PREMIUM_)
        data_operations.append(data_operations_)


    df = pd.DataFrame()
    df['main'] = pd.Series(data_main)
    df['middle'] = pd.Series(data_middle)
    df['sub'] = pd.Series(data_sub)

    df['operations'] = pd.Series(data_operations)
    df['evaluation'] = pd.Series(data_evaluation)

    df['STANDARD'] = pd.Series(data_STANDARD)
    df['DELUXE'] = pd.Series(data_DELUXE)
    df['PREMIUM'] = pd.Series(data_PREMIUM)
    df['wishlist'] = pd.Series(data_wishlist)
    df['operations'] = pd.Series(data_operations)

    df['title'] = pd.Series(data_title)
    df['name'] = pd.Series(data_name)
    df['url'] = pd.Series(data_url)

    fc_name = (categorys_name + '_' + time_name + name + '.csv')
    fx_name = (categorys_name + '_' + time_name + name + '.xls')

    df.to_excel(fx_name, index=False, encoding="utf-8", engine='openpyxl')
    df.to_csv(fc_name, index=False, encoding="utf-8-sig")

print('작업이 완료되었습니다.')
# %%

