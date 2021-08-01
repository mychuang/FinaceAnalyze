#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 31 09:06:40 2021

@author: miller
"""

## ==========================================
# Follow investment Purchase 
## ==========================================
# 取得股價
from FinMind.data import DataLoader
# creare crawl function
def stockCrawl(stockID, start, end):
    dl = DataLoader()
    # 下載台股股價資料
    stockData = dl.taiwan_stock_daily(
             stock_id=stockID, start_date=start, end_date=end)
    # 下載三大法人資料
    stockData = dl.feature.add_kline_institutional_investors(stockData)
    # 下載融資券資料
    stockData = dl.feature.add_kline_margin_purchase_short_sale(stockData)
    return stockData 

stock0050 = stockCrawl("0050", "2010-01-01", "2020-01-01")

#%% plot raw data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

#plot close
fig = plt.figure(figsize=(16,12)) #create figure
ax = fig.add_subplot(2, 1, 1) #create ax within figure

ax.plot(stock0050['date'], stock0050['close'], color='red',label='close')

ax.xaxis.set_major_locator(ticker.MultipleLocator(60)) #set xTicks interval 
#ax.xaxis.set_tick_params(rotation=45,labelsize=10,colors='g') #setting xticks
ax.axes.xaxis.set_ticklabels([]) #hide xTicks
ax.minorticks_on()

ax.grid(which='minor', axis='both')
ax.set_title('0050 daily-K',fontsize=18)
ax.set_ylabel('stock price', fontsize='x-large',fontstyle='oblique')
#ax.set_xlabel('date', fontsize=18,fontfamily = 'sans-serif',fontstyle='italic')
ax.legend(fontsize=16)

#%%
## calculate the profit
import math

setPro = 1000000 #initial asset
singleStock = stock0050['close'][0] * 1000 #one stock value (a slice)
#in initial time, we can buy how much stock?
numStock = math.floor(setPro / singleStock)
#in initial time, we still have how much money?
iniMoney = setPro - numStock*singleStock
#track the (a share of )stock varius
assetStock      = stock0050['close']*1000*numStock
trackMoneyStand = (iniMoney + assetStock)/setPro;

# == plot == 
ax2 = fig.add_subplot(2, 1, 2) #create ax within figure

ax2.plot(stock0050['date'], trackMoneyStand, color='red',label='close')

ax2.xaxis.set_major_locator(ticker.MultipleLocator(60)) #set xTicks interval 
ax2.xaxis.set_tick_params(rotation=45,labelsize=10,colors='g') #setting xticks
ax2.minorticks_on()

ax2.grid(which='minor', axis='both')
ax2.set_title('Asset varius',fontsize=18)
ax2.set_ylabel('profit', fontsize='x-large',fontstyle='oblique')
ax2.set_xlabel('date', fontsize=18,fontfamily = 'sans-serif',fontstyle='italic')
ax2.legend(fontsize=16)

























