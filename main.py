#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dataProcessing
import promptNgenAI 


# In[9]:


import requests
import pandas as pd


# In[3]:


BSUrl = "https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap07_O_bd"

BSResponse = requests.get(BSUrl)
a = BSResponse.json()
BSdf = pd.DataFrame(a)


# In[4]:


ISurl = "https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap06_O_bdA"

ISresponse = requests.get(ISurl)
b = ISresponse.json()
ISdf = pd.DataFrame(b)


# In[5]:


fields_IS = ["公司代號", "公司名稱", "收益", "營業利益", "稅前淨利（淨損）", "本期淨利（淨損）", "所得稅費用（利益）",  "本期綜合損益總額", "基本每股盈餘（元）"]
fields_BS = ["公司代號", "流動資產", "流動負債", "負債總計", "每股參考淨值", "保留盈餘（或累積虧損）"]
companyList = []
result_IS = []
result_BS = []
companyNumber = int(input("enter the number you'd like to look up: "))

for i in range(companyNumber):
    id = input("enter the companuy id you'd like to look up: ")
    companyList.append(id)

for id in companyList:
    filteredIS = dataProcessing.getData(ISdf, id, fields_IS)
    filteredBS = dataProcessing.getData(BSdf, id, fields_BS)
    
    finalIS = dataProcessing.listAdding(filteredIS, result_IS)
    finalBS = dataProcessing.listAdding(filteredBS, result_BS)

finaldf = pd.merge(finalIS, BSdf, on="公司代號", how="inner")

# finaldf.to_csv("final_result_1.csv", index=False, encoding="utf-8-sig")


# In[6]:


dataStr = promptNgenAI.dataReader("final_result_1.csv")
report = promptNgenAI.aiAdvisor(dataStr)
print(report)


# In[7]:


convo = promptNgenAI.getHistory()
print(convo)


# In[8]:


prompting = """
你是一位專業的投資顧問，專注於低頻交易策略。
請根據以下財務數據，為投資者設計合適的低頻交易策略：
1. 價值投資策略：根據「營收」、「本期淨利」、「基本每股盈餘（EPS）」等數據，評估是否有低估的股票適合長期持有。
2. 動量交易策略：如果某些公司連續幾季「營收」或「淨利潤」增長，請標記出來，作為潛在的投資標的。
3. 低波動選股策略：挑選「基本每股盈餘」和「本期淨利」較穩定的公司，適合低風險投資者持有。

請提供你的分析結果，包括：
- 你認為值得關注的公司及其指標
- 該公司適用的策略（價值投資、動量交易、低波動選股）
- 具體的投資建議

以下是最新的財務數據：
"""

newPrompt = promptNgenAI.promptImprovement(prompting, 3)
print(newPrompt)

