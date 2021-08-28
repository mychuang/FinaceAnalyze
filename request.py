#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 08:43:21 2021

@author: miller
"""

import requests
import pandas as pd
from datetime import datetime
dateFormatter = "%Y/%m/%d"
threldTime = datetime.strptime("2007-01-01", "%Y-%m-%d")

#獲取上市股票資訊
res = requests.get(\
    "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&chklike=Y")
    
dfMark = pd.read_html(res.text)[0]
dfMark = dfMark.drop([0, 1, 4, 5, 8, 9],axis = 1)

dfMark.columns = dfMark.iloc[0]
dfMark = dfMark.iloc[1:]

for i in dfMark.index:
    dfMark['公開發行/上市(櫃)/發行日'][i] = datetime.strptime(dfMark['公開發行/上市(櫃)/發行日'][i], dateFormatter)

dfMark = dfMark[dfMark['公開發行/上市(櫃)/發行日'] <= threldTime]

#%%
#獲取上櫃股票資訊
res = requests.get(\
    "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=2&issuetype=4&industry_code=&Page=1&chklike=Y")
    
dfCont = pd.read_html(res.text)[0]
dfCont = dfCont.drop([0, 1, 4, 5, 8, 9],axis = 1)

dfCont.columns = dfCont.iloc[0]
dfCont = dfCont.iloc[1:]


for i in dfCont.index:
    dfCont['公開發行/上市(櫃)/發行日'][i] = datetime.strptime(dfCont['公開發行/上市(櫃)/發行日'][i], dateFormatter)

dfCont = dfCont[dfCont['公開發行/上市(櫃)/發行日'] <= threldTime]
#%%
#獲取上市ETF
res = requests.get(\
    "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=I&industry_code=&Page=1&chklike=Y")
    
dfETF = pd.read_html(res.text)[0]
dfETF = dfETF.drop([0, 1, 4, 5, 8, 9],axis = 1)

dfETF.columns = dfETF.iloc[0]
dfETF = dfETF.iloc[1:]


for i in dfETF.index:
    dfETF['公開發行/上市(櫃)/發行日'][i] = datetime.strptime(dfETF['公開發行/上市(櫃)/發行日'][i], dateFormatter)

dfETF = dfETF[dfETF['公開發行/上市(櫃)/發行日'] <= threldTime]



