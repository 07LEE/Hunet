# %%
import numpy as np
import pandas as pd
import os, datetime, re, getpass

file_format = '.csv' #  .xlsx
file_path = 'C:\\Users\\yzz07\\Desktop\\git\\Hunet\\hunet_FP\\saramin'
file_list = [f'{file}' for file in os.listdir(file_path) if file_format in file]
os.chdir(file_path)

merge_df = pd.DataFrame()

for file_name in file_list:
    file_df = pd.read_csv(file_name)
    columns = file_df.columns            
    temp_df = pd.DataFrame(file_df, columns=columns)
        
    merge_df = pd.concat([merge_df, temp_df])

merge_df.to_csv('병합파일.csv',  index=False, encoding="utf-8-sig")
