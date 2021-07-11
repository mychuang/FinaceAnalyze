#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 14:41:04 2021

@author: miller
"""

import requests
import pandas as pd

date = 20210201
stockNo = '0056'


def stockCrawler(date, stockNo):
    urlTemplete = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date={}&stockNo={}"    
    url = urlTemplete.format(date, stockNo)
    
    file_name = "{}_{}.csv".format(stockNo, date)
    data = pd.read_html(requests.get(url).text)[0]
    data.columns = data.columns.droplevel(0)
    data.to_csv(file_name, index=False)    
    return data
##

import datetime

for i in range(1,12):
    print(i)

stockNo = '0056'
stockData = stockCrawler(20100101, stockNo)

dataLoop = stockCrawler(20100201, stockNo)
#stockData = pd.concat([data,dataLoop])
dataLoop = stockCrawler(20100301, stockNo)
#data.append(dataLoop)

