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
# 3. read stock data
# 3. clean data
# 4. get signal
# 5. trading

#%%
import os 
filePath = os.getcwd()+"/stockDataofMark/"
fileName = '1203'+'.csv'

import pandas as pd
stock = pd.read_csv(filePath+fileName)


#%%
import os
import pandas as pd
 
filePath = os.getcwd()+"/stockDataofMark/"
stockDic = {}

with open(filePath+'log','r') as fh:
    linelist = fh.readlines()
    #strip()去除換行字元(\n)和空白字元
    for i in range(len(linelist)):
        linelist[i] = linelist[i].strip()
        print('reading file: ', linelist[i])
        stock = pd.read_csv(filePath + linelist[i])
        stockDic.setdefault(linelist[i], stock)
    
#%%


















