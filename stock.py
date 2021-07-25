#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 14:41:04 2021

@author: miller
"""

# 取得股價
from FinMind.data import DataLoader

dl = DataLoader()
# 下載台股股價資料
stockData = dl.taiwan_stock_daily(
    stock_id='2330', start_date='2020-07-01', end_date='2021-07-24'
)
# 下載三大法人資料
stockData = dl.feature.add_kline_institutional_investors(
    stockData
) 
# 下載融資券資料
stockData = dl.feature.add_kline_margin_purchase_short_sale(
    stockData
)

#%%
import pandas as pd
#data process
#[1] foreignPurchase nalmalize
pd1 = (stockData['Foreign_Investor_diff'] / stockData['Foreign_Investor_diff'].sum())*(-1.)
pd2 = (stockData['Foreign_Investor_diff'] / stockData['Foreign_Investor_diff'].sum())*(-1.)
foreignPurchase = pd.concat([pd1, pd2], axis=1)
foreignPurchase.columns = ['buy','sell']

for i in foreignPurchase.index:
    if(foreignPurchase['sell'][i] > 0):
        foreignPurchase['sell'][i] = 0
    if(foreignPurchase['buy'][i] < 0):
        foreignPurchase['buy'][i] = 0



#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

#plot close
#fig, ax = plt.subplots(figsize=(16,8))
fig = plt.figure(figsize=(16,8)) #create figure
ax = fig.add_subplot(2, 1, 1) #create ax within figure

ax.plot(stockData['date'], stockData['close'], color='red',label='close')

ax2 = ax.twinx()
ax2.bar(stockData['date'], stockData['Trading_Volume'], color='black')

ax.xaxis.set_major_locator(ticker.MultipleLocator(10)) #set xTicks interval 
ax.axes.xaxis.set_ticklabels([]) #hide xTicks
ax.minorticks_on()

ax.grid(which='minor', axis='both')
ax.set_title('2330 daily-K',fontsize=18)
ax.set_ylabel('stock proce', fontsize='x-large',fontstyle='oblique')
ax.legend(fontsize=16)
#-----------------------

#plot Foreign_Investor_diff
ax3 = fig.add_subplot(2, 1, 2) #create ax within figure
ax3.bar(stockData['date'], foreignPurchase['buy'], color='red')
ax3.bar(stockData['date'], foreignPurchase['sell'], color='blue')

ax3.xaxis.set_major_locator(ticker.MultipleLocator(10)) #set xTicks interval
ax3.xaxis.set_tick_params(rotation=45,labelsize=10,colors='g') #setting xticks
ax3.set_title('2330 Foreign Investor Normallize Diff',fontsize=18)
ax3.set_xlabel('date', fontsize=18,fontfamily = 'sans-serif',fontstyle='italic')
ax3.set_ylabel('Normallize value', fontsize='x-large',fontstyle='oblique')
















