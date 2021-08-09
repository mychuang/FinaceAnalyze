#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 20:56:41 2021

@author: miller
"""

## ==========================================
# 取得股價
from FinMind.data import DataLoader

# creare crawl function
def stockCrawl(stockID, start, end):
    dl = DataLoader()
    # 下載台股股價資料
    stockData = dl.taiwan_stock_daily(
             stock_id=stockID, start_date=start, end_date=end)
    if(len(stockData) == 0):
        return False
    else:
        # 下載三大法人資料
        stockData = dl.feature.add_kline_institutional_investors(stockData)
        # 下載融資券資料
        stockData = dl.feature.add_kline_margin_purchase_short_sale(stockData)
        return stockData 
    
stockId = '0050'
bigin   = '2011-08-06'
end     = '2021-08-06'
stockData = stockCrawl(stockId, bigin, end)


#%%
import pandas as pd 
stockData.index = pd.DatetimeIndex(stockData['date'])
stockData = stockData.drop(['date'], axis = 1)

df_adj = stockData.iloc[:, 3:7]
seriesVol = stockData['Trading_Volume']
df_adj = pd.concat([df_adj, seriesVol], axis=1)
df_adj.columns = ['Open','High','Low','Close','Volume']
#df_adj.columns = ['Open','High','Low','Close']
df_adj.index.name = 'Date'

#%%
# import mplfinance as mpf
# #mpf.plot(df_adj, type='candle')
# mpf.plot(df_adj, type='candle',mav=(20, 40, 60), volume=True)

#%%
import numpy as np
def EveningStarSignal(stockData):
#---Evening star: 3-k strategy, impliy short signal 
#1k: big red-k, should higher than avg
#2k: small-k, should close 25% Percentile
#3k: big green-k, should higher than half of 1k (~58%)
    dailyChg = stockData['close'] - stockData['open']
    positiveChg = np.array([])
    nagetiveChg = np.array([])
    
    #get spread
    for i in range(len(dailyChg)):
        if(dailyChg[i] > 0):
            positiveChg = np.append(positiveChg, dailyChg[i])
        elif(dailyChg[i] < 0):
            nagetiveChg = np.append(nagetiveChg, dailyChg[i])
    meanPositive = positiveChg.mean()
    
    #catch condition 1 of Evening star
    # [i-2]: big 'red' K
    # [i-1]: small k
    # [i]  : midian 'black' k, midian means the spread greater than 0.5[i-2]k
    evenningStarCond1 = np.array([False, False]) #from 3rd day record
    for i in range(2, len(dailyChg)):
        if(dailyChg[i-2] > 0.25*meanPositive and \
          abs(dailyChg[i-1]) < abs(dailyChg.quantile([0.25])[0.25]) and \
          dailyChg[i] < 0):
            evenningStarCond1 = np.append(evenningStarCond1, [True])
        else:
            evenningStarCond1 = np.append(evenningStarCond1, [False])
            
    #catch condition 2 of Evening star
    evenningStarCond2 = np.array([False, False]) #from 3rd day record
    for i in range(2, len(dailyChg)):
        if(stockData['open'][i-1] > stockData['close'][i-2] and \
          stockData['open'][i-1] > stockData['open'][i]    and \
          stockData['close'][i-1] > stockData['close'][i-2] and \
          stockData['close'][i-1] > stockData['open'][i]):
            evenningStarCond2 = np.append(evenningStarCond2, [True])
        else:
            evenningStarCond2 = np.append(evenningStarCond2, [False])
    
    #get signal
    evenningStarSig = np.array([])
    for i in range(len(evenningStarCond1)):
        if(evenningStarCond1[i] == True and evenningStarCond2[i] == True):
            evenningStarSig = np.append(evenningStarSig, [True])
        else:
            evenningStarSig = np.append(evenningStarSig, [False])
            
    #check message
    for i in range(len(evenningStarSig)):
        if(evenningStarSig[i]):
            print("evening star appear: ",dailyChg.index[i])
    
    sig = pd.Series(index=stockData.index, data= evenningStarSig)
    return sig

def MorningStarSignal(stockData):
#---Morining star: 3-k strategy, impliy short signal 
#1k: big green-k, should lower than avg
#2k: small-k, should close 25% Percentile
#3k: big red-k, should higher than half of 1k (~58%)
    dailyChg = stockData['close'] - stockData['open']
    positiveChg = np.array([])
    nagetiveChg = np.array([])
    
    #get spread
    for i in range(len(dailyChg)):
        if(dailyChg[i] > 0):
            positiveChg = np.append(positiveChg, dailyChg[i])
        elif(dailyChg[i] < 0):
            nagetiveChg = np.append(nagetiveChg, dailyChg[i])
    meanNagetive = nagetiveChg.mean()
    
    #catch condition 1 of Morning star
    # [i-2]: big 'green' K
    # [i-1]: small k
    # [i]  : midian 'red' k, midian means the spread greater than 0.5[i-2]k
    morningStarCond1 = np.array([False, False]) #from 3rd day record
    for i in range(2, len(dailyChg)):
        if(dailyChg[i-2] < 0.25*meanNagetive and \
          abs(dailyChg[i-1]) < abs(dailyChg.quantile([0.25])[0.25]) and \
          dailyChg[i] > 0):
            morningStarCond1 = np.append(morningStarCond1, [True])
        else:
            morningStarCond1 = np.append(morningStarCond1, [False])
            
    #catch condition 2 of Evening star
    morningStarCond2 = np.array([False, False]) #from 3rd day record
    for i in range(2, len(dailyChg)):
        if(stockData['open'][i-1] < stockData['close'][i-2] and \
          stockData['open'][i-1] < stockData['open'][i]    and \
          stockData['close'][i-1] < stockData['close'][i-2] and \
          stockData['close'][i-1] < stockData['open'][i]):
            morningStarCond2 = np.append(morningStarCond2, [True])
        else:
            morningStarCond2 = np.append(morningStarCond2, [False])
    
    #get signal
    morningStarSig = np.array([])
    for i in range(len(morningStarCond1)):
        if(morningStarCond1[i] == True and morningStarCond2[i] == True):
            morningStarSig = np.append(morningStarSig, [True])
        else:
            morningStarSig = np.append(morningStarSig, [False])
            
    #check message
    for i in range(len(morningStarSig)):
        if(morningStarSig[i]):
            print("morning star appear: ",dailyChg.index[i])
    
    sig = pd.Series(index=stockData.index, data= morningStarSig)
    return sig

sellSignal = EveningStarSignal(stockData)
buySignal  = MorningStarSignal(stockData)

#%%
# import mplfinance as mpf
# df_adj_star = df_adj['2019-7']
# mpf.plot(df_adj_star, type='candle',mav=(3, 5, 10), volume=True, \
#          style='blueskies', title='5347')
    
#%%
# === backtrading ===  
intAssset   = 1000000

handleMoney = np.zeros(len(df_adj))
handleStock = np.zeros(len(df_adj));
handleAsset = np.zeros(len(df_adj));
handleMoney[0] = intAssset; handleMoney[1] = intAssset
handleAsset[0] = intAssset; handleAsset[1] = intAssset

buyStock  = np.zeros(len(df_adj))
sellStock = np.zeros(len(df_adj))

moneyVar = 0;
stockVar = 0; 
assetVar = 0;

for i in range(2, len(df_adj)):
    currentOpen = df_adj['Open'][i]
    if(buySignal[i]):
        if(handleMoney[i-1] >= df_adj['Open'][i]*1000):
            buyStock[i] = 1000
            print(df_adj.index[i], " 買進 1 張 ",currentOpen)
        else:
            buyStock[i] = 0
    
    if(sellSignal[i]):
        if(handleStock[i-1] >= 1000):
            sellStock[i] = 1000
            #sellStock[i] = handleStock[i-1] #clean position
            print(df_adj.index[i], " 賣出 1 張 ",currentOpen)
            #print(df_adj.index[i], " 賣出", int(handleStock[i-1]/1000) ,"張 ",currentOpen)
        else:
            sellStock[i] = 0
            
    stockVar       = handleStock[i-1] + buyStock[i] - sellStock[i]
    handleStock[i] = stockVar
    
    moneyVar       = handleMoney[i-1] + stockData['open'][i]*(sellStock[i]-buyStock[i])
    handleMoney[i] = moneyVar
    
    assetVar       = handleStock[i]*stockData['open'][i] + handleMoney[i]
    handleAsset[i] = assetVar
    
    stockVar=0; moneyVar=0; assetVar=0

handleAsset    = (handleAsset/intAssset) - 1
#handleAsset    = np.around(handleAsset, decimals=2)

#%%    
# import matplotlib.pyplot as plt
# import matplotlib.ticker as ticker

# fig = plt.figure(figsize=(16,12)) #create figure
# ax = fig.add_subplot(1, 1, 1) #create ax within figure
# ax.plot(df_adj.index, handleAsset, color='red',label='close')

# ax.xaxis.set_major_locator(ticker.MultipleLocator(160)) #set xTicks interval 
# ax.xaxis.set_tick_params(rotation=20,labelsize=16,colors='g') #setting xticks
# ax.yaxis.set_tick_params(labelsize=16,colors='b') #setting xticks
# ax.minorticks_on()

# ax.grid(which='minor', axis='both')
# ax.set_title(stockId + ' Back Trade Testing',fontsize=24)
# ax.set_ylabel('Return', fontsize='x-large',fontstyle='oblique')

#%%
#compare with handle 0050

stockId = '0050'
stockCTL = stockCrawl(stockId, bigin, end)

import math
def AassetChange(money, currentStockValue, numOfStock):
    totalAsset = money + numOfStock*(currentStockValue*1000)
    return totalAsset

setAsset = 1000000 #initial asset
#in initial time, we can buy how much stock?
numStock = math.floor(setAsset / (stockCTL['open'][0]*1000))
#in initial time, we still have how much money?
money = setAsset - numStock*(stockCTL['open'][0]*1000)
#track the (a share of )stock varius
trackMoneyStand = (AassetChange(money, stockCTL['open'], numStock)/setAsset)-1

#%%

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

fig = plt.figure(figsize=(16,12)) #create figure
ax = fig.add_subplot(1, 1, 1) #create ax within figure
ax.plot(df_adj.index, handleAsset, color='red',label='Star trade')
ax.plot(df_adj.index, trackMoneyStand, color='black',label='CTL')


ax.xaxis.set_major_locator(ticker.MultipleLocator(160)) #set xTicks interval 
ax.xaxis.set_tick_params(rotation=20,labelsize=16,colors='g') #setting xticks
ax.yaxis.set_tick_params(labelsize=16,colors='b') #setting xticks
ax.minorticks_on()

ax.grid(which='minor', axis='both')
ax.set_title(stockId + ' Back Trade Testing',fontsize=24)
ax.set_ylabel('Return', fontsize='x-large',fontstyle='oblique')

ax.legend(fontsize=16)










