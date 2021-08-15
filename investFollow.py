#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 11:57:57 2021

@author: miller
"""

## ==========================================
 
from Class_checkSingleStock import SingleStock
# get stock data
stockObj = SingleStock("2303", "2018-07-01", "2021-08-12")
stock2303 = stockObj.stockCrawl()

#import pandas as pd
#df_adj    = stock2303.iloc[:, 3:7]
#seriesVol = stock2303['Trading_Volume']
#df_adj = pd.concat([df_adj, seriesVol], axis=1)
#df_adj.columns = ['Open','High','Low','Close','Volume']
#df_adj.index.name = 'Date'

#import mplfinance as mpf
#mpf.plot(df_adj, type='candle',mav=(20, 40, 60), volume=True)

#%%
from Class_checkSingleStock import InvestStrategy

invest = InvestStrategy()

buySig = invest.investBuy(stock2303)

sellSig= invest.investSell(stock2303)


#%%
from Class_checkSingleStock import BackSimulate

iniAsset = 1000000
model = BackSimulate(iniAsset, stock2303)
result = model.Simulate(buySig, sellSig)

#%%
#compare with handle 0050

stockId   = '0050'
stockObj  = SingleStock(stockId, "2018-07-01", "2021-08-12")
stock0050 = stockObj.stockCrawl()

import math
def AassetChange(money, currentStockValue, numOfStock):
    totalAsset = money + numOfStock*(currentStockValue*1000)
    return totalAsset

setAsset = 1000000 #initial asset
#in initial time, we can buy how much stock?
numStock = math.floor(setAsset / (stock0050['open'][0]*1000))
#in initial time, we still have how much money?
money = setAsset - numStock*(stock0050['open'][0]*1000)
#track the (a share of )stock varius
trackMoneyStand = (AassetChange(money, stock0050['open'], numStock)/setAsset)

#%%

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

fig = plt.figure(figsize=(16,12)) #create figure
ax = fig.add_subplot(1, 1, 1) #create ax within figure
ax.plot(stock2303.index, result, color='red',label='strategy')
ax.plot(stock2303.index, trackMoneyStand, color='black',label='CTL')

ax.xaxis.set_major_locator(ticker.MultipleLocator(160)) #set xTicks interval 
ax.xaxis.set_tick_params(rotation=20,labelsize=16,colors='g') #setting xticks
ax.yaxis.set_tick_params(labelsize=16,colors='b') #setting xticks
ax.minorticks_on()

ax.grid(which='minor', axis='both')
ax.set_title('2303' + ' Back Trade Testing',fontsize=24)
ax.set_ylabel('Return', fontsize='x-large',fontstyle='oblique')

ax.legend(fontsize=16)

