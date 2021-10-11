#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 11:50:09 2021

@author: miller
"""

import os
import pandas as pd
import numpy as np

#%% reading ETF data

filePath = os.getcwd()+"/ETF/"
stockDic = {}
dicKeys = np.array([])

with open(filePath+'log','r') as fh:
    linelist = fh.readlines()
    #strip()去除換行字元(\n)和空白字元
    for i in range(len(linelist)):
        linelist[i] = linelist[i].strip()
        print('reading file: ', linelist[i])
        stock = pd.read_csv(filePath + linelist[i])
        stock.index = pd.DatetimeIndex(stock['date'])
        stock = stock.drop(['date'], axis = 1)
        stockDic.setdefault(linelist[i], stock)
        dicKeys = np.append(dicKeys, linelist[i])
#%% sort data to 0050 
# data clean -> add [i-1]

Col = stockDic['0050.csv'].columns
extractCtlIndex = stockDic['0050.csv'].index
lenCtl = len(extractCtlIndex)
#%%
import numpy as np
for dicIndex in range(1,6):
    # Get the single stock from Dic
    exp = stockDic[dicKeys[dicIndex]]
    extractExpIndex = exp.index
    lenExp = len(extractExpIndex)
    insertPos = 0
    
    # Process the data length to fit 0050
    while(len(extractCtlIndex) > len(extractExpIndex)):
        for i in range(len(extractExpIndex)):
            if(extractExpIndex[i] != extractCtlIndex[i]):
                print(dicKeys[dicIndex], "disapear date", extractCtlIndex[i])
                insertPos = i
                break
        
        indexAbove = extractExpIndex[:insertPos]
        if(len(indexAbove) > 0):
            getAbove = exp[ indexAbove[0] : indexAbove[insertPos-1]]
            
        indexBelow = extractExpIndex[insertPos:]
        getBelow = exp[indexBelow[0] : indexBelow[len(indexBelow)-1]]

        insertRow = pd.Series({ 
                             Col[0]: exp['stock_id'][0],
                             Col[1]:  np.nan, 
                             Col[2]:  np.nan,
                             Col[3]:  np.nan,
                             Col[4]:  np.nan,
                             Col[5]:  np.nan,
                             Col[6]:  np.nan,
                             Col[7]:  np.nan,
                             Col[8]:  np.nan,
                             Col[9]:  np.nan, 
                             Col[10]: np.nan,
                             Col[11]: np.nan,
                             Col[12]: np.nan                                                                                        
                           }, name = extractCtlIndex[insertPos])
        if(len(indexAbove) > 0):
            exp = getAbove.append(pd.DataFrame(insertRow).T).append(getBelow)
        else:
            insert = pd.DataFrame(insertRow).T
            exp = insert.append(getBelow)
    
        extractExpIndex = exp.index   
        lenExp = len(extractExpIndex) #update for while loop statement
    stockDic[dicKeys[dicIndex]] = exp

#%% follow weighting index
# 台灣50, MSCI, 高股息, fh富時不動產, 美元, 美債
#['0050', '0055', '0056', '00712', '00682U', '00679B']
# 65% 0056; 10% 00712; 20% 00679B; 5% 00682U 
# 
stockVar   = stockDic['0056.csv']  ; wstock    = 0.65
estimateVar= stockDic['00712.csv'] ; westimate = 0.1
moneyVar   = stockDic['00682U.csv']; wmoney    = 0.05
bondVar    = stockDic['00679B.csv']; wbond     = 0.2

for i in range(len(stockVar)-1):
    if(np.isnan(stockVar['open'][i])):
        stockVar['open'][i] = stockVar['open'][i+1]
    if(np.isnan(estimateVar['open'][i])):
        estimateVar['open'][i] = estimateVar['open'][i+1]
    if(np.isnan(moneyVar['open'][i]) or moneyVar['open'][i] == 0):
        moneyVar['open'][i] = moneyVar['open'][i-1]
    if(np.isnan(bondVar['open'][i])):
        bondVar['open'][i] = bondVar['open'][i+1]

weightIndex = stockVar['open'] * wstock + \
              estimateVar['open'] * westimate + \
              bondVar['open'] * wbond + \
              moneyVar['open'] * wmoney
#%%
weightIndex = weightIndex / weightIndex[0]
ctlVar      = stockDic['0050.csv']
ctlIndex    = ctlVar['open']/  ctlVar['open'][0]

stockIndex   = stockVar['open']/ stockVar['open'][0]   
estimatIndex = estimateVar['open']/ estimateVar['open'][0] 
moneyIndex   = moneyVar['open']/ moneyVar['open'][0]
bondIndex    = bondVar['open']/ bondVar['open'][0]

#%% plot

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

#plot close
fig = plt.figure(figsize=(16,12)) #create figure
ax = fig.add_subplot(2, 1, 1) #create ax within figure

ax.plot(ctlIndex, color='dimgray', label='0050')
ax.plot(weightIndex, color='red', label='Muti')

ax.xaxis.set_major_locator(ticker.MultipleLocator(80)) #set xTicks interval
ax.axes.xaxis.set_ticklabels([]) #hide xTicks 
#ax.xaxis.set_tick_params(rotation=20,labelsize=16,colors='g') #setting xticks
ax.yaxis.set_tick_params(labelsize=16,colors='b') #setting xticks
ax.minorticks_on()

ax.grid(which='minor', axis='both')
ax.set_title('Back trading',fontsize=18)
ax.set_ylabel('profit', fontsize='x-large',fontstyle='oblique')
ax.legend(fontsize=16)
#========================
ax2 = fig.add_subplot(2, 1, 2) #create ax within figure

ax2.plot(stockIndex, color='darkorange', label='0056')
ax2.plot(estimatIndex, color='darkgoldenrod', label='00712')
ax2.plot(moneyIndex, color='thistle', label='00682U')
ax2.plot(bondIndex, color='steelblue', label='00679B')

ax2.xaxis.set_major_locator(ticker.MultipleLocator(80)) #set xTicks interval 
ax2.xaxis.set_tick_params(rotation=20,labelsize=16,colors='g') #setting xticks
ax2.yaxis.set_tick_params(labelsize=16,colors='b') #setting xticks
ax2.minorticks_on()

ax2.grid(which='minor', axis='both')
ax2.set_title('Raw data',fontsize=18)
ax2.set_ylabel('profit', fontsize='x-large',fontstyle='oblique')
ax2.legend(fontsize=16)









