import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib.cm as cm
import numpy as np
import ephem
import matplotlib.colors as mcolors


# Create Zodiac colormap
colors = [

    '#ba1b1b', '#e75321', '#e75321', '#e75321', '#ba1b1b',  # AR    красный
    '#073763', '#0c343d', '#0c343d', '#0c343d', '#073763',  # TA    пастельные тона розового и зеленого
    '#ffdb00', '#fdff14', '#fdff14', '#fdff14', '#ffdb00',  # GE    желтый
    '#cec9c9', '#ee68db', '#ee68db', '#ee68db', '#cec9c9',  # CN    серебристый, фиолетовый
]

elements_cmap = LinearSegmentedColormap.from_list('elements_cmap', colors, N=960)


if __name__ == '__main__':

    # plt.style.use('_mpl-gallery-nogrid')
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(4, 7))
    fig.subplots_adjust(top=0.95, bottom=.05, left=0.15, right=.95, wspace=0.00)
    # ************************************************************************

    xs = np.linspace(0, 1, 1000)


    # date = ephem.Date(12022)
    # moon = ephem.Moon()
    # moon.compute(date)
    # phase = round(moon.moon_phase * 100, 2)
    # print(phase)
    # ***********************************************************

    ycolors = xs    # convert_colors(in_y_list=ys, thresh=0.27)
    ys = ycolors

    axes[0].set_title(f'ypoints', fontsize=10)
    axes[0].grid()
    # axes[0].invert_xaxis()
    # axes[0].invert_yaxis()
    axes[0].axis(ymin=360, ymax=0)
    axes[0].plot(ys, xs, linestyle='dotted')


    arr_size = len(ys)
    gcolumn = 5
    Z = np.zeros(arr_size * gcolumn).reshape(arr_size, gcolumn)
    Z[:, 0] = ys
    Z[:, 1] = ys
    Z[:, 2] = ys
    Z[:, 3] = ys
    Z[:, 4] = ys
    # print(Z)

    axes[1].set_title(f"Elements", fontsize=10)
    axes[1].axis('off')
    axes[1].imshow(Z, interpolation='bilinear',  # 'nearest', 'bilinear', 'bicubic'
                   aspect='auto',
                   cmap=elements_cmap,
                   origin='upper',
                   vmax=Z.max(), vmin=Z.min())

    plt.show()
