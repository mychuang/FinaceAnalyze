#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  8 08:08:24 2021

@author: miller
"""

class StrategyStar:
        
    def EveningStarSignal(stockData):
#---Evening star: 3-k strategy, impliy short signal 
#1k: big red-k, should higher than avg
#2k: small-k, should close 25% Percentile
#3k: big green-k, should higher than half of 1k (~58%)
        import numpy as np
        import pandas as pd 
        
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