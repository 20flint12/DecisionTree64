# -*- coding: utf-8 -*-

import json
import os

import numpy as np
from binance.client import Client
import matplotlib.pyplot as plt
from sklearn import linear_model
from scipy.signal import argrelextrema
from matplotlib.animation import FuncAnimation
import matplotlib.dates as mdates
from datetime import datetime


def get_credentials():

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

    return api_key, api_secret


def get_klines(symbol="BTCUSDT", kline_interval=Client.KLINE_INTERVAL_15MINUTE, interval="1 day ago UTC"):

    api_key, api_secret = get_credentials()
    client = Client(api_key, api_secret)
    print(client)

    ticker = client.get_symbol_ticker(symbol=symbol)
    print(f"The current rate of {symbol} is {ticker['price']}")

    klines = client.get_historical_klines(symbol, kline_interval, interval)   # "1 day ago UTC" 24 hour ago UTC

    # timestamps = [entry[0] / 1000 for entry in klines]
    timestamps = [datetime.fromtimestamp(entry[0] / 1000) for entry in klines]

    # dates = [mdates.date2num(mdates.epoch2num(timestamp)) for timestamp in timestamps]
    dates = [mdates.date2num(timestamp) for timestamp in timestamps]

    # Convert the dates to datetime objects
    # dates = [datetime.strptime(str(kline[0]/1000), '%Y%m%d').date() for kline in klines]
    # print(klines, "\n", timestamps, "\n", dates)

    # times = np.array([kline[0] for kline in klines]).reshape(-1, 1)
    times = np.array([date for date in dates]).reshape(-1, 1)
    rates = np.array([float(kline[4]) for kline in klines])
    print(times.shape, rates.shape)

    return times, rates


def predict_future(times=None, rates=None, from_time=0, to_time=0, time_delta=1, track=2):

    regression = linear_model.LinearRegression()
    regression.fit(times[from_time:to_time, :], rates[from_time:to_time])
    # future_times = np.array([times[-1][0] + (itm * 3600 * 1000) for itm in range(long_mark)]).reshape(-1, 1)
    future_times = np.array([times[to_time-1][0] + (itm * time_delta) for itm in range(track)]).reshape(-1, 1)
    future_rates = regression.predict(future_times)

    return future_times, future_rates


# symbol = "BTCUSDT"
# interval = "1 day ago UTC"
# kline_interval = Client.KLINE_INTERVAL_1HOUR
kline_interval = Client.KLINE_INTERVAL_15MINUTE
# kline_interval = Client.KLINE_INTERVAL_1MINUTE
# interval = "24 hour ago UTC"
interval = "4 hour ago UTC"
times, rates = get_klines(symbol="BTCUSDT", kline_interval=kline_interval, interval=interval)
time_delta = times[1] - times[0]
print("time_delta=", time_delta)


# ===========================================================
fig, ax1 = plt.subplots()

line1, = ax1.plot(times, rates, 'b-')
# ax1.tick_params('x', colors='b')
# locator = mdates.AutoDateLocator(minticks=3, maxticks=7)
# formatter = mdates.ConciseDateFormatter(locator)
# ax1.xaxis.set_major_locator(locator)
# ax1.xaxis.set_major_formatter(formatter)

ax1.xaxis_date()
ax1.autoscale_view()
# ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
# ax1.xticks(rotation=45)
# ax1.grid(axis='x')




ax2 = ax1.twiny()
ax2.grid(axis='x')

# xdata = []
# ydata = []
# # for line in [line1, line2, line3, line4]:
# for line in [line1, line2, ]:
#     if line is not None:
#         xdata.append(line.get_xdata())
#         ydata.append(line.get_ydata())
# xdata = np.concatenate(xdata)
# ydata = np.concatenate(ydata)
# # print(len(xdata), xdata)



counter = np.linspace(0, len(times)-1, len(times))
ax2.plot(counter, rates, 'r.')

# counter = np.linspace(0, len(xdata), len(xdata))
# counter = np.linspace(len(xdata)-1, 0, len(xdata))
# ax2.plot(counter, ydata, 'r.')

ax2.tick_params('x', colors='r')



line2 = None
line22 = None
points = 3
track = 2
# for index in range(0, len(rates)-points, 1):
for index in range(len(rates)-points, 0, -1):

    future_times, future_rates = predict_future(times=times, rates=rates,
                                                from_time=index, to_time=index + points,
                                                time_delta=time_delta, track=track)

    future_rates_track = future_rates[(index + track) % track]
    rate_diff = abs(rates[index] - future_rates_track)
    # print(index, rates[index], future_rates_long, rate_diff)
    if rate_diff > 50:
        print(rate_diff > 100, index, rate_diff)
        # index += int(points / 2)

        line2, = ax1.plot(future_times, future_rates)

        future_counter = np.linspace(index, index + track-1, track)
        line22, = ax2.plot(future_counter + points - 1, future_rates)

        # line3, = ax1.scatter(times[index], rates[index], color='red', s=30)
        ax1.scatter(times[index + points - 1], rates[index + points - 1], color='red', s=30)


line4 = None
line42 = None
points = len(rates) - 12
index = len(rates) - points
track = 5
future_times, future_rates = predict_future(times=times, rates=rates,
                                            from_time=index, to_time=index + points,
                                            time_delta=time_delta, track=track)
line4, = ax1.plot(future_times, future_rates, label="Prediction1")


# np.linspace(0, len(times)-1, len(times))
future_counter = np.linspace(index, index + track-1, track)
line42, = ax2.plot(future_counter + points - 1, future_rates)









# plt.xlabel("Time")
# plt.ylabel("Rate (USDT)")
# plt.title(f"Rate of {symbol}")


# plt.legend()
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

