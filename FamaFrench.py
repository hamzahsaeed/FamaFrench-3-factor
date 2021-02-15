# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 23:40:21 2021

@author: Hamzah
"""
import yfinance as yf
import xlsxwriter
import matplotlib.pyplot as plt
import pandas as pd
import xlrd
import os
import numpy as np
import scipy
import random
import itertools
import datetime
from datetime import date
import seaborn as seabornInstance 
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import statsmodels.api as sm
#%matplotlib inline


# Directory for files
os.chdir(r"C:\Users\Hamzah\Documents\Python files")
wb = xlrd.open_workbook(r'C:\Users\Hamzah\Documents\Python files\NASDAQ_tickers.xlsx')

wb_tickers=wb.sheet_by_index(0)
N=wb_tickers.nrows
pd.set_option('display.max_columns', None)  

#Set dates
start_date="1990-01-31"
end_date="2020-12-31"

master_tickers=[]
for i in range(0,N):
    x=wb_tickers.row_values(i)[0]
    master_tickers.append(x)
#Get data for factor loadings, this is the FFM data taken from: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
data=pd.read_excel('FFM3_data.xlsx')
factor_data=pd.DataFrame()
factor_data['mkt-rf']=data['Mkt-RF']
factor_data['SMB']=data['SMB']
factor_data['HML']=data['HML']
#Get monthly data matching start and end dates
factors=factor_data[763:1134]


class FamaFrench:
    def __init__(self,ticker,factor_data,start_data,end_date,interval):
        self.ticker=ticker
        self.factor_data=factor_data
        self.start_date=start_date
        self.end_date=end_date
        self.interval=interval
    def FF3(self):
        import statsmodels.api as sm
        R=yf.download(self.ticker,self.start_date,self.end_date,interval=self.interval)
        R=R.Close
        R=R.dropna()
        p=pd.concat([self.factor_data.reset_index(),R.reset_index()],axis=1).set_index(['index','Date'])
        X=pd.DataFrame()
        X['mkt-rf']=p['mkt-rf']
        X['SMB']=p['SMB']
        X['HML']=p['HML']
        Y=p['Close']
        X=sm.add_constant(X)
        model = sm.OLS(Y.astype(float), X.astype(float)).fit()
        predictions = model.predict(X)
        results=model.summary()
        parameters= pd.read_html(model.summary().tables[1].as_html(),header=0,index_col=0)[0]
        return results, parameters
    
        
        
            

