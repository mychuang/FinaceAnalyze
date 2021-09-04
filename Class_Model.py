#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 16:00:20 2021

@author: miller
"""

class BackSimulate:
    def __init__(self, intAssset, stockData):
        import numpy as np
        self.intAsset    = intAssset
        self.stockData   = stockData
        self.__handleMoney = np.zeros(len(stockData))
        self.__handleStock = np.zeros(len(stockData))
        self.__handleAsset = np.zeros(len(stockData))
        self.__handleMoney[0] = intAssset 
        self.__handleMoney[1] = intAssset
        self.__handleAsset[0] = intAssset
        self.__handleAsset[1] = intAssset
        self.__buyStock  = np.zeros(len(stockData))
        self.__sellStock = np.zeros(len(stockData))
        self.__fee = 0.001425 #買賣手續費 0.1425%
        self.__tax = 0.003 #賣出時繳稅 0.3 %

        
    def Simulate(self, signal):
        
        moneyVar = 0;
        stockVar = 0; 
        assetVar = 0;
        
        for i in range(2, len(self.stockData)):
        
            currentOpen = self.stockData['open'][i]            
            if(signal[i] == 1):
                if(self.__handleMoney[i-1] >= self.stockData['open'][i]):
                    self.__buyStock[i] = 1000
                    print(self.stockData.index[i], " 買進 1 張 ",currentOpen)
                else:
                    self.__buyStock[i] = 0    
            elif(signal[i] == -1):
                if(self.__handleStock[i-1] >= 1000):
                    self.__sellStock[i] = 1000
                    print(self.stockData.index[i], " 賣出 1 張 ",currentOpen)
                else:
                    self.__sellStock[i] = 0
                                        
            
            stockVar       = self.__handleStock[i-1] + \
                             self.__buyStock[i] - self.__sellStock[i]
            self.__handleStock[i] = stockVar                 
    
            moneyVar       = self.__handleMoney[i-1] + \
                self.stockData['open'][i]*(self.__sellStock[i]-self.__buyStock[i]) - \
                self.stockData['open'][i]*(self.__sellStock[i]-self.__buyStock[i])*self.__tax - \
               (self.stockData['open'][i]*(self.__sellStock[i]-self.__buyStock[i])*self.__fee)*2
                
            self.__handleMoney[i] = moneyVar
            
            assetVar       = self.__handleStock[i]*self.stockData['open'][i] + \
                             self.__handleMoney[i]
            self.__handleAsset[i] = assetVar
    
            stockVar=0; moneyVar=0; assetVar=0
            #print(self.handleAsset)
            
        self.__handleAsset    = (self.__handleAsset/self.intAsset)
        
        
        return self.__handleAsset