#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 08:31:33 2021

@author: miller
"""

import pandas as pd
import numpy as np

# ==== case 1 : miss one index

dateCTL = ['2017-06-20', '2017-06-21', '2017-06-22', '2017-06-23', '2017-06-24']

pdCtl = pd.DataFrame(
    {
        "col1": np.random.randn(5),
        "col2": np.random.randn(5),
        "col3": np.random.randn(5)
    },
    columns=["col1", "col2", "col3"],
    index = pd.to_datetime(dateCTL)
)

dateExp = ['2017-06-20', '2017-06-21', '2017-06-23', '2017-06-24']

pdExp = pd.DataFrame(
    {
        "col1": np.random.randn(4),
        "col2": np.random.randn(4),
        "col3": np.random.randn(4)
    },
    columns=["col1", "col2", "col3"],
    index = pd.to_datetime(dateExp)
)

#%%
extractCtlIndex = pdCtl.index
extractExpIndex = pdExp.index

insertPos = 0
        
if(len(extractCtlIndex) > len(extractExpIndex)):
    
    for i in range(len(extractExpIndex)):
        if(extractExpIndex[i] != extractCtlIndex[i]):
            print("disapear index", extractCtlIndex[i])
            insertPos = i
            break
#%%
indexAbove = extractExpIndex[:insertPos]

getAbove = pdExp[indexAbove[0] : indexAbove[insertPos-1]]

indexBelow = extractExpIndex[insertPos:]

getBelow = pdExp[indexBelow[0] : indexBelow[len(indexBelow)-1] ]

#%%
#insertRow = pd.Series({ "col1": np.nan, "col2": np.nan }, 
#                      name = extractCtlIndex[insertPos])

insertRow = [np.nan, np.nan, np.nan]
data_to_append = {}
for i in range(len(pdExp.columns)):
    data_to_append[pdExp.columns[i]] = insertRow[i]

pdExp = getAbove.append(data_to_append, ignore_index=True).append(getBelow, ignore_index=True)


#%% ==== case 2 : miss 2 index
import pandas as pd
import numpy as np

dateCTL = ['2017-06-20', '2017-06-21', '2017-06-22', '2017-06-23', 
           '2017-06-24', '2017-06-25', '2017-06-26', '2017-06-27']

pdCtl = pd.DataFrame(
    {
        "col1": np.random.randn(8),
        "col2": np.random.randn(8),
        "col3": np.random.randn(8)
    },
    columns=["col1", "col2", "col3"],
    index = pd.to_datetime(dateCTL)
)

dateExp = ['2017-06-20', '2017-06-21', '2017-06-23', 
           '2017-06-24', '2017-06-26', '2017-06-27']

pdExp = pd.DataFrame(
    {
        "col1": np.random.randn(6),
        "col2": np.random.randn(6),
        "col3": np.random.randn(6)
    },
    columns=["col1", "col2", "col3"],
    index = pd.to_datetime(dateExp)
)

#%%
extractCtlIndex = pdCtl.index
extractExpIndex = pdExp.index

insertPos = 0

lenCtl = len(extractCtlIndex)
lenExp = len(extractExpIndex)

#%%

while(len(extractCtlIndex) > len(extractExpIndex)):
    
    for i in range(lenExp):
        if(extractExpIndex[i] != extractCtlIndex[i]):
            print("disapear index", extractCtlIndex[i])
            insertPos = i
            break
        
    indexAbove = extractExpIndex[:insertPos]
    getAbove = pdExp[indexAbove[0] : indexAbove[insertPos-1]]
    
    indexBelow = extractExpIndex[insertPos:]
    getBelow = pdExp[indexBelow[0] : indexBelow[len(indexBelow)-1]]
    
    insertRow = pd.Series({ "col1": np.nan, "col2": np.nan }, 
                          name = extractCtlIndex[insertPos])
    
    pdExp = getAbove.append(pd.DataFrame(insertRow).T).append(getBelow)
    
    #update   
    lenExp = len(extractExpIndex) #while loop
    extractExpIndex = pdExp.index #if loop


#%%
from Class_Request import RequestStockList

requestObj = RequestStockList("2007-01-01")

stockList = requestObj.getMarkStock()


#%%
from Class_Request import RequestStock

obj = RequestStock('2330', 2012, 6)

test = obj.getMonthlyStock();


#%%
from Class_GetStock import SingleStock
import os 
from random import randint
import time

filePath = os.getcwd()+"/stockDataofMark/"


for i in stockList.index:
    if(i > 252):
        try:
            #print("num of stock:", i)
            stockObj = SingleStock(stockList['??????????????????'][i], "2006-01-01", "2017-01-01")
            stock    = stockObj.stockCrawl()
            fileName = stockList['??????????????????'][i]+".csv"
            stock.to_csv(filePath+fileName)
            del stockObj
            time.sleep(randint(40,80))
        except:
            print("error stock:", i, stockList['??????????????????'][i])

#%%
from Class_GetStock import SingleStock
filePath = os.getcwd()+"/ETF/"

stockObj = SingleStock('01004T', "2018-01-01", "2021-01-01")
stock    = stockObj.stockCrawl()
fileName = "01004T.csv"
stock.to_csv(filePath+fileName)

#%% == Load ETF ==
#??????50, MSCI, ?????????, fh???????????????, ??????, ??????
listData = ['0050', '0055', '0056', '00712', '00682U', '00679B']
import os
import time
from Class_GetStock import SingleStock

filePath = os.getcwd()+"/ETF/"
for index in range(len(listData)):
    print('loading: ',listData[index])
    stockObj = SingleStock(listData[index], "2018-01-01", "2021-01-01")
    stock    = stockObj.stockCrawl()
    fileName = listData[index]+".csv"
    stock.to_csv(filePath+fileName)
    del stockObj
    time.sleep(10)
    
#%% == Load ETF frm ?????????
import time
from Class_Request import RequestStock
import pandas as pd

model = RequestStock('01004T', 2018, 1)
test = model.getMonthlyStock()
del model
time.sleep(10)

for year in range(2018, 2021):
    for month in range(1,13):
        model = RequestStock('01004T', year, month)
        test2 = model.getMonthlyStock()
        test = pd.concat([test, test2])
        del model
        time.sleep(12)




#%%
import os
filePath = os.getcwd()+"/ETF/"
fileName = "01004T.csv"
test.to_csv(filePath+fileName)








        


        













