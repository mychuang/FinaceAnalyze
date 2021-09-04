#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 29 09:57:11 2021

@author: miller
"""

from Class_Request import RequestStockList

requestObj = RequestStockList("2007-01-01")

stockList = requestObj.getMarkStock()

#%%
# == psudo code ==
# 1. get stock list -> done  
# 2. get each stock info for every stock list
# 3. clean data
# 4. get signal
# 5. trading

#%%
from Class_GetStock import SingleStock
import pandas as pd
import os 
filePath = os.getcwd()+"/stockDataofMark/"


for i in stockList.index:
    if(i>=151 and i<201):
        print("num of stock:", i)
        stockObj = SingleStock(stockList['有價證券代號'][i], "2006-01-01", "2017-01-01")
        stock    = stockObj.stockCrawl()
        
        
        fileName = stockList['有價證券代號'][i]+".csv"
        stock.to_csv(filePath+fileName)
        del stockObj
#%%
stockObj = SingleStock('1101', "2006-01-01", "2017-01-01")
stock    = stockObj.stockCrawl()


