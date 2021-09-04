#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 11:31:42 2021

@author: miller
"""

from abc import ABC, abstractmethod

class Strategy(ABC):
    
    @abstractmethod
    def signal(self):
        pass
    
class Star(Strategy):
    def signal(self, stockData):
        import numpy as np
        dailyChg = stockData['close'] - stockData['open']
        
        positiveChg = np.array([])
        nagetiveChg = np.array([])
        
        for i in range(len(dailyChg)):
            if(dailyChg[i] > 0):
                positiveChg = np.append(positiveChg, dailyChg[i])
            elif(dailyChg[i] < 0):
                nagetiveChg = np.append(nagetiveChg, dailyChg[i])
        meanPositive = positiveChg.mean()
        meanNagetive = nagetiveChg.mean()
        
        starCond1 = np.array([0, 0])
        for i in range(2, len(dailyChg)):
            if(dailyChg[i-2] > 0.25*meanPositive and \
               abs(dailyChg[i-1]) < abs(dailyChg.quantile([0.25])[0.25]) and \
               dailyChg[i] < 0):
                starCond1 = np.append(starCond1, -1)
            elif(dailyChg[i-2] < 0.25*meanNagetive and \
                 abs(dailyChg[i-1]) < abs(dailyChg.quantile([0.25])[0.25]) and \
                 dailyChg[i] > 0):
                starCond1 = np.append(starCond1, 1)
            else:
                starCond1 = np.append(starCond1, 0)
        
        starCond2 = np.array([0, 0])
        for i in range(2, len(dailyChg)):
            if(stockData['open'][i-1] > stockData['close'][i-2] and \
               stockData['open'][i-1] > stockData['open'][i]    and \
               stockData['close'][i-1] > stockData['close'][i-2] and \
               stockData['close'][i-1] > stockData['open'][i]):
                starCond2 = np.append(starCond2, -1)
            elif(stockData['open'][i-1] < stockData['close'][i-2] and \
                 stockData['open'][i-1] < stockData['open'][i]    and \
                 stockData['close'][i-1] < stockData['close'][i-2] and \
                 stockData['close'][i-1] < stockData['open'][i]):
                starCond2 = np.append(starCond2, 1)
            else:
                starCond2 = np.append(starCond2, 0)
                
        starSig = np.array([])
        for i in range(len(starCond1)):
            if(starCond1[i] == -1 and starCond2[i] == -1):
                starSig = np.append(starSig, -1)
            elif(starCond1[i] == 1 and starCond2[i] == 1):
                starSig = np.append(starSig, 1)
            else:
                starSig = np.append(starSig, 0)
        
        for i in range(len(starSig)):
           if(starSig[i] == 1):
               print("morning star appear: ",dailyChg.index[i])
           elif(starSig[i] == -1):
               print("evenning star appear: ",dailyChg.index[i])
               
        import pandas as pd
        sig = pd.Series(index=stockData.index, data= starSig)
        return sig
           
class InvestFollow(Strategy):
    def signal(self):
        #市值（百萬） < 10000
        #投信當日買賣 > 200 張
        #買入該股30天
        pass
    
    
    
        
                
                
                