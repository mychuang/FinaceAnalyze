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
        
        
        
        
        
        
        