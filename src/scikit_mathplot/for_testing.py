# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

# generate some data
x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)

# create the figure and axes
fig, ax = plt.subplots()

# plot the data
ax.plot(x, y)

# remove the tick labels on the x-axis
ax.set_xticklabels([])

# remove the tick labels on the y-axis
ax.set_yticklabels([])

# show the plot
plt.show()

