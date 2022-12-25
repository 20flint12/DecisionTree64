import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib.cm as cm
import numpy as np

plt.style.use('_mpl-gallery-nogrid')

# # make data with uneven sampling in x
# x = [-3, -2, -1.6, -1.2, -.8, -.5, -.2, .1, .3, .5, .8, 1.1, 1.5, 1.9, 2.3, 3]
# X, Y = np.meshgrid(x, np.linspace(-3, 3, 128))
# Z = (1 - X/2 + X**5 + Y**3) * np.exp(-X**2 - Y**2)
#
# # plot
# fig, ax = plt.subplots()
#
# ax.pcolormesh(X, Y, Z, vmin=-0.5, vmax=1.0)


# Create the colormap
colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (0.7, 0.4, 0.1)]  # R -> G -> B
my_cmap = LinearSegmentedColormap.from_list('my_list', colors, N=100)


fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(4, 7))
fig.subplots_adjust(top=0.95, bottom=.05, left=0.15, right=.95, wspace=0.00)
# ************************************************************************

# gradient = np.linspace(0, 1, 100)
gradient = np.linspace(0, 1, 20)
gradient = np.vstack((gradient, gradient))


# x = np.linspace(-2, 2, 100)
# y = np.sin(x)
# gradient = np.vstack((x, y))
# gradient = np.hstack((x, y))


# t = np.linspace(0, 2 * np.pi, 10)
# gradient = np.sin(t)[:, np.newaxis] * np.cos(t)[np.newaxis, :]
# print(gradient)


delta = 1
x = y = np.arange(-10.0, 10.0, delta)
X, Y = np.meshgrid(x, y)
# print(X)
# print(Y)
# Z1 = np.exp(-X**2 - Y**2)
# Z = np.sin(Y)
i = np.linspace(-3, 3, 10)
Z = np.power(i, 2)
# Z = np.sin(i) - np.cos(i[:, np.newaxis])
# Z2 = np.exp(-(X - 1)**2 - (Y - 1)**2)
# Z = (Z1 - Z2) * 2
print(Z)
#
# # fig, ax = plt.subplots()
# im = axs[1].imshow(Z, interpolation='bilinear',
#                    cmap=cm.RdYlGn,
#                    origin='lower',
#                    extent=[-1, 1, -4, 4],
#                    vmax=Z.max(), vmin=Z.min())
# print(im)
#
# axs[0].set_title(f'my_list', fontsize=10)
# # axs[0].grid()
# # axs[0].swap_axes()
# # axs[0].invert_yaxis()
# axs[0].imshow(gradient, aspect='auto', cmap=my_cmap)
#
# # axs[1].set_title(f"twilight_r", fontsize=10)
# # axs[1].imshow(gradient, aspect='auto', cmap="twilight_r")
#
# plt.show()
