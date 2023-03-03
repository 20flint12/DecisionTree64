# -*- coding: utf-8 -*-

from pprint import pprint
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import matplotlib.dates as mdates

from src.scikit_mathplot import main_binance_plot as mbp
from src.scikit_mathplot import binance_trader as btd


def on_press(event):
    print('press', event.key)
    if event.key == 'p':
        ani.event_source.stop()
    if event.key == 'r':
        ani.event_source.start()
    if event.key == 'l':
        current_frame = ani.frame_seq[-1]
        if current_frame < ani.frame_seq[-2]:
            ani.frame_seq = range(current_frame + 1, ani.frame_seq[-1] + 1)
        else:
            ani.event_source.stop()


trader_0 = btd.Trader(currency="BTC", wallet=(0, 0))
# trader_0.top_up_wallet(crypto=0.00123)
trader_0.top_up_wallet(valuta=100)
trader_1 = btd.Trader(currency="USDT", wallet=(0, 100))
print("trader_0=", trader_0)
print("trader_1=", trader_1)


# Set the figure size and title
fig = plt.figure(figsize=(10, 14))  # Figure(400x754)

fig.canvas.mpl_connect('key_press_event', on_press)


fig.subplots_adjust(top=0.95, bottom=.2, left=0.07, right=0.97, wspace=0.0, hspace=0.0)
ax0 = plt.subplot2grid((20, 1), (0, 0), rowspan=1)
ax1 = plt.subplot2grid((20, 1), (1, 0), rowspan=19)
# #######################################################################################


# Load the BTC price data from the CSV file
df = pd.read_csv('BTC_price_data_by_minute_last_5days.csv')
# print("df0=", df)

# Convert the timestamp column to a datetime object
df['time'] = pd.to_datetime(df['time'])

len_df = len(df)
SLICE_COUNT = 100

begin_date = df.iloc[0]['time']
end_date = df.iloc[-1]['time']
print(len_df, "|", SLICE_COUNT, " ***begin=", begin_date, "***end=", end_date)


# # start_time = pd.Timestamp.now() - pd.Timedelta(days=12)
# start_time = end_date - pd.Timedelta(days=1)
# df_filtered = df[df['time'] >= start_time]
# print(len_df, "|", len(df_filtered), "df_filtered=\n", df_filtered)

buy_rates = []
buy_times = []

sell_rates = []
sell_times = []


# Define the update function for the animation
def update(frame, dataframe=None, samples=1):
    # global df
    annot_text0 = ""
    annot_text1 = ""
    annot_text2 = ""
    len_total = len(dataframe)
    slice3 = dataframe.loc[frame:(frame + samples - 1), ['time', 'open']]
    # print(len(slice3))

    dates = mdates.date2num(slice3['time'])
    times = np.array([date for date in dates]).reshape(-1, 1)
    rates = slice3['open'].values

    trader_0.set_kilns(times, rates)
    trader_1.set_kilns(times, rates)
    # print("trader_0=", trader_0)
    # print("trader_1=", trader_1)

    history_trace_0 = 5
    future_trace_0 = 5
    future_times_0, future_rates_0 = trader_0.predict_future(history_trace=history_trace_0, future_trace=future_trace_0)
    history_trace_1 = 20
    future_trace_1 = 15
    future_times_1, future_rates_1 = trader_1.predict_future(history_trace=history_trace_1, future_trace=future_trace_1)
    # print(future_times_0, future_rates_0)
    # #######################################################################################

    rate_diff = trader_0.get_diffs()[2]
    rate_thrs = 20

    sell_condition = (rate_diff >= rate_thrs) and not trader_0.block_sell()
    if sell_condition:
        # print("sell")
        trader_0.sell_crypto()
        buy_times.append(times[-1])
        buy_rates.append(rates[-1])

    buy_condition = (rate_diff <= -rate_thrs) and True
    if buy_condition:
        # print("buy")
        trader_0.buy_crypto()
        sell_times.append(times[-1])
        sell_rates.append(rates[-1])

    # Clear graph points
    if len(buy_times) > 0 and buy_times[0] < times[0]:
        buy_times.pop(0)
        buy_rates.pop(0)

    if len(sell_times) > 0 and sell_times[0] < times[0]:
        sell_times.pop(0)
        sell_rates.pop(0)

    #
    wallet_0 = trader_0.get_wallet
    wallet_1 = trader_1.get_wallet
    annot_text0 += str(round(wallet_0[btd.CRYPTO], 5)) + " <> " + str(round(wallet_0[btd.VALUTA], 2))
    annot_text0 += " ||| "
    # text0 += str(round(wallet_1[btd.CRYPTO], 5)) + " <> " + str(round(wallet_1[btd.VALUTA], 2))
    annot_text0 += str(round(trader_0.get_rates[0], 2)) + " <> " + str(round(trader_0.get_rates[1], 2))

    annot_text1 = f"{frame}/{len_total}"

    annot_text2 += str(round(trader_0.get_diffs()[0], 1)) + " :: "
    annot_text2 += str(round(trader_0.get_diffs()[1], 1)) + " :: " + str(round(trader_0.get_diffs()[2], 1))
    annot_text2 += " | "
    annot_text2 += str(round(trader_1.get_diffs()[0], 1)) + " :: "
    annot_text2 += str(round(trader_1.get_diffs()[1], 1)) + " :: " + str(round(trader_1.get_diffs()[2], 1))
    # print(annot_text2)

    print(annot_text1, end=" ")
    print(annot_text0)

    # return

    #
    ax0.clear()
    ax0.axis('off')
    # ax0.set_xticks([])
    # ax0.set_yticks([])
    # ax0.set_xticklabels([])
    # ax0.set_yticklabels([])

    coords0 = (0.2, 0.5)
    ax0.annotate(annot_text0, xy=coords0, fontsize=10, horizontalalignment='center', verticalalignment='center', )

    coords1 = (0.5, 0.5)
    ax0.annotate(annot_text1, xy=coords1, fontsize=10, horizontalalignment='center', verticalalignment='center', )

    coords2 = (0.85, 0.5)
    ax0.annotate(annot_text2, xy=coords2, fontsize=10, horizontalalignment='center', verticalalignment='center', )

    #
    ax1.clear()
    ax1.plot(times, rates, color='#23a881')
    ax1.plot(future_times_0, future_rates_0)
    ax1.plot(future_times_1, future_rates_1)
    ax1.scatter(buy_times, buy_rates, color='blue', s=30)
    ax1.scatter(sell_times, sell_rates, color='red', s=30)
    ax1.scatter(times[samples-history_trace_0:samples], rates[samples-history_trace_0:samples], color='yellow', s=20)

    # Format the times-axis labels
    ax1.xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    ax1.xaxis.set_major_locator(plt.MaxNLocator(15))
    plt.xticks(rotation=90)


# Create a lambda function to pass named parameters to update function
args = {'dataframe': df, 'samples': SLICE_COUNT}
update_func = lambda frame: update(frame, **args)

# Animate the plot
ani = FuncAnimation(fig=fig, func=update_func, frames=len_df - SLICE_COUNT, interval=0, repeat=False)

# Show the plot
# plt.show()
