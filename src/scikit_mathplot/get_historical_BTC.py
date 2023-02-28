#
# import pandas as pd
# from pycoingecko import CoinGeckoAPI
#
# # Initialize CoinGecko API client
# cg = CoinGeckoAPI()
#
# # Define the start and end dates for the data
# start_date = '2019-02-19'
# end_date = '2021-02-19'
#
# # Convert the start and end dates to Unix timestamps
# start_timestamp = int(pd.Timestamp(start_date).timestamp())
# end_timestamp = int(pd.Timestamp(end_date).timestamp())
#
# # Get historical BTC price data
# btc_price_data = cg.get_coin_market_chart_range_by_id(id='bitcoin', vs_currency='usd', from_timestamp=start_timestamp, to_timestamp=end_timestamp)
#
# # Convert the data to a pandas dataframe
# df = pd.DataFrame(btc_price_data['prices'], columns=['timestamp', 'price'])
#
# # Convert the timestamp to a datetime object
# df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
#
# # Save the data to a CSV file
# df.to_csv('BTC_price_data.csv', index=False)


# import pandas as pd
# import requests
#
# # Define the start and end dates for the data
# start_date = '2019-02-19'
# end_date = '2021-02-19'
#
# # Define the URL for the API endpoint
# url = f'https://min-api.cryptocompare.com/data/v2/histominute?fsym=BTC&tsym=USD&aggregate=1&e=CCCAGG&limit=2000&toTs={pd.Timestamp(end_date).timestamp()}'
#
# # Initialize a list to store the data
# data = []
#
# # Loop through the API responses to retrieve all the data
# while True:
#     response = requests.get(url)
#     result = response.json()['Data']
#     data.extend(result['Data'])
#     if result['TimeTo'] <= pd.Timestamp(start_date).timestamp():
#         break
#     url = f"https://min-api.cryptocompare.com/data/v2/histominute?fsym=BTC&tsym=USD&aggregate=1&e=CCCAGG&limit=2000&toTs={result['TimeFrom']}"
#
# # Convert the data to a pandas dataframe
# df = pd.DataFrame(data, columns=['time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_volume', 'trades', 'base_volume', 'vwap'])
#
# # Convert the time to a datetime object
# df['time'] = pd.to_datetime(df['time'], unit='s')
#
# # Save the data to a CSV file
# df.to_csv('BTC_price_data_by_minute.csv', index=False)





#
# import pandas as pd
# import requests
#
# # Define the start and end dates for the data
# end_date = int(pd.Timestamp.now().timestamp())
# start_date = int((pd.Timestamp.now() - pd.DateOffset(day=1)).timestamp())
#
# # start_timestamp = int(pd.Timestamp(start_date).timestamp())
# # end_timestamp = int(pd.Timestamp(end_date).timestamp())
#
# # Define the URL for the API endpoint
# url = f'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range?vs_currency=usd&from={start_date}&to={end_date}&interval=min'
#
# # Retrieve the data from the API
# response = requests.get(url)
# data = response.json()
#
# # Convert the data to a pandas dataframe
# df = pd.DataFrame(data['prices'], columns=['time', 'price'])
#
# # Convert the time to a datetime object
# df['time'] = pd.to_datetime(df['time'], unit='ms')
#
# # Save the data to a CSV file
# df.to_csv('BTC_price_data_by_minute_last_year.csv', index=False)


from binance.client import Client
import pandas as pd

from src.scikit_mathplot import main_binance_plot as bcr


api_key, api_secret = bcr.get_credentials()

# Create a client object
client = Client(api_key, api_secret)

# Define the start and end dates for the data
end_date = pd.Timestamp.now()
start_date = end_date - pd.DateOffset(years=1)

# Convert the dates to Unix timestamp integers in milliseconds
start_time = int(start_date.timestamp() * 1000)
end_time = int(end_date.timestamp() * 1000)

# Retrieve the data from Binance
symbol = 'BTCUSDT'
interval = Client.KLINE_INTERVAL_1MINUTE
klines = client.get_historical_klines(symbol, interval, start_time, end_time)
print(len(klines))

# Convert the data to a pandas dataframe
df = pd.DataFrame(klines, columns=['time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'num_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])

# Convert the time column to a datetime object
df['time'] = pd.to_datetime(df['time'], unit='ms')

# Save the data to a CSV file
df.to_csv('BTC_price_data_by_minute_last_1year.csv', index=False)

