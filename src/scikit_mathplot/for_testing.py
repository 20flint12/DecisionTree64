# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
#
# # Create some data
# x = np.linspace(0, 2*np.pi, 100)
# y = np.sin(x)
#
# # Create the figure and axis
# fig, ax = plt.subplots()
#
# # Plot the initial data
# line, = ax.plot(x, y)
#
# # Define the function to update the plot
# def update(num):
#     line.set_ydata(np.sin(num*x))
#     return line,
#
# # Define the function to handle key presses
# def on_key_press(event):
#     if event.key == ' ':
#         anim.event_source.stop()
#         print("\n", anim.frame_seq,
#               "\n", anim.new_frame_seq(),
#               "\n", anim.save_count
#               )
#         # plt.close()
#
# # Create the animation
# anim = animation.FuncAnimation(fig, update, frames=np.linspace(0, 2, 100), interval=50)
#
# # Connect the key press event to the figure
# fig.canvas.mpl_connect('key_press_event', on_key_press)
#
# # Show the plot
# plt.show()




import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Define the update function
def update(frame):
    # Update the plot with new data
    ...

# Define the key press event function
def on_key_press(event):
    if event.key == 'left':
        # Decrement the frame number by 1
        anim.frame_seq = range(max(0, anim.frame_seq[0] - 1), anim.frame_seq[-1])
    elif event.key == 'right':
        # Increment the frame number by 1
        anim.frame_seq = range(anim.frame_seq[0] + 1, min(len(anim.frames), anim.frame_seq[-1] + 1))
    else:
        return
    # Redraw the plot with the new frame
    anim.event_source.stop()
    anim.event_source.start()

# Create the figure and axis
fig, ax = plt.subplots()

# Create the animation with 100 frames
anim = animation.FuncAnimation(fig, update, frames=range(100), interval=100)

# Bind the key press event function to the figure
fig.canvas.mpl_connect('key_press_event', on_key_press)

# Start the animation
plt.show()
