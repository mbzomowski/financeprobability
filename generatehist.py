import yfinance as yf
import matplotlib.pyplot as plt

STARTING_YEAR = 2014
END_YEAR = 2019

# This list can be adjusted to include whatever securities are needed
tickers = ['AMZN']

# Downloads daily historical data for all securities, 2015-2020
data = yf.download(
    tickers,
    start=str(STARTING_YEAR)+'-01-01',
    end=str(END_YEAR)+'-01-10',
    period='1d',
    threading=True)

# We will only use the adjusted close prices, as I believe they account for splits
daily_price = data['Adj Close']

mean_security_returns = []
yearly_security_returns = []

monthly_returns = []
for year in range(STARTING_YEAR, END_YEAR):
    for month in range(1, 13):
        start = daily_price[str(year)+'-'+str(month).zfill(2)].iloc[0]
        if month == 12:
            end = daily_price[str(year+1)+'-01'].iloc[0]
        else:
            end = daily_price[str(year)+'-'+str(month+1).zfill(2)].iloc[0]
        monthly_returns.append((end-start)/start)

fig = plt.figure()
ax1 = fig.add_axes([0.1,0.1,0.8,0.8])
monthly_returns.plot.hist(bins=60)
plt.show()
