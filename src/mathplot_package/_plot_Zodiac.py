import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib.cm as cm
import numpy as np
import math


# Create Zodiac colormap
colors = [
          '#ba1b1b', '#e75321', '#ba1b1b',  # AR    красный
          '#073763', '#0c343d', '#073763',  # TA    пастельные тона розового и зеленого
          '#ffdb00', '#fdff14', '#ffdb00',  # GE    желтый
          '#cec9c9', '#ee68db', '#cec9c9',  # CN    серебристый, фиолетовый
          '#ffd966', '#ce7e00', '#ffd966',  # LE    золотистый, оранжевый
          '#00294f', '#023e4f', '#00294f',  # VI    сине-зеленый
          '#0054b5', '#007e90', '#0054b5',  # LI    темно-голубой, зеленый, цвет морской волны
          '#31061e', '#0e0211', '#31061e',  # SC    черный
          '#3a0856', '#92001d', '#3a0856',  # SG    синий, голубой, фиолетовый, багровый
          '#45464f', '#983a17', '#45464f',  # CP    коричневый цвет, а также другие темные цвета оттенков земли
          '#35c3de', '#58dbee', '#35c3de',  # AQ    светло-голубой (такой оттенок у метановых облаков).
          '#7ea7d8', '#207678', '#7ea7d8',  # PI    все оттенки синего (болотный, сиреневый)
]
zodiac_cmap = LinearSegmentedColormap.from_list('zodiac_cmap', colors, N=960)


if __name__ == '__main__':

    plt.style.use('_mpl-gallery-nogrid')
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(4, 7))
    fig.subplots_adjust(top=0.95, bottom=.05, left=0.15, right=.95, wspace=0.00)
    # ************************************************************************

    xs = np.linspace(0, 360, 1000)
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

    axes[1].set_title(f"Zodiac", fontsize=10)
    axes[1].axis('off')
    axes[1].imshow(Z, interpolation='bilinear',  # 'nearest', 'bilinear', 'bicubic'
                   aspect='auto',
                   cmap=zodiac_cmap,
                   origin='upper',
                   vmax=Z.max(), vmin=Z.min())

    plt.show()
