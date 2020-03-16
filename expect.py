# R = Sum_{i = 1}^{n} W_i R_i
# R = Expected return of entire portfolio
# W_i = Weight associated with security i
# R_i = The expected return for security i
# n = The total number of different securities in the portfolio

# Return of Portfolio = Sum(W_1 R_1 + W_2 R_2 + ... + W_n R_n)
# Where
# W_1 = weight of 1st security in the portfolio
# R_1 = expected return of the 1st security.
# NOTE : THE SUMMATION OF THE WEIGHTS SHOULD ADD TO 1


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

# pull 3 random stocks from ticker list to create a mock portfolio
# You can mess around with the number of stocks 

my_port = random.sample(tickers, 3) 

data = pd.DataFrame()

for item in my_port:
    data[item] = web.DataReader(item, data_source='yahoo', start='25-02-2019')['Adj Close']

# daily returns 
ds_returns = data.pct_change() 

# annualize daily data (multiply by 250 - since there are 250 trading days in a year) 
ann_returns = ds_returns.mean() * 250. 

# create weights 
w = np.random.random(3) # since we have 3 random stocks in our mockfolio 
w = w /sum(w) #In order to normalize weights - remember the sum must equal 1! 

assert sum(w) == 1, "Weights are not normalized!" 

myport_exp_returns = np.sum(w * ann_returns) 

print(myport_exp_returns) 
