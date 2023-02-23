import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

# Generate some example data
x = np.linspace(0, 2*np.pi, 200)
y = np.sin(x)

# Create a figure and axis object
fig, ax = plt.subplots()

# Create a line plot
line, = ax.plot(x, y)

# Define the update function for the animation
def update(freq):
    line.set_ydata(np.sin(x * freq))
    fig.canvas.draw_idle()

# Create a slider widget
ax_freq = plt.axes([0.2, 0.1, 0.6, 0.03])
slider_freq = Slider(ax=ax_freq, label='Frequency', valmin=0.1, valmax=5, valinit=1)

# Add a callback to the slider
slider_freq.on_changed(update)

# Display the plot
plt.show()
