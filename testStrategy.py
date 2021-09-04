#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 14:12:39 2021

@author: miller
"""

from Class_Stratery import Star

#%%
from Class_GetStock import SingleStock
# get stock data
stockObj = SingleStock("2303", "2018-07-01", "2021-08-12")
stock2303 = stockObj.stockCrawl()

#%%

strategy = Star()
sig = strategy.signal(stock2303)

#%%
import mplfinance as mpf
import pandas as pd
df_adj    = stock2303.iloc[:, 3:7]
seriesVol = stock2303['Trading_Volume']
df_adj = pd.concat([df_adj, seriesVol], axis=1)
df_adj.columns = ['Open','High','Low','Close','Volume']
df_adj.index.name = 'Date'

df_adj_star = df_adj['2019-7']
mpf.plot(df_adj_star, type='candle',mav=(3, 5, 10), volume=True, \
          style='blueskies', title='5347')

#mpf.plot(df_adj, type='candle',mav=(20, 40, 60), volume=True)

#%%

from Class_Model import BackSimulate

model = BackSimulate(1000000, stock2303)

result = model.Simulate(sig)

#%%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

#plot close
#fig, ax = plt.subplots(figsize=(16,8))
fig = plt.figure(figsize=(8,8)) #create figure
ax = fig.add_subplot(3, 1, 1) #create ax within figure

ax.plot(df_adj.index, result, color='red',label='close')
ax.xaxis.set_major_locator(ticker.MultipleLocator(100)) #set xTicks interval
ax.xaxis.set_tick_params(rotation=30,labelsize=8,colors='g') #setting xticks

ax.grid(which='minor', axis='both')
ax.set_title('2303 backSimulate',fontsize=18)
ax.set_ylabel('stock proce', fontsize='x-large',fontstyle='oblique')
ax.legend(fontsize=16)


