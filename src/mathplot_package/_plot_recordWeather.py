
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib.cm as cm
import numpy as np
import ephem
import matplotlib.colors as mcolors


# Create colormap
colors = [
    '#ba1b1b', '#e75321', '#e75321', '#e75321', '#ba1b1b',  # AR    красный
    '#073763', '#0c343d', '#0c343d', '#0c343d', '#073763',  # TA    пастельные тона розового и зеленого
]

weather_cmap = LinearSegmentedColormap.from_list('elements_cmap', colors, N=960)


def plot_weather(data_list=None, file_name="user_photo2.jpg"):

    # plt.style.use('_mpl-gallery-nogrid')
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(4, 7))
    fig.subplots_adjust(top=0.95, bottom=.05, left=0.15, right=.95, wspace=0.00)
    # ************************************************************************

    len_arr = len(data_list)
    len_append = len_arr
    print("len_arr=", len_arr)
    # ***********************************************************

    xs = np.linspace(0, len_arr+len_append, len_arr+len_append)

    ycolors = np.array(data_list)
    ys = np.append(ycolors, np.full(len_append, np.average(ycolors)))


    axes[0].set_title(f'ypoints', fontsize=10)
    axes[0].grid()

    axes[0].axis(ymin=len_arr+len_append, ymax=0)
    axes[0].plot(ys, xs, linestyle='dotted')


    # ############################################################
    arr_size = len(ys); gcolumn = 1
    Z = np.zeros(arr_size * gcolumn).reshape(arr_size, gcolumn)
    Z[:, 0] = ys

    axes[1].set_title(f"Weather", fontsize=10)
    # axes[1].axis('off')

    # vert_range = lbl_dates[-1] - lbl_dates[0]
    # vert_range = days * 2
    vert_range = len_arr
    horiz_half = vert_range / axes[1].bbox.height * axes[1].bbox.width / 2

    axes[1].imshow(Z, interpolation='bicubic',  # 'nearest', 'bilinear', 'bicubic'
                   aspect='auto',
                   cmap='summer',
                   origin='upper',
                   extent=[-horiz_half, horiz_half, vert_range, 0],
                   vmax=Z.max(), vmin=Z.min())

    plt.show()


if __name__ == '__main__':

    values = [79, 79, 79, 79, 79, 82, 82, 82, 82, 82, 82, 82, 82, 82, 82, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79,
              79, 79, 79, 79, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 76, 76, 76, 76, 76, 76, 76, 76, 76, 76,
              76, 76, 76, 76, 76, 76, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80,
              80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 84, 84, 84, 84,
              84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 87, 87,
              87, 87, 87]

    plot_weather(data_list=values, file_name="user_photo2.jpg")




