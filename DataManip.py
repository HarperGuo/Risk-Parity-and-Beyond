# -*- coding: utf-8 -*-
"""
Created on Fri May 12 22:17:42 2017

@author: Hao Guo
"""

import datetime as dt
import numpy as np 
import pandas as pd
import pandas_datareader.data as web
from scipy.stats import mode


'''
# In[]: Data Retrieving for S&P 500 stocks
tickerdf = pd.read_csv('SandP500.csv')    
tickers = list(tickerdf['Symbol'].values) 
verbose_flag = False                      
start_date = dt.datetime(2006, 12, 31) 
end_date = dt.datetime(2017, 3, 31)     
ticker_df_list = []                                                 

for ticker in tickers: 
    try:
        r = web.DataReader(ticker, "yahoo", start=start_date, end=end_date)
        r['Ticker'] = ticker 
        ticker_df_list.append(r)
        if verbose_flag:
            print "Obtained data for ticker %s" % ticker  
    except:
        if verbose_flag:
            print "No data for ticker %s" % ticker  
# 
df = pd.concat(ticker_df_list)
cell= df[['Ticker','Adj Close']]          
cell.reset_index().sort(['Ticker', 'Date'], ascending=[1,0]).set_index('Ticker')
cell.to_pickle('close_price.pkl')
if 'cell' not in locals():
    df = pd.read_pickle('close_price.pkl')
else: 
    df = cell
    
# In[]:Data Wrangling for S&P 500 stocks

dte1 = '2006-12-31'
dte2 = '2017-03-31'
tickers = sorted(list(set(df['Ticker'].values)))                   
tkrlens = [len(df[df.Ticker==tkr][dte1:dte2]) for tkr in tickers]  
tkrmode = mode(tkrlens)[0][0]
good_tickers = [tickers[i] for i,tkr in enumerate(tkrlens) if tkrlens[i]==tkrmode]
Data = pd.DataFrame()
for tkr in good_tickers:
    tmpdf = df[df.Ticker==tkr]['Adj Close'][dte1:dte2]
    Data = pd.concat([Data, tmpdf], axis=1)
Data.columns = good_tickers
Data = Data.dropna(axis=1) 

# In[]: save the dataframe to csv
Data.to_csv('SP500.csv',sep='\t', encoding='utf-8')
'''
# In[]: load data we've wrangled
data = pd.read_csv('SP500.csv')
data.index = pd.to_datetime(data['Date'])
data = data.drop('Date',axis=1)
ret = np.log(data/data.shift(1)).dropna()
# In[]: 
#Factors= web.DataReader('F-F_Research_Data_5_Factors_2x3', 'famafrench')[0]
#quandl.get("KFRENCH/FACTORS_D")
#Factors = pd.read_csv('FamaFrench.csv')