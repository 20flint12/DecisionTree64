# -*- coding: utf-8 -*-

import json
import os

import numpy as np
from binance.client import Client
import matplotlib.pyplot as plt
from sklearn import linear_model


script_dir = os.path.dirname(os.path.abspath(__file__))
# print(script_dir)
script_dir_up = os.path.dirname(script_dir)
# print(script_dir_up)
script_dir_up_up = os.path.dirname(script_dir_up)
# print(script_dir_up_up)
file_name = "credentials.json"
file_path = os.path.join(script_dir_up_up, file_name)
# print(file_path)

with open(file_path, 'r') as f:
    print(f)
    config = json.load(f)

api_key = config['Binance']['api_key']
api_secret = config['Binance']['api_secret']


client = Client(api_key, api_secret)
print(client)


symbol = "BTCUSDT"
ticker = client.get_symbol_ticker(symbol=symbol)
print(f"The current rate of {symbol} is {ticker['price']}")

klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_15MINUTE, "6 hour ago UTC")   # "1 day ago UTC" 24 hour ago UTC


times = np.array([kline[0] for kline in klines]).reshape(-1, 1)
rates = np.array([float(kline[4]) for kline in klines])
print(times.shape, rates.shape)


regr_1 = linear_model.LinearRegression()
regr_1.fit(times[-20:, :], rates[-20:])
future_times1 = np.array([times[-1][0] + (i * 3600 * 1000) for i in range(4)]).reshape(-1, 1)
future_rates_1 = regr_1.predict(future_times1)


regr_2 = linear_model.LinearRegression()
regr_2.fit(times[-10:, :], rates[-10:])
future_times2 = np.array([times[-1][0] + (i * 3600 * 1000) for i in range(3)]).reshape(-1, 1)
future_rates_2 = regr_2.predict(future_times2)


regr_3 = linear_model.LinearRegression()
regr_3.fit(times[-5:, :], rates[-5:])
future_times3 = np.array([times[-1][0] + (i * 3600 * 1000) for i in range(2)]).reshape(-1, 1)
future_rates_3 = regr_3.predict(future_times3)


plt.plot(times, rates, label="Historical Data")
plt.plot(future_times1, future_rates_1, label="Prediction1")
plt.plot(future_times2, future_rates_2, label="Prediction2")
plt.plot(future_times3, future_rates_3, label="Prediction3")
plt.xlabel("Time")
plt.ylabel("Rate (USDT)")
plt.title(f"Rate of {symbol}")
plt.legend()
plt.show()






# res = client.get_exchange_info()
# # print(client.response.headers)
# print(client.get_all_orders(symbol='BNBBTC', requests_params={'timeout': 5}))


# for r in res:
#     # {'close': '29316.38000000',
#     #  'closeTime': 1654926299999,
#     #  'high': '29343.35000000',
#     #  'low': '29300.82000000',
#     #  'numTrades': 5585,
#     #  'open': '29330.69000000',
#     #  'openTime': 1654925400000,
#     #  'quoteVolume': '5139150.08936450',
#     #  'volume': '175.24264000'},
#     # print(r)
#
#     print(r["close"], r["volume"], r["quoteVolume"])

