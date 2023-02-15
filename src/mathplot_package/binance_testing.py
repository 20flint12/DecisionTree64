# -*- coding: utf-8 -*-

import json
import os

from binance.client import Client
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


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


api_key, api_secret = get_credentials()
client = Client(api_key, api_secret)

klines = client.get_historical_klines('BTCUSDT', Client.KLINE_INTERVAL_1DAY, '30 days ago UTC')

timestamps = [entry[0]/1000 for entry in klines]
dates = [mdates.date2num(mdates.epoch2num(timestamp)) for timestamp in timestamps]

open_prices = [float(entry[1]) for entry in klines]
high_prices = [float(entry[2]) for entry in klines]
low_prices = [float(entry[3]) for entry in klines]
close_prices = [float(entry[4]) for entry in klines]

fig, ax = plt.subplots()

ax.xaxis_date()
ax.autoscale_view()

candlestick_data = list(zip(dates, open_prices, high_prices, low_prices, close_prices))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax.xaxis.set_major_locator(mdates.AutoDateLocator())

ax.set_xlabel('Date')
ax.set_ylabel('Price')

plt.title('BTCUSDT 1-day candlestick chart')
plt.xticks(rotation=45)

plt.grid()

# candlestick_ohlc(ax, candlestick_data, width=0.6, colorup='g', colordown='r')

plt.show()
