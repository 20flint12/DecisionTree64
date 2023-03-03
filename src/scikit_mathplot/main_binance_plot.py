# -*- coding: utf-8 -*-

# https://github.com/sammchardy/python-binance/issues

import json
import os
from datetime import datetime

import numpy as np
from binance.client import Client

import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# from matplotlib.animation import FuncAnimation
import matplotlib.dates as mdates

from sklearn import linear_model
# from scipy.signal import argrelextrema


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

    text = ""
    api_key, api_secret = get_credentials()
    client = Client(api_key, api_secret)
    print(client)

    ticker = client.get_symbol_ticker(symbol=symbol)
    price = round(float(ticker['price']), 2)
    text += f"The current rate of {symbol} is {price}"

    klines = client.get_historical_klines(symbol, kline_interval, interval)   # "1 day ago UTC" 24 hour ago UTC

    # timestamps = [entry[0] / 1000 for entry in klines]
    timestamps = [datetime.fromtimestamp(entry[0] / 1000) for entry in klines]
    dates = [mdates.date2num(timestamp) for timestamp in timestamps]

    # Convert the dates to datetime objects
    # dates = [datetime.strptime(str(kline[0]/1000), '%Y%m%d').date() for kline in klines]
    # print(klines, "\n", dates)

    # times = np.array([kline[0] for kline in klines]).reshape(-1, 1)
    times = np.array([date for date in dates]).reshape(-1, 1)
    rates = np.array([(float(kline[1])+float(kline[2])+float(kline[3])+float(kline[4]))/4. for kline in klines])
    # print(times.shape, rates.shape)
    text += "\nshapes=" + str(times.shape) + " / " + str(rates.shape)

    return times, rates, text


def predict_future(times=None, rates=None, sample_from=0, sample_to=0, time_delta=1, future_trace=2):

    regression = linear_model.LinearRegression()

    regression.fit(times[sample_from:sample_to, :], rates[sample_from:sample_to])
    # regression.fit(times.iloc[sample_from:sample_to, :], rates[sample_from:sample_to])

    # future_times = np.array([times[-1][0] + (itm * 3600 * 1000) for itm in range(long_mark)]).reshape(-1, 1)
    future_times = np.array([times[sample_to - 1][0] + (itm * time_delta) for itm in range(future_trace)]).reshape(-1, 1)
    future_rates = regression.predict(future_times)

    return future_times, future_rates


def plot_binance(file_name="photo_name", force_plot=False):
    text = ""

    # ===========================================================
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(7, 14))
    fig.subplots_adjust(top=0.975, bottom=.025, left=0.08, right=0.97, hspace=0.08)

    symbol = "BTCUSDT"

    kline_interval = Client.KLINE_INTERVAL_1MINUTE
    interval = "1 hour ago UTC"
    times, rates, text_out = get_klines(symbol=symbol, kline_interval=kline_interval, interval=interval)
    time_delta = times[1] - times[0]
    print("time_delta=", time_delta)
    text += "\n" + text_out


    # ++++++++++++++++++++++++++++++++++++++++++++++
    kline_interval = Client.KLINE_INTERVAL_1MINUTE
    interval = "5 hour ago UTC"
    times2, rates2, text_out2 = get_klines(symbol=symbol, kline_interval=kline_interval, interval=interval)

    ax2.grid(axis='y')
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax2.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=3, maxticks=10))

    ax2.plot(times2, rates2, color='y', linestyle='-')  # 'color': 'g', 'linestyle': '--'


    # ++++++++++++++++++++++++++++++++++++++++++++++
    kline_interval = Client.KLINE_INTERVAL_5MINUTE
    interval = "24 hour ago UTC"
    times3, rates3, text_out3 = get_klines(symbol=symbol, kline_interval=kline_interval, interval=interval)

    ax3.grid(axis='y')
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax3.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=3, maxticks=10))

    ax3.plot(times3, rates3, color='r', linestyle='-')  # 'color': 'g', 'linestyle': '--'



    # ===========================================================

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
    ax1.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=3, maxticks=10))
    # ax1.xticks(rotation=45)
    # ax1.grid(axis='x')



    ax12 = ax1.twiny()
    ax12.grid(axis='x')

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
    # counter = np.linspace(0, len(xdata), len(xdata))
    # counter = np.linspace(len(xdata)-1, 0, len(xdata))
    # ax12.plot(counter, ydata, 'r.')



    counter = np.linspace(0, len(times)-1, len(times))
    # counter = np.linspace(len(times)-1, -1, len(times))
    ax12.plot(counter, rates, 'r.')
    # ax12.invert_xaxis()

    ax12.tick_params('x', colors='r')



    line2 = None
    line22 = None
    points = 4
    future_trace = 2
    # for index_from in range(0, len(rates)-points, 1):
    for index_from in range(len(rates)-points, 0, -1):

        future_times, future_rates = predict_future(times=times, rates=rates,
                                                    sample_from=index_from, sample_to=index_from + points,
                                                    time_delta=time_delta, future_trace=future_trace)

        future_rates_track = future_rates[(index_from + future_trace) % future_trace]
        rate_diff = abs(rates[index_from] - future_rates_track)
        # print(index_from, rates[index_from], future_rates_track, rate_diff)
        if rate_diff > 50:
            print(rate_diff > 100, index_from, rate_diff)
            # index_from += int(points / 2)

            line2, = ax1.plot(future_times, future_rates, color='y', linestyle='-')    # 'color': 'g', 'linestyle': '--'

            future_counter = np.linspace(index_from, index_from + future_trace-1, future_trace)
            line22, = ax12.plot(future_counter + points - 1, future_rates, color='g', linestyle='--')

            # line3, = ax1.scatter(times[index_from], rates[index_from], color='red', s=30)
            ax1.scatter(times[index_from + points - 1], rates[index_from + points - 1], color='red', s=30)


    line4 = None
    line42 = None
    points = 5
    index_from = len(rates) - points
    future_trace = 5
    future_times, future_rates = predict_future(times=times, rates=rates,
                                                sample_from=index_from, sample_to=index_from + points,
                                                time_delta=time_delta, future_trace=future_trace)
    line4, = ax1.plot(future_times, future_rates, label="Prediction1", color='b', linestyle='-')

    # np.linspace(0, len(times)-1, len(times))
    future_counter = np.linspace(index_from, index_from + future_trace-1, future_trace)
    line42, = ax12.plot(future_counter + points - 1, future_rates, color='r', linestyle='--')



    # print(index_from, future_times, future_rates)
    future_rates_track = future_rates[future_trace-1]
    rate_diff = (future_rates_track - future_rates[0])
    print(index_from, future_times, future_rates, rate_diff)
    text += "\n" + str(round(rate_diff, 1))
    text += "\n" + str(round(rates[-1], 2))
    send_image = False
    if abs(rate_diff) > 100 or force_plot:
        send_image = True


        # ***********************************************************************
        res_savefig = plt.savefig(file_name)
        print("res_savefig=", res_savefig)

        # plt.xlabel("Time")
        # plt.ylabel("Rate (USDT)")
        # plt.title(f"Rate of {symbol}")
        # plt.legend()

        plt.show()

    return send_image, text


if __name__ == "__main__":
    """
    Plot image
    """

    plot_binance(file_name="photo_name", force_plot=True)

