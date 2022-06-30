# %%
import numpy as np
import pandas as pd
import os, datetime, re, getpass
from tqdm import tqdm
import getpass

# %% 
username = getpass.getuser()
file_format = '.csv' #  .xlsx
file_path = f'C:\\Users\\{username}\\Desktop\\git\\Hunet\\\hunet_FinalProject\\data'
file_list = [f'{file}' for file in os.listdir(file_path) if file_format in file]
os.chdir(file_path)
print(file_list)
df = pd.read_csv('탤런트뱅크.csv')
# %%
skill_list = list(df['data_field_'])
expert_list = list(df['name'])

# %%
user = []
skills = []

for i in range(0, len(expert_list)) :
    sl = skill_list[i].split(',')
    for j in range(0, len(sl)) :
        user.append(expert_list[i])
        skills.append(sl[j])

save_df = pd.DataFrame()
save_df['expert'] = user
save_df['skills'] = skills

# %%
fc_name = ('TB_.csv')
save_df.to_csv(fc_name, index=False, encoding="utf-8-sig")
# %%
