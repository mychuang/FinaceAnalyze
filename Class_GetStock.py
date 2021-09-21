#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 12:03:59 2021

@author: miller
"""
        
class SingleStock:
    def __init__(self, stockID, startTime, endTime):
        self.stockID = stockID
        self.startTime = startTime
        self.endTime = endTime
        
    def stockCrawl(self):
        print("id", self.stockID)
        
        from FinMind.data import DataLoader
        import pandas as pd
        
        dl = DataLoader()
        stockData = dl.taiwan_stock_daily(
             self.stockID, self.startTime, self.endTime)
        if(len(stockData) == 0):
            return False
        else:
            #下載三大法人資料
            stockData = dl.feature.add_kline_institutional_investors(stockData)
            # 下載融資券資料
            stockData = dl.feature.add_kline_margin_purchase_short_sale(stockData)
            #convert index as date
            stockData.index = pd.DatetimeIndex(stockData['date'])
            stockData = stockData.drop(['date'], axis = 1)
            return stockData
        
    def resizeTo0050(self, stockData):
        import pandas as pd
        import numpy as np
        
        self.stockID = "0050"
        stock0050 = self.stockCrawl()
        
        extractCtlIndex = stock0050.index
        print(len(extractCtlIndex))
        extractExpIndex = stockData.index
        
        insertPos = 0
        lenExp = len(extractExpIndex)
        
        while(len(extractCtlIndex) > len(extractExpIndex)):
    
            for i in range(lenExp):
                if(extractExpIndex[i] != extractCtlIndex[i]):
                    print("disapear index", extractCtlIndex[i])
                    insertPos = i
                    break
        
            indexAbove = extractExpIndex[:insertPos]
            getAbove = stockData[indexAbove[0] : indexAbove[insertPos-1]]
    
            indexBelow = extractExpIndex[insertPos:]
            getBelow = stockData[indexBelow[0] : indexBelow[len(indexBelow)-1]]
    
            insertRow = pd.Series({ "stock_id": stockData['stock_id'][0],
                                    "Trading_Volume": np.nan, 
                                    "Trading_money": np.nan,
                                    "open": np.nan,
                                    "max": np.nan,
                                    "min": np.nan,
                                    "close": np.nan,
                                    "spread": np.nan,
                                    "Trading_turnover": np.nan,
                                    "foreign_Investor_diff": np.nan, 
                                    "Investment_Trust_diff": np.nan,
                                    "Margin_Purchase_diff": np.nan,
                                    'Short_Sale_diff': np.nan                                                                                        
                                  }, 
                          name = extractCtlIndex[insertPos])
            stockData = getAbove.append(insertRow).append(getBelow)
                          
            #update   
            lenExp = len(extractExpIndex) #while loop
            extractExpIndex = stockData.index #if loop

        return stockData
        
        
        
        
        
        