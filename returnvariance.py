import yfinance as yf

# This list can be adjusted to include whatever securities are needed
tickers = ['MSFT', 'KO', 'HAL']

# Downloads daily historical data for all securities, 2015-2020
data = yf.download(tickers, start='2015-01-01', end='2020-01-10', period='1d', threading=True)

# We will only use the adjusted close prices, as I believe they account for splits
daily_price = data['Adj Close']

for sym in tickers:
    yearly_returns = []
    yearly_variance = []
    for year in range(2015, 2020):
        # Calculate the pct change for each year
        current_year_start = daily_price[sym][str(year)].iloc[0]
        next_year_start = daily_price[sym][str(year+1)].iloc[0]
        security_return = (next_year_start - current_year_start) / current_year_start
        yearly_returns.append(security_return)

        # Calculate the variance for each year
        avg_yearly_price = daily_price[sym][str(year)].mean()
        year_mean_sq_avg = daily_price[sym][str(year)].apply(lambda x: (x - avg_yearly_price)**2)
        num_trading_days = daily_price[sym][str(year)].size
        year_variance = year_mean_sq_avg.sum() / num_trading_days
        yearly_variance.append(year_variance)

    # Weight the returns and variances for more recent years heavier than earlier years
    weighted_expected_return = sum([yearly_returns[i-1] * 0.1 * i for i in range(1, 5)])
    weighted_variance = sum([yearly_variance[i-1] * 0.1 * i for i in range(1, 5)])

    # Print data for each stock
    print(sym)
    print("Expected return:")
    print(weighted_expected_return)
    print("Expected variance:")
    print(weighted_variance)
    print()
