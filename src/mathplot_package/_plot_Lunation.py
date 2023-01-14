
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
    '#ffd966', '#ce7e00', '#ce7e00', '#ce7e00', '#ffd966',  # LE    золотистый, оранжевый
    '#00294f', '#023e4f', '#023e4f', '#023e4f', '#00294f',  # VI    сине-зеленый
    '#0054b5', '#007e90', '#007e90', '#007e90', '#0054b5',  # LI    темно-голубой, зеленый, цвет морской волны
    '#31061e', '#0e0211', '#0e0211', '#0e0211', '#31061e',  # SC    черный
    '#3a0856', '#92001d', '#92001d', '#92001d', '#3a0856',  # SG    синий, голубой, фиолетовый, багровый
    '#45464f', '#983a17', '#983a17', '#983a17', '#45464f',  # CP    коричневый цвет, а также другие темные цвета оттенков земли
    '#35c3de', '#58dbee', '#58dbee', '#58dbee', '#35c3de',  # AQ    светло-голубой (такой оттенок у метановых облаков).
    '#7ea7d8', '#207678', '#207678', '#207678', '#7ea7d8',  # PI    все оттенки синего (болотный, сиреневый)

]

BREAK_COLOR = (0, 0.5, 0, 1.0)
colors = [

    # BREAK_COLOR,

    (0, 0, 1, 0.6),
    (0, 0, 1, 0.6),
    (0, 0, 1, 0.7),
    (0, 0, 1, 0.7),
    (0, 0, 1, 0.8),
    (0, 0, 1, 0.8),
    (0, 0, 1, 0.9),
    (0, 0, 1, 0.9),
    (0, 0, 1, 1.0),
    (0, 0, 1, 1.0),

    (1, 0, 0, 0.1),     # first color is black, last is red
    (1, 0, 0, 0.1),
    (1, 0, 0, 0.2),
    (1, 0, 0, 0.2),
    (1, 0, 0, 0.3),
    (1, 0, 0, 0.3),
    (1, 0, 0, 0.4),
    (1, 0, 0, 0.4),
    (1, 0, 0, 0.5),
    (1, 0, 0, 0.5),

    # BREAK_COLOR,

    (1, 0, 0, 0.6),
    (1, 0, 0, 0.6),
    (1, 0, 0, 0.7),
    (1, 0, 0, 0.7),
    (1, 0, 0, 0.8),
    (1, 0, 0, 0.8),
    (1, 0, 0, 0.9),
    (1, 0, 0, 0.9),
    (1, 0, 0, 1.0),
    (1, 0, 0, 1.0),

    # BREAK_COLOR,

    (0, 0, 1, 0.1),
    (0, 0, 1, 0.1),
    (0, 0, 1, 0.2),
    (0, 0, 1, 0.2),
    (0, 0, 1, 0.3),
    (0, 0, 1, 0.3),
    (0, 0, 1, 0.4),
    (0, 0, 1, 0.4),
    (0, 0, 1, 0.5),
    (0, 0, 1, 0.5),

    # BREAK_COLOR,

    (0, 0, 1, 0.6),
    (0, 0, 1, 0.6),
    (0, 0, 1, 0.7),
    (0, 0, 1, 0.7),
    (0, 0, 1, 0.8),
    (0, 0, 1, 0.8),
    (0, 0, 1, 0.9),
    (0, 0, 1, 0.9),
    (0, 0, 1, 1.0),
    (0, 0, 1, 1.0),

    (1, 0, 0, 0.1),     # extra color for transfer
    (1, 0, 0, 0.1),
    (1, 0, 0, 0.2),
    (1, 0, 0, 0.2),
    (1, 0, 0, 0.3),
    (1, 0, 0, 0.3),
    (1, 0, 0, 0.4),
    (1, 0, 0, 0.4),
    (1, 0, 0, 0.5),
    (1, 0, 0, 0.5),

    # BREAK_COLOR,

]

lunation_cmap = LinearSegmentedColormap.from_list('lunation_cmap', colors, N=960)


if __name__ == '__main__':

    INT_BEG = 0.80
    INT_END = 1.20
    INT_BEG = 0.0
    INT_END = 2.0

    plt.style.use('_mpl-gallery-nogrid')
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(4, 7))
    fig.subplots_adjust(top=0.95, bottom=.05, left=0.15, right=.95, wspace=0.00)
    # ************************************************************************

    xs = np.linspace(INT_BEG, INT_END, 1000)

    # date = ephem.Date(12022)
    # moon = ephem.Moon()
    # moon.compute(date)
    # phase = round(moon.moon_phase * 100, 2)
    # print(phase)
    # ***********************************************************

    ycolors = np.mod(xs, 1.0)    # for several cycles
    ys = ycolors

    axes[0].set_title(f'ypoints', fontsize=10)
    axes[0].grid()
    axes[0].axis(ymin=INT_END, ymax=INT_BEG)
    axes[0].plot(ys, xs, linestyle='dotted')


    arr_size = len(ys)
    gcolumn = 1
    Z = np.zeros(arr_size * gcolumn).reshape(arr_size, gcolumn)
    Z[:, 0] = ys

    axes[1].set_title(f"Zodiac", fontsize=10)
    axes[1].axis('off')

    # CYCLING_OVERLAP = 0.239
    CYCLING_OVERLAP = 1.0 * (2 / 4) / 2 * 0.95
    axes[1].imshow(Z, interpolation='nearest',  # 'nearest', 'bilinear', 'bicubic'
                   aspect='auto',
                   cmap=lunation_cmap,
                   origin='upper',
                   # vmax=Z.max(), vmin=Z.min(),
                   vmin=0-CYCLING_OVERLAP, vmax=1+CYCLING_OVERLAP,
                   # vmin=-0.0, vmax=1.0,
                   )

    plt.show()
