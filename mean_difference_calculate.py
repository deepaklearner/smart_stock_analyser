import yfinance as yf
import pandas as pd

#################################################################
# Top 50 Nifty stocks list updated as of Oct 11, 2021
# Pass below three values to calculate difference % between average price of stocks with current price.
# The final value is a sorted value dictionary. The best stock will be at the top having negative % value.
#################################################################
stock_names = ["BAJAJ-AUTO.NS", "TITAN.NS", "TATAMOTORS.NS", "HEROMOTOCO.NS", "EICHERMOT.NS", "ITC.NS", "SBIN.NS", "BAJAJFINSV.NS", "HINDALCO.NS", "KOTAKBANK.NS", "TATACONSUM.NS", "CIPLA.NS", "DRREDDY.NS", "RELIANCE.NS", "WIPRO.NS", "BRITANNIA.NS", "NESTLEIND.NS", "TATASTEEL.NS", "UPL.NS", "AXISBANK.NS", "JSWSTEEL.NS", "SBILIFE.NS", "NTPC.NS", "MARUTI.NS", "BAJFINANCE.NS", "HINDUNILVR.NS", "HDFC.NS", "HDFCBANK.NS", "INDUSINDBK.NS", "BPCL.NS", "SUNPHARMA.NS", "ULTRACEMCO.NS", "M&M.NS", "BHARTIARTL.NS", "SHREECEM.NS", "GRASIM.NS", "TCS.NS", "LT.NS", "IOC.NS", "POWERGRID.NS", "ASIANPAINT.NS", "ONGC.NS", "ADANIPORTS.NS", "DIVISLAB.NS", "HDFCLIFE.NS", "ICICIBANK.NS", "INFY.NS", "COALINDIA.NS", "TECHM.NS", "HCLTECH.NS"]
start_date = "2021-01-01"
end_date = "2021-10-11"
#################################################################

stock_names.sort()
# Change format to pass value of stocks in yfinance function
# stock_names_formatted
first_flag = 1
for x in stock_names:
    if first_flag == 1:
        stock_names_formatted = x
        first_flag = 0
    else:
        stock_names_formatted = stock_names_formatted + " " + x

# Passing value to yfinance function
stock_value_df = yf.download(stock_names_formatted, start=start_date, end=end_date)

# Keeping useful columns only in yfinance df
stock_names_length = len(stock_names)
df_small = stock_value_df.iloc[:, 0:stock_names_length]

# Calculate mean values in loop
displacement_value_stock_name = 0
mean_dict = {}
#stock_names.reverse()
for x in stock_names:
    #formula for calculate mean = dataframe.iloc[:, 0].mean()
    mean_value_of_stock = df_small.iloc[:,displacement_value_stock_name].mean()
    mean_dict[x] = mean_value_of_stock
    displacement_value_stock_name = displacement_value_stock_name + 1

print("Mean values:", mean_dict)

## Run a loop to find the market price of all stocks present in list and then store them in dict
# Old code
# market_price_dict = {}
# for x in stock_names:
#     stock_info = yf.Ticker(x).info
#     market_price = stock_info['regularMarketPrice']
#     market_price_dict[x]=market_price

# New faster and optimized code to calculate market value
market_stock_value_df = yf.download(tickers=stock_names_formatted,period="1d",interval="1d",
                                    auto_adjust = True,prepost = False,threads = True,proxy = None)
df_small_market_stock_value_df = market_stock_value_df.iloc[:,0:stock_names_length]

displacement_value_stock_name = 0
market_price_dict = {}

for x in stock_names:
    # mean is not actually used here as data is for just 1 day. 
    market_price_of_stock = df_small_market_stock_value_df.iloc[:, displacement_value_stock_name].mean()
    market_price_dict[x] = market_price_of_stock
    displacement_value_stock_name = displacement_value_stock_name + 1

print("market_price_dict: ", market_price_dict)

# Calculate difference % between average and market price and store value in dict
diff_market_and_mean_price_dict = {}
for x in stock_names:
    diff = market_price_dict[x] - mean_dict[x]
    diff_percent = diff *100/mean_dict[x]
    diff_market_and_mean_price_dict[x] = diff_percent

diff_market_and_mean_price_dict_sorted = sorted(diff_market_and_mean_price_dict.items(), key=lambda x: x[1])

print("diff_market_and_mean_price_dict_sorted: ", diff_market_and_mean_price_dict_sorted)


# diff_market_and_mean_price_df = pd.DataFrame([diff_market_and_mean_price_dict])
#
# print(diff_market_and_mean_price_df)
