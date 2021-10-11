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