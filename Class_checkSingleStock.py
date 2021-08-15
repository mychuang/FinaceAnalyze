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
        
class Strategy:
    def __init__(self):
        self.event_sendorder = None
    def event_tick(self, market_data):
        pass
    def event_order(self, order):
        pass
    def event_position(self, positions):
        pass
    def send_market_order(self, symbol, qty, is_buy, timestamp):
        pass
    
class StarStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self)
        
    def EveningStarSignal(self, stockData):
        import numpy as np
        import pandas as pd
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
    
    def MorningStarSignal(self, stockData):
        import numpy as np
        import pandas as pd
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


class InvestStrategy(Strategy):
    
    def __init__(self):
        import numpy as np
        self.positiveChg = np.array([])
        self.nagativeChg = np.array([])
        
        
    def investBuy(self, stockData):
        import numpy as np
        import pandas as pd
        
        #get aveage positive volumn
        for i in range(len(stockData)):
            if(stockData['Investment_Trust_diff'][i] > 0):
                self.positiveChg = np.append(self.positiveChg, \
                                             stockData['Investment_Trust_diff'][i])
                    
        InvestCond = np.array([False, False]) #from 2nd day record
        for i in range(2, len(stockData)):
            
            if(stockData['Investment_Trust_diff'][i-1] > 
               self.positiveChg.mean()):
                InvestCond = np.append(InvestCond, [True])
            else:
                InvestCond = np.append(InvestCond, [False])
                
        #get signal
        InvestrSig = np.array([])
        for i in range(len(InvestCond)):
            if(InvestCond[i] == True):
                InvestrSig = np.append(InvestrSig, [True])
            else:
                InvestrSig = np.append(InvestrSig, [False])
            
        #check message
        for i in range(len(InvestrSig)):
            if(InvestrSig[i]):
                print("Investr buy: ",stockData.index[i])
        sig = pd.Series(index=stockData.index, data=InvestrSig)
        return sig
    
    def investSell(self, stockData):
        import numpy as np
        import pandas as pd
        
        #get aveage positive volumn
        for i in range(len(stockData)):
            if(stockData['Investment_Trust_diff'][i] < 0):
                self.nagativeChg = np.append(self.nagativeChg, \
                                             stockData['Investment_Trust_diff'][i])
                    
        InvestCond = np.array([False, False]) #from 2nd day record
        for i in range(2, len(stockData)):
            
            if(stockData['Investment_Trust_diff'][i-1] < 
               self.nagativeChg.mean()):
                
                InvestCond = np.append(InvestCond, [True])
            else:
                InvestCond = np.append(InvestCond, [False])
                
        #get signal
        InvestrSig = np.array([])
        for i in range(len(InvestCond)):
            if(InvestCond[i] == True):
                InvestrSig = np.append(InvestrSig, [True])
            else:
                InvestrSig = np.append(InvestrSig, [False])
            
        #check message
        for i in range(len(InvestrSig)):
            if(InvestrSig[i]):
                print("Investr Sell: ",stockData.index[i])
        sig = pd.Series(index=stockData.index, data=InvestrSig)
        
        return sig

    
class BackSimulate:
    def __init__(self, intAssset, stockData):
        import numpy as np
        self.intAsset    = intAssset
        self.stockData   = stockData
        self.handleMoney = np.zeros(len(stockData))
        self.handleStock = np.zeros(len(stockData))
        self.handleAsset = np.zeros(len(stockData))
        self.handleMoney[0] = intAssset 
        self.handleMoney[1] = intAssset
        self.handleAsset[0] = intAssset
        self.handleAsset[1] = intAssset
        self.buyStock  = np.zeros(len(stockData))
        self.sellStock = np.zeros(len(stockData))
        
    def Simulate(self, buySignal, sellSignal):
        
        moneyVar = 0;
        stockVar = 0; 
        assetVar = 0;
        
        for i in range(2, len(self.stockData)):
        
            currentOpen = self.stockData['open'][i]
            
            if(buySignal[i]):
                if(self.handleMoney[i-1] >= self.stockData['open'][i]*5000):
                    self.buyStock[i] = 5000
                    print(self.stockData.index[i], " 買進 5 張 ",currentOpen)
                else:
                    self.buyStock[i] = 0
    
            if(sellSignal[i]):
                if(self.handleStock[i-1] >= 5000):
                    self.sellStock[i] = 5000
                    #sellStock[i] = handleStock[i-1] #clean position
                    print(self.stockData.index[i], " 賣出 5 張 ",currentOpen)
                    #print(df_adj.index[i], " 賣出", int(handleStock[i-1]/1000) ,"張 ",currentOpen)
                else:
                    self.sellStock[i] = 0
            
            stockVar       = self.handleStock[i-1] + \
                             self.buyStock[i] - self.sellStock[i]
            self.handleStock[i] = stockVar                 
    
            moneyVar       = self.handleMoney[i-1] + \
                self.stockData['open'][i]*(self.sellStock[i]-self.buyStock[i])
            self.handleMoney[i] = moneyVar
            
            assetVar       = self.handleStock[i]*self.stockData['open'][i] + \
                             self.handleMoney[i]
            self.handleAsset[i] = assetVar
    
            stockVar=0; moneyVar=0; assetVar=0
            #print(self.handleAsset)
            
        self.handleAsset    = (self.handleAsset/self.intAsset)
        
        
        return self.handleAsset
        
        
        
        
        
        
        