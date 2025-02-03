#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

import google.generativeai as genai
import os
from dotenv import load_dotenv


# In[2]:


load_dotenv()
API_KEY = os.getenv("API_KEY")

genai.configure(api_key=API_KEY)
headers = {'Content-Type': 'application/json'}
model = genai.GenerativeModel('gemini-pro')


history = []

# In[3]:


def dataReader(fileName):
    df = pd.read_csv(fileName)
    df_str = df.to_string()
    return df_str


# 優化 AI 回應可以嘗試：
# 1. 加入明確的指標（e.g. 「EPS > 1.0 的股票」）
# 2. 給 AI 範例輸出（讓ai模仿）

# In[4]:

def aiAdvisor(df_str):
    global history
    
    prompting = f"""
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
    {df_str}
    """
    
    history.append({"role": "user", "content": prompting})
    
    response = model.generate_content(
        prompting,
        generation_config=genai.types.GenerationConfig(max_output_tokens=800,temperature=0.5)
    )
    
    history.append({"role": "assistant", "content": response.text})

    return response.text

def getHistory():
    return history
# In[9]:


def promptImprovement(original_prompt, score):
    
    improvement_prompt = f"""
    你是一位 Prompt Engineering 專家，以下是目前的 Prompt：
    {original_prompt}

    使用者給出的評價是 {score} 分（1-5 分，5 分為最滿意）。
    請根據該評價分數，對原先的prompt重新優化，讓它更適合財務數據分析，並解釋修改的地方。
    """
    improved_prompt = model.generate_content(improvement_prompt)
    return improved_prompt.text

