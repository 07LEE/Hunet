# %%
import numpy as np
import pandas as pd
import os, datetime, re, getpass
from tqdm import tqdm

file_format = '.csv' #  .xlsx
file_path = 'C:\\Users\\yzz07\\Desktop\\git\\a'
file_list = [f'{file}' for file in os.listdir(file_path) if file_format in file]
os.chdir(file_path)
print(file_list)

# %%
merge_df = pd.DataFrame()

for file_name in tqdm(file_list) :
    file_df = pd.read_csv(file_name)
    file_df = file_df.dropna()
    columns = file_df.columns 
    temp_df = pd.DataFrame(file_df, columns=columns)
    merge_df = pd.concat([merge_df, temp_df])

merge_df.to_csv('병합파일.csv',  index=False, encoding="utf-8-sig")
print('-' * 50)
print(len(merge_df))
# %%
merge_df
# %%
