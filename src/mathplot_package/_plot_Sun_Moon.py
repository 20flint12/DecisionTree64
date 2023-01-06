import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib.cm as cm
import numpy as np
import math


def convert_colors(in_y_list=None, thresh=0.2):
    """
    :param in_y_list:
    :param thresh:    threshold
    :return:
    """

    # y_max = (max(in_y_list) + abs(min(in_y_list))) / 2
    y_max = min(max(in_y_list), abs(min(in_y_list)))

    y_thr = y_max * thresh
    # print("y_max=", y_max, " y_thr=", y_thr)

    last_y = 0
    res_color_list = []

    for y in in_y_list:

        if y > y_thr:
            y = y_thr
        elif y < -y_thr:
            y = -y_thr

        color_y = y / y_max
        if last_y < y:      # rising
            color_y = y / y_max
        elif last_y > y:    # setting
            color_y = -y / y_max + 2 * y_thr / y_max
        if last_y == y:
            if y >= y_thr:
                color_y = y_thr / y_max
            if y <= -y_thr:
                color_y = 3 * y_thr / y_max
        last_y = y

        res_color_list.append(color_y)

    # print("len=", len(res_color_list), " min=", min(res_color_list), " max=", max(res_color_list))

    return res_color_list


if __name__ == '__main__':

    plt.style.use('_mpl-gallery-nogrid')
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(4, 7))
    fig.subplots_adjust(top=0.95, bottom=.05, left=0.15, right=.95, wspace=0.00)
    # ************************************************************************

    # i = np.linspace(-5, 5, 20)
    # print(i)
    # # Z = np.power(i, 2)
    #
    # # image *= 255.0 / image.max()
    # i *= 0.5/i.max()
    # Z = i + 0.5
    # print(Z)

    # ***********************************************************
    xs = np.linspace(-2 * np.pi, 2 * np.pi, 1000)
    ys = np.sin(xs) * 27

    ycolors = convert_colors(in_y_list=ys, thresh=0.27)
    ys = ycolors

    axes[0].set_title(f'ypoints', fontsize=10)
    axes[0].grid()
    # axes[0].invert_xaxis()
    # axes[0].invert_yaxis()
    # axes[0].axis(ymin=-2 * np.pi, ymax=2 * np.pi)
    axes[0].axis(ymin=2 * np.pi, ymax=-2 * np.pi)
    axes[0].plot(ys, xs,
                 # aspect='auto',
                 linestyle='dotted')

    arr_size = len(ys)
    gcolumn = 5
    Z = np.zeros(arr_size * gcolumn).reshape(arr_size, gcolumn)
    Z[:, 0] = ys
    Z[:, 1] = ys
    Z[:, 2] = ys
    Z[:, 3] = ys
    Z[:, 4] = ys
    # print(Z)

    axes[1].set_title(f"twilight_r", fontsize=10)
    axes[1].axis('off')
    axes[1].imshow(Z, interpolation='nearest',  # 'nearest', 'bilinear', 'bicubic'
                   aspect='auto',
                   # cmap=cm.RdYlGn,  # gray
                   cmap="twilight_shifted",     # twilight_shifted
                   origin='upper',
                   vmax=Z.max(), vmin=Z.min())

    plt.show()

