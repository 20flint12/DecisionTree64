import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
import numpy as np

fig, ax = plt.subplots()
line, = ax.plot([], [])

t = np.linspace(0, 10, 100)
x = np.sin(t)

def update(frame):
    line.set_data(t[:frame], x[:frame])
    return line,

def on_forward(event):
    current_frame = anim.frame_seq[-1]
    if current_frame < anim.frame_seq[-2]:
        anim.frame_seq = range(current_frame + 1, anim.frame_seq[-1] + 1)
    else:
        anim.event_source.stop()

def on_backward(event):
    current_frame = anim.frame_seq[-1]
    if current_frame > anim.frame_seq[0]:
        anim.frame_seq = range(current_frame - 1, anim.frame_seq[0] - 1, -1)
    else:
        anim.event_source.stop()

anim = FuncAnimation(fig, update, frames=len(t), blit=True, repeat=False)

# Create two buttons to step the animation forward and backward
ax_forward = plt.axes([0.81, 0.02, 0.1, 0.05])
ax_backward = plt.axes([0.7, 0.02, 0.1, 0.05])
button_forward = Button(ax_forward, 'Forward')
button_backward = Button(ax_backward, 'Backward')
button_forward.on_clicked(on_forward)
button_backward.on_clicked(on_backward)

plt.show()
