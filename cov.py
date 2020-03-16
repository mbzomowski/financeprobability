import numpy as np
import bs4 as bs
import pickle
import requests
import pandas as pd
from pandas_datareader import data as web
import random

# Imports ticker names - not my own code, if used probably should be written, but OK for example

def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)

    with open("sp500tickers.pickle","wb") as f:
        pickle.dump(tickers,f)

    return tickers

tickers = save_sp500_tickers()
tickers = [s.rstrip() for s in tickers]

# pull 2 random stocks from ticker list to create a mock portfolio
# You can mess around with the number of stocks

#my_port = random.sample(tickers, 2)

my_port = ['WHR', 'CTAS']

data = pd.DataFrame()

for item in my_port:
    data[item] = web.DataReader(item, data_source='yahoo', start='17-02-2020')['Adj Close']

# daily returns
ds_returns = data.pct_change()

# calculate average return for each stock 
s_mean = ds_returns.mean()

# calculate the covariance 
# sum (R_1 - Avg_1) * (R_2 - Avg_2) / (Sample Size - 1.) 
# Where 
# R_1 = Return on stock 1 
# Avg_1 = Average return on stock 1 
# R_2 = Return on stock 2 
# Avg_2 = Average return on stock 2 
# This needs to be modified if you have more than two securities in your portfolio! Think about how to do this. 
ds_returns.columns[0:]

ret_arr = ds_returns.as_matrix(columns=ds_returns.columns[0:]) # Might want to modify this line... looks like it's depreciated 

# Get rid of NaN row 
ret_arr = np.delete(ret_arr, (0),axis=0) 

cov = 0 
for row in ret_arr: 
    cov += (row[0] - ds_returns.mean()[0]) * (row[1] - ds_returns.mean()[1]) 

cov / (ret_arr.shape[0] - 1.) 

print(cov) 
