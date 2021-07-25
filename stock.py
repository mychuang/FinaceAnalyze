#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 14:41:04 2021

@author: miller
"""

# 取得股價
from FinMind.data import DataLoader

dl = DataLoader()
# 下載台股股價資料
stock_data = dl.taiwan_stock_daily(
    stock_id='2330', start_date='2020-07-01', end_date='2021-07-24'
)
# 下載三大法人資料
stock_data = dl.feature.add_kline_institutional_investors(
    stock_data
) 
# 下載融資券資料
stock_data = dl.feature.add_kline_margin_purchase_short_sale(
    stock_data
)

#%%
# plot daily k-line
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

#plot open & close
fig, ax = plt.subplots(figsize=(16,8))
ax.plot(stock_data['date'], stock_data['close'], color='red',label='close')
ax.plot(stock_data['date'], stock_data['open'], color='blue',label='open')
#ax.plot(stock_data .close, color='red',label='close')
#ax.plot(stock_data .open,color='green',label='open')
ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
ax.minorticks_on()



# ax.grid(which='minor', axis='both')

ax.xaxis.set_tick_params(rotation=45,labelsize=12,colors='g')  
# ax.yaxis.tick_right()

# ax.set_title('2330 daily-K',fontsize=18)
# ax.set_xlabel('date', fontsize=18,fontfamily = 'sans-serif',fontstyle='italic')
# ax.set_ylabel('stock proce', fontsize='x-large',fontstyle='oblique')
# ax.legend()
