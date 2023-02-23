# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation


# fig, ax = plt.subplots()
#
# t = np.linspace(0, 3, 40)
# g = -9.81
# v0 = 12
# z = g * t**2 / 2 + v0 * t
#
# v02 = 5
# z2 = g * t**2 / 2 + v02 * t
#
# scat = ax.scatter(t[0], z[0], c="b", s=5, label=f'v0 = {v0} m/s')
# line2 = ax.plot(t[0], z2[0], label=f'v0 = {v02} m/s')[0]
# ax.set(xlim=[0, 3], ylim=[-4, 10], xlabel='Time [s]', ylabel='Z [m]')
# ax.legend()
#
#
# def update(frame):
#     # for each frame, update the data stored on each artist.
#     x = t[:frame]
#     y = z[:frame]
#     # update the scatter plot:
#     data = np.stack([x, y]).T
#     scat.set_offsets(data)
#     # update the line plot:
#     line2.set_xdata(t[:frame])
#     line2.set_ydata(z2[:frame])
#     return (scat, line2)
#
#
# ani = animation.FuncAnimation(fig=fig, func=update, frames=40, interval=30)
# plt.show()



# Load the BTC price data from the CSV file
df = pd.read_csv('BTC_price_data_by_minute_last_5days.csv')

# Convert the timestamp column to a datetime object
df['time'] = pd.to_datetime(df['time'])

# Set the figure size and title
fig, ax = plt.subplots(figsize=(10, 5))
fig.subplots_adjust(top=0.975, bottom=.25, left=0.08, right=0.97, hspace=0.08)
ax.set_title('BTC Price (Last 2 Years by Minute)')


# Define the update function for the animation
def update(frame):
    # Filter the data to only include the last 2 years
    start_time = pd.Timestamp.now() - pd.Timedelta(days=5)
    df_filtered = df[df['time'] >= start_time]

    # Convert the timestamp column to a matplotlib date format
    x = df_filtered['time']

    # Plot the BTC close price data
    y = df_filtered['close']
    ax.clear()
    ax.plot(x, y)

    # Format the x-axis labels
    ax.xaxis.set_major_locator(plt.MaxNLocator(10))
    ax.xaxis.set_major_formatter(plt.FixedFormatter([t.strftime("%Y-%m-%d %H:%M") for t in x]))
    plt.xticks(rotation=90)


# Animate the plot
ani = FuncAnimation(fig, update, interval=60000)

# Show the plot
plt.show()



