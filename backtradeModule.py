#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 19:49:34 2021

@author: miller
"""

##backtrading module#
#1）Data module    : obtain, process data & simulate situation
#2）Event module   : process trading event (basic class)
#3）Strategy module: include input data & create signa (basic class)
#4）Trading module : process signal
#5）Asset module   : record asset

from FinMind.data import DataLoader
import pandas as pd  
import numpy as np
import matplotlib.pyplot as plt
from   pylab import mpl
mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False


#Input data in every timestep/timestamp
class TickData:
    def __init__(self, symbol, timestamp,last_price=0, total_volume=0):
        self.symbol = symbol
        self.timestamp = timestamp
        self.open_price = 0
        self.last_price = last_price
        self.total_volume = total_volume

# Event module
class MarketData:
    def __init__(self):
        self.__recent_ticks__ = dict()
        
    def add_last_price(self, time, symbol, price, volume):
        tick_data = TickData(symbol, time, price, volume)
        self.__recent_ticks__[symbol] = tick_data
        
    def add_open_price(self, time, symbol, price):
        tick_data = self.get_existing_tick_data(symbol, time)
        tick_data.open_price = price
        
    def get_existing_tick_data(self, symbol, time):
        if not symbol in self.__recent_ticks__:
            tick_data = TickData(symbol, time)
            self.__recent_ticks__[symbol] = tick_data
        return self.__recent_ticks__[symbol]
    
    def get_last_price(self, symbol):  
        return self.__recent_ticks__[symbol].last_price
    
    def get_open_price(self, symbol): 
        return self.__recent_ticks__[symbol].open_price
    
    def get_timestamp(self, symbol):  
        return self.__recent_ticks__[symbol].timestamp

#Data module
class MarketDataSource:
    def __init__(self):
        self.event_tick = None
        self.ticker = None
        self.autype='qfq'
        self.start, self.end = None, None
        self.md = MarketData()
        
    def start_market_simulation(self):
        dl = DataLoader()
        data = dl.taiwan_stock_daily(
               stock_id=self.ticker, start_date=self.start, end_date=self.end)
        data = dl.feature.add_kline_institutional_investors(data)
        data = dl.feature.add_kline_margin_purchase_short_sale(data)
        print(self.ticker)
        print(data.columns)
        print(self.event_tick)
        
        for time, row in data.iterrows():
            self.md.add_last_price(time, self.ticker, row["close"], row["Trading_Volume"])
            self.md.add_open_price(time, self.ticker, row["open"])
            if not self.event_tick is None:
                #print(self.event_tick)
                #self.event_tick(self.md)
                self.event_tick = None

# trade module
class Order:
    def __init__(self, timestamp, symbol, qty, is_buy,
                 is_market_order, price=0):
        self.timestamp = timestamp
        self.symbol = symbol
        self.qty = qty
        self.price = price
        self.is_buy = is_buy
        self.is_market_order = is_market_order
        self.is_filled = False
        self.filled_price = 0
        self.filled_time = None
        self.filled_qty = 0
        
class Position:
    def __init__(self):
        self.symbol = None
        self.buys, self.sells, self.net = 0, 0, 0
        self.realized_pnl = 0
        self.unrealized_pnl = 0
        self.position_value = 0
    def event_fill(self, timestamp, is_buy, qty, price):
        if is_buy:
            self.buys += qty
        else:
            self.sells += qty
        self.net = self.buys - self.sells
        changed_value = qty * price * (-1 if is_buy else 1)
        self.position_value += changed_value
        if self.net == 0:
            self.realized_pnl = self.position_value
    def update_unrealized_pnl(self, price):
        if self.net == 0:
            self.unrealized_pnl = 0
        else:
            self.unrealized_pnl = price * self.net + self.position_value
        return self.unrealized_pnl
        
# Strategy module
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
        if not self.event_sendorder is None:
            order = Order(timestamp, symbol, qty, is_buy, True)
            self.event_sendorder(order)
            
class MeanRevertingStrategy(Strategy):
    def __init__(self, symbol,
                 lookback_intervals=20,
                 buy_threshold=-1.5,
                 sell_threshold=1.5):
        Strategy.__init__(self)
        self.symbol = symbol
        self.lookback_intervals = lookback_intervals
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
        self.prices = pd.DataFrame()
        self.is_long, self.is_short = False, False
    def event_position(self, positions):
        if self.symbol in positions:
            position = positions[self.symbol]
            self.is_long = True if position.net > 0 else False
            self.is_short = True if position.net < 0 else False
    def event_tick(self, market_data):
        self.store_prices(market_data)
        if len(self.prices) < self.lookback_intervals:
            return
        signal_value = self.calculate_z_score()
        timestamp = market_data.get_timestamp(self.symbol)
        if signal_value < self.buy_threshold:
            self.on_buy_signal(timestamp)
        elif signal_value > self.sell_threshold:
            self.on_sell_signal(timestamp)
    def store_prices(self, market_data):
        timestamp = market_data.get_timestamp(self.symbol)
        self.prices.loc[timestamp, "close"] = \
            market_data.get_last_price(self.symbol)
        self.prices.loc[timestamp, "open"] = \
            market_data.get_open_price(self.symbol)
    def calculate_z_score(self):
        self.prices = self.prices[-self.lookback_intervals:]
        returns = self.prices["close"].pct_change().dropna()
        z_score = ((returns-returns.mean())/returns.std())[-1]
        return z_score
    def on_buy_signal(self, timestamp):
        if not self.is_long:
            self.send_market_order(self.symbol, 100, True, timestamp)
    def on_sell_signal(self, timestamp):
        if not self.is_short:
            self.send_market_order(self.symbol, 100, False, timestamp)
            
import datetime as dt
import pandas as pd
class Backtester:
    def __init__(self, symbol, start_date, end_date):
        self.target_symbol = symbol
        self.start_dt = start_date
        self.end_dt = end_date
        self.strategy = None
        self.unfilled_orders = []
        self.positions = dict()
        self.current_prices = None
        self.rpnl, self.upnl = pd.DataFrame(), pd.DataFrame()
        
    def get_timestamp(self):
        return self.current_prices.get_timestamp(self.target_symbol)
    
    def get_trade_date(self):
        timestamp = self.get_timestamp()
        return timestamp.strftime("%Y-%m-%d")
    
    def update_filled_position(self, symbol, qty, is_buy,price, timestamp):
        position = self.get_position(symbol)
        position.event_fill(timestamp, is_buy, qty, price)
        self.strategy.event_position(self.positions)
        self.rpnl.loc[timestamp, "rpnl"] = position.realized_pnl
        print (self.get_trade_date(), \
            "deal:", "buy" if is_buy else "sell", \
            qty, symbol, "price", price)
            
    def get_position(self, symbol):
        if symbol not in self.positions:
            position = Position()
            position.symbol = symbol
            self.positions[symbol] = position
        return self.positions[symbol]
    
    def evthandler_order(self, order):
        self.unfilled_orders.append(order)
        print (self.get_trade_date(), \
            "got CMD:", \
            "buy" if order.is_buy else "sell", order.qty, \
             order.symbol)
            
    def match_order_book(self, prices):
        if len(self.unfilled_orders) > 0:
            self.unfilled_orders = \
                [order for order in self.unfilled_orders
                 if self.is_order_unmatched(order, prices)]
                
    def is_order_unmatched(self, order, prices):
        symbol = order.symbol
        timestamp = prices.get_timestamp(symbol)
        if order.is_market_order and timestamp > order.timestamp:
            # Order is matched and filled.
            order.is_filled = True
            open_price = prices.get_open_price(symbol)
            order.filled_timestamp = timestamp
            order.filled_price = open_price
            self.update_filled_position(symbol,
                                        order.qty,
                                        order.is_buy,
                                        open_price,
                                        timestamp)
            self.strategy.event_order(order)
            return False
        return True
    
    def evthandler_tick(self, prices):
        self.current_prices = prices
        self.strategy.event_tick(prices)
        self.match_order_book(prices)
        
    def start_backtest(self):
        self.strategy = MeanRevertingStrategy(self.target_symbol)
        self.strategy.event_sendorder = self.evthandler_order
        mds = MarketDataSource()
        mds.event_tick = self.evthandler_tick
        mds.ticker = self.target_symbol
        mds.start, mds.end = self.start_dt, self.end_dt
        print(mds.start, " to ", mds.end)
        print ("Backtesting started...")
        mds.start_market_simulation()
        #print ("Completed.")
        
######
backtester = Backtester("2303",'2018-01-01','2020-03-23')
backtester.start_backtest()






        