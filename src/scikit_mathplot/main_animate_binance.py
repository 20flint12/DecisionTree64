# -*- coding: utf-8 -*-

from pprint import pprint
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import matplotlib.dates as mdates

from src.scikit_mathplot import main_binance_plot as mbp


# Set the figure size and title
fig = plt.figure(figsize=(10, 14))  # Figure(400x754)
fig.subplots_adjust(top=0.95, bottom=.2, left=0.07, right=0.97, wspace=0.0, hspace=0.0)
# ax1.set_title('BTC Price (Last 2 Years by Minute)')
# #######################################################################################


ax0 = plt.subplot2grid((20, 1), (0, 0), rowspan=1)
ax1 = plt.subplot2grid((20, 1), (1, 0), rowspan=19)

# ax0.axis('off')
# ax0.set_xticks([])
# ax0.set_yticks([])
# ax0.set_xticklabels([])
# ax0.set_yticklabels([])

# Load the BTC price data from the CSV file
df = pd.read_csv('BTC_price_data_by_minute_last_5days.csv')
# print("df0=", df)

# Convert the timestamp column to a datetime object
df['time'] = pd.to_datetime(df['time'])

len_df = len(df)
SLICE_COUNT = 800

begin_date = df.iloc[0]['time']
end_date = df.iloc[-1]['time']
print(len_df, "|", SLICE_COUNT, " ***begin=", begin_date, "***end=", end_date)


# # start_time = pd.Timestamp.now() - pd.Timedelta(days=12)
# start_time = end_date - pd.Timedelta(days=1)
# df_filtered = df[df['time'] >= start_time]
# print(len_df, "|", len(df_filtered), "df_filtered=\n", df_filtered)


# Define the update function for the animation
def update(frame, dataframe=None, samples=1):
    # global df
    len_total = len(dataframe)
    slice3 = dataframe.loc[frame:frame + samples, ['time', 'open']]
    # print(len(slice3))

    dates = mdates.date2num(slice3['time'])
    times = np.array([date for date in dates]).reshape(-1, 1)
    rates = slice3['open'].values

    time_delta = times[1] - times[0]

    POINTS = 20
    index_from = samples + 1 - POINTS
    future_trace = 15
    future_times, future_rates = mbp.predict_future(times=times, rates=rates,
                                                    sample_from=index_from, sample_to=index_from + POINTS,
                                                    time_delta=time_delta, future_trace=future_trace)
    POINTS = 5
    index_from = samples + 1 - POINTS
    future_trace = 5
    future_times2, future_rates2 = mbp.predict_future(times=times, rates=rates,
                                                      sample_from=index_from, sample_to=index_from + POINTS,
                                                      time_delta=time_delta, future_trace=future_trace)

    # print(future_times, future_rates)

    #
    ax0.clear()
    ax0.axis('off')
    # ax0.set_xticks([])
    # ax0.set_yticks([])
    # ax0.set_xticklabels([])
    # ax0.set_yticklabels([])
    annot_text1 = f"{frame}/{len_total}"
    annot_text2 = "w4r2erd34"
    coords1 = (0.1, 0.5)
    coords2 = (0.8, 0.5)
    ax0.annotate(annot_text1, xy=coords1, fontsize=10, horizontalalignment='center', verticalalignment='center', )
    ax0.annotate(annot_text2, xy=coords2, fontsize=10, horizontalalignment='center', verticalalignment='center', )

    #
    ax1.clear()
    ax1.plot(times, rates)
    ax1.plot(future_times, future_rates)
    ax1.plot(future_times2, future_rates2)
    ax1.scatter(times[index_from:index_from + POINTS], rates[index_from:index_from + POINTS], color='red', s=20)

    # Format the times-axis labels
    ax1.xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    # ax.xaxis.set_major_locator(plt.MaxNLocator(10))
    plt.xticks(rotation=90)


# Create a lambda function to pass named parameters to update function
args = {'dataframe': df, 'samples': 100}
update_func = lambda frame: update(frame, **args)

# Animate the plot
ani = FuncAnimation(fig=fig, func=update_func, frames=len_df - SLICE_COUNT, interval=50)

# Show the plot
plt.show()
