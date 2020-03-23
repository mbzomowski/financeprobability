import yfinance as yf

STARTING_YEAR = 2015
END_YEAR = 2020

# This list can be adjusted to include whatever securities are needed
tickers = ['AMZN', 'KO', 'CMG']

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

for sym in tickers:
    yearly_returns = []
    for year in range(STARTING_YEAR, END_YEAR):
        # Calculate the pct change for each year
        current_year_start = daily_price[sym][str(year)].iloc[0]
        next_year_start = daily_price[sym][str(year+1)].iloc[0]
        security_return = (next_year_start - current_year_start) / current_year_start
        yearly_returns.append(security_return)

    yearly_security_returns.append(yearly_returns)

    # Weight the returns and variances for more recent years heavier than earlier years
    mean_yearly_return = sum(yearly_returns) / (END_YEAR - STARTING_YEAR)

    mean_security_returns.append(mean_yearly_return)

    # Calculate the variance of the returns
    return_variance = 0
    for ret in yearly_returns:
        return_variance += (ret - mean_yearly_return)**2
    return_variance /= (END_YEAR - STARTING_YEAR - 1)

    # Print data for each stock
    print(sym)
    print("Expected return:")
    print(mean_yearly_return)
    print("Expected variance of returns:")
    print(return_variance)
    print()

# Calculate the covariance between all combinations of securities
for i in range(len(tickers)):
    for j in range(len(tickers)):
        cov = 0
        print("Covariance between {} and {}".format(tickers[i], tickers[j]))
        for k in range(END_YEAR - STARTING_YEAR):
            cov += (yearly_security_returns[i][k] - mean_security_returns[i])\
                * (yearly_security_returns[j][k] - mean_security_returns[j])
        cov /= (END_YEAR - STARTING_YEAR - 1)
        print(cov)
