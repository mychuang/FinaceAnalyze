#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 29 09:57:11 2021

@author: miller
"""

#%%
# == psudo code ==
# 1. get stock list -> done  
# 2. get each stock info for every stock list -> done
# 3. read stock data -> done
# 3. clean data -> done
# 4. get signal
# 5. trading


#%%
# read all stock data 2012-01-01 ~ 2017-01-01
import os
import pandas as pd
import numpy as np
 
filePath = os.getcwd()+"/stockDataofMark/"
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
        if(len(stock) < 1150):
            continue
        stockDic.setdefault(linelist[i], stock)
        dicKeys = np.append(dicKeys, linelist[i])
#%%
# read 0050 as our CTL
import os
import pandas as pd

stockCtl = pd.read_csv("0050.csv")
stockCtl.index = pd.DatetimeIndex(stockCtl['date'])
stockCtl = stockCtl.drop(['date'], axis = 1)

#%%
#clean data test

# exp = stockDic['1201.csv']

# import pandas as pd
# import numpy as np
# expCol = exp.columns
# extractCtlIndex = stockCtl.index
# extractExpIndex = exp.index

# lenCtl = len(extractCtlIndex)
# lenExp = len(extractExpIndex)
# insertPos = 0
        
# while(len(extractCtlIndex) > len(extractExpIndex)):
# #if(len(extractCtlIndex) > len(extractExpIndex)):
    
#     for i in range(len(extractExpIndex)):
#         if(extractExpIndex[i] != extractCtlIndex[i]):
#             print("disapear index", extractCtlIndex[i])
#             insertPos = i
#             break
    
#     indexAbove = extractExpIndex[:insertPos]
#     getAbove = exp[ indexAbove[0] : indexAbove[insertPos-1]]
    
#     indexBelow = extractExpIndex[insertPos:]
#     getBelow = exp[indexBelow[0] : indexBelow[len(indexBelow)-1]]
    
#     insertRow = pd.Series({ 
#                             expCol[0]: exp['stock_id'][0],
#                             expCol[1]:  np.nan, 
#                             expCol[2]:  np.nan,
#                             expCol[3]:  np.nan,
#                             expCol[4]:  np.nan,
#                             expCol[5]:  np.nan,
#                             expCol[6]:  np.nan,
#                             expCol[7]:  np.nan,
#                             expCol[8]:  np.nan,
#                             expCol[9]:  np.nan, 
#                             expCol[10]: np.nan,
#                             expCol[11]: np.nan,
#                             expCol[12]: np.nan                                                                                        
#                           }, name = extractCtlIndex[insertPos])
#     exp = getAbove.append(pd.DataFrame(insertRow).T).append(getBelow)
    
#     extractExpIndex = exp.index   
#     lenExp = len(extractExpIndex) #while loop

#%%
# data clean -> add np.nan
# The ctl parameters
ctlCol = stockCtl.columns
extractCtlIndex = stockCtl.index
lenCtl = len(extractCtlIndex)

for dicIndex in range(len(dicKeys)):
#for dicIndex in range(10):
    # Get the single stock from Dic
    exp = stockDic[dicKeys[dicIndex]]
    extractExpIndex = exp.index
    lenExp = len(extractExpIndex)
    insertPos = 0
    
    # Process the data length to fit Ctl
    while(len(extractCtlIndex) > len(extractExpIndex)):
        for i in range(len(extractExpIndex)):
            if(extractExpIndex[i] != extractCtlIndex[i]):
                print(dicKeys[dicIndex], "disapear date", extractCtlIndex[i])
                insertPos = i
                break
        indexAbove = extractExpIndex[:insertPos]
        getAbove = exp[ indexAbove[0] : indexAbove[insertPos-1]]    
        indexBelow = extractExpIndex[insertPos:]
        getBelow = exp[indexBelow[0] : indexBelow[len(indexBelow)-1]]
        
        insertRow = pd.Series({ 
                             ctlCol[0]: exp['stock_id'][0],
                             ctlCol[1]:  np.nan, 
                             ctlCol[2]:  np.nan,
                             ctlCol[3]:  np.nan,
                             ctlCol[4]:  np.nan,
                             ctlCol[5]:  np.nan,
                             ctlCol[6]:  np.nan,
                             ctlCol[7]:  np.nan,
                             ctlCol[8]:  np.nan,
                             ctlCol[9]:  np.nan, 
                             ctlCol[10]: np.nan,
                             ctlCol[11]: np.nan,
                             ctlCol[12]: np.nan                                                                                        
                           }, name = extractCtlIndex[insertPos])
        exp = getAbove.append(pd.DataFrame(insertRow).T).append(getBelow)
    
        extractExpIndex = exp.index   
        lenExp = len(extractExpIndex) #update for while loop statement
    stockDic[dicKeys[dicIndex]] = exp
        
    












