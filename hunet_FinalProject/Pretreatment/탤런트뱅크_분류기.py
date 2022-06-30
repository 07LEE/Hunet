# %%
import numpy as np
import pandas as pd
import os, datetime, re, getpass
from tqdm import tqdm
from konlpy.tag import Okt
okt = Okt()
import getpass

# %%
dic = {
        '경영전략/신사업': ['신규', '사업', 'BD', '경영', '경영기획', '영기획', '경영전략', '관리', '경영혁신', 'PI', 'M&A', 'PM'],
       '영업/구매/유통': ['B2B', 'B2C', '무역', '구매', '물류', '유통', 'CS', '해외'],
       '인사/총무': ['인사', '총무', '교육', '노무'],
       '재무/투자': ['재무', '회계', '자금', '원가', '관리', '투자', 'IPO', '세무'],
       '마케팅': ['브랜딩', '마케팅', '상품', '기획', '홍보', 'PR'],
       '엔지니어링': ['연구', '연구개발', '개발', '생산', '제조', '공장', '품질', '안전'],
       'IT': ['IT', 'PM', '서비스', 'GUI', '앱', 'UX', 'UI', '빅데이터', 'AI', '시스템', ' 엔지니어', '딥러닝', ''],
       '법무/대정부': ['정부', '지원', '특허', '일반', '법무'],
       '디자인/패션': ['제안서', '편집', '디자인', '광고', '영상', '공간', '디자인']
       }

dic_sub = {'전문가': '전문가', '제안': '전문가'}

new_morse = {}
for k, v in dic.items():
    for i in range(0, len(v)) :
        new_morse[v[i]] = k

dic_score = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# %% 
username = getpass.getuser()
file_format = '.csv' #  .xlsx
file_path = f'C:\\Users\\{username}\\Desktop\\git\\Hunet\\\hunet_FinalProject\\data'
file_list = [f'{file}' for file in os.listdir(file_path) if file_format in file]
os.chdir(file_path)
print(file_list)
# %%
df = pd.read_csv('탤런트뱅크_프로젝트.csv')
df
# %%
a = df['expert']
okt_list = []
ddic = []

# %%
for i in range(0, len(a)) :
    pos = okt.morphs(a[i])
    okt_list.append(pos)

# %%
ddic = []
for i in range(0, len(a)):
    ddic.append('Other')
# %%
for i in range(0, len(a)) :
    for j in range(0, len(okt_list[i])) :
        if okt_list[i][j] in new_morse :
            ddic[i] = new_morse.get(okt_list[i][j])
            break
        elif okt_list[i][j] in dic_sub :
            ddic[i] = '전문가'

# %%
ddic

# %%
for i in range(0, len(a)) :
    for j in range(0, len(okt_list[i])) :
        if okt_list[i][j] in dic_sub :
            if ddic[i] == 'Other' :
                ddic[i] = new_morse.get(okt_list[i][j])
            break


# %%
df['make'] = ddic
df.to_csv('분류기.csv',  index=False, encoding="utf-8-sig")
# %%