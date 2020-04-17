import yfinance as yf
import numpy as np
import pandas as pd

STARTING_YEAR = 2013
END_YEAR = 2020
TARGET = 0.015

# This list can be adjusted to include whatever securities are needed
tickers = ['TGT', 'TSLA', 'FB', 'GOOG', 'AMZN', 'AAL', 'AAPL', 'BABA', 'DAL', 'F', 'GM', 'LYFT', 'PFE', 'PG']

# Downloads daily historical data for all securities, 2015-2020
data = yf.download(
    tickers,
    start=str(STARTING_YEAR)+'-01-01',
    end=str(END_YEAR)+'-04-01',
    period='1d',
    threading=True)

# We will only use the adjusted close prices, as I believe they account for splits
daily_price = data['Adj Close']
monthly_change = daily_price.resample('M').apply(lambda x: x[0]).pct_change()

mean_security_returns = []

for sym in tickers:
    mean_security_returns.append(monthly_change[sym].mean())

cov = []
for i in range(len(tickers)):
    row = []
    for j in range(len(tickers)):
        row.append(2 * monthly_change[tickers[i]].cov(monthly_change[tickers[j]]))
    row.append(-1)
    row.append(-1 * mean_security_returns[i])
    cov.append(row)
row = [1 for i in range(len(tickers))]
row += [0, 0]
cov.append(row)
cov.append(mean_security_returns + [0, 0])

k = [0 for i in range(len(tickers))] + [1, TARGET]

A_inv = np.linalg.inv(cov)
weights = np.matmul(A_inv, k)
final = [tickers + ["lambda1", "lambda2"], weights]

print("MEAN VALUES")
print(pd.Series(mean_security_returns))
print()
print("COVARIANCE MATRIX:")
print(pd.DataFrame(cov))
print()
print("WEIGHTS")
print(pd.DataFrame(final))
