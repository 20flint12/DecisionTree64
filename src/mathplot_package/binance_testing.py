import matplotlib.pyplot as plt

fig, ax = plt.subplots()
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]
ax.plot(x, y)

def onclick(event):
    print('x =', event.xdata)

cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()