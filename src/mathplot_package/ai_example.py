# import matplotlib.pyplot as plt
# import numpy as np
# import matplotlib.animation as animation
#
# # Generate the data for the animation
# def generate_data():
#     for i in range(10):
#         yield np.random.rand(10)
#
# # Set up the figure and axis for the plot
# fig, ax = plt.subplots()
# line, = ax.plot(np.random.rand(10))
#
# # Define the update function for the animation
# def update(data):
#     line.set_ydata(data)
#     return line,
#
# # Run the animation
# ani = animation.FuncAnimation(fig, update, generate_data, interval=100)
# plt.show()








#
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
# import numpy as np
#
# # Generate some example data
# x = np.linspace(0, 2*np.pi, 200)
# y = np.sin(x)
#
# # Create a figure and axis object
# fig, ax = plt.subplots()
#
# # Create a line plot
# line, = ax.plot(x, y)
#
# # Define the update function for the animation
# def update(frame):
#     line.set_ydata(np.sin(x + frame/10))
#     return line,
#
# # Create the animation object
# ani = FuncAnimation(fig, update, frames=range(100), interval=50)
#
# # Wait for the animation to finish
# plt.show()


