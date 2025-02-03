#!/usr/bin/env python
# coding: utf-8

# #### Data Processing module

# In[1]:


import requests
import pandas as pd


# In[2]:


## 上櫃公司資產負債表

BSUrl = "https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap07_O_bd"

BSResponse = requests.get(BSUrl)
a = BSResponse.json()
BSdf = pd.DataFrame(a)


# In[3]:


BSdf


# In[4]:


## 上櫃公司財報資訊

ISurl = "https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap06_O_bdA"

ISresponse = requests.get(ISurl)
b = ISresponse.json()
ISdf = pd.DataFrame(b)


# In[5]:


ISdf


# In[6]:


# 輸入欲查詢公司號以及年分、時間長度
# 綜合損益表評估之指標 -> 淨利（損）歸屬於母公司業主, 基本每股盈餘（元）, 稅前淨利（淨損）, 本期其他綜合損益（稅後淨額）, 收益   ## (可以試試看寫,markdown file問要留那些數值來評估)
# 查詢 / 合併

def getData(df, company_id, fields):
    filtered_df = df[
        (df["公司代號"] == company_id)
    ]
    selected_df = filtered_df[fields]

    return selected_df

result_IS = []
result_BS = []

def listAdding(df, defaultList):
    defaultList.append(df)
    finalList = pd.concat(defaultList, ignore_index=True)
    
    return finalList


# In[7]:


fields_IS = ["公司代號", "公司名稱", "收益", "營業利益", "稅前淨利（淨損）", "本期淨利（淨損）", "所得稅費用（利益）",  "本期綜合損益總額", "基本每股盈餘（元）"]
fields_BS = ["公司代號", "流動資產", "流動負債", "負債總計", "每股參考淨值", "保留盈餘（或累積虧損）"]
companyList = []
companyNumber = int(input("enter the number you'd like to look up: "))

for i in range(companyNumber):
    id = input("enter the companuy id you'd like to look up: ")
    companyList.append(id)

for id in companyList:
    filteredIS = getData(ISdf, id, fields_IS)
    filteredBS = getData(BSdf, id, fields_BS)
    
    finalIS = listAdding(filteredIS, result_IS)
    finalBS = listAdding(filteredBS, result_BS)

finaldf = pd.merge(finalIS, BSdf, on="公司代號", how="inner")


# In[8]:


finaldf


# In[9]:


# finaldf.to_csv("final_result_1.csv", index=False, encoding="utf-8-sig")


# In[10]:


## 資料視覺化


# In[11]:


# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# from sklearn.preprocessing import MinMaxScaler
# import plotly.graph_objects as go


# In[12]:


# finaldf.set_index("公司代號", inplace=True)

# ### 法1：雷達圖（Radar Chart）

# ### 法2：標準化後的群組柱狀圖




