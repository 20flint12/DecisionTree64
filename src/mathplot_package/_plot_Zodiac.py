import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib.cm as cm
import numpy as np
import math


# Create Zodiac colormap
colors = [

    # '#ba1b1b', '#e75321', '#ba1b1b',  # AR    красный
    # '#073763', '#0c343d', '#073763',  # TA    пастельные тона розового и зеленого
    # '#ffdb00', '#fdff14', '#ffdb00',  # GE    желтый
    # '#cec9c9', '#ee68db', '#cec9c9',  # CN    серебристый, фиолетовый
    # '#ffd966', '#ce7e00', '#ffd966',  # LE    золотистый, оранжевый
    # '#00294f', '#023e4f', '#00294f',  # VI    сине-зеленый
    # '#0054b5', '#007e90', '#0054b5',  # LI    темно-голубой, зеленый, цвет морской волны
    # '#31061e', '#0e0211', '#31061e',  # SC    черный
    # '#3a0856', '#92001d', '#3a0856',  # SG    синий, голубой, фиолетовый, багровый
    # '#45464f', '#983a17', '#45464f',  # CP    коричневый цвет, а также другие темные цвета оттенков земли
    # '#35c3de', '#58dbee', '#35c3de',  # AQ    светло-голубой (такой оттенок у метановых облаков).
    # '#7ea7d8', '#207678', '#7ea7d8',  # PI    все оттенки синего (болотный, сиреневый)

    '#7ea7d8', '#207678', '#207678', '#207678', '#7ea7d8',  # PI    все оттенки синего (болотный, сиреневый)

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

    '#ba1b1b', '#e75321', '#e75321', '#e75321', '#ba1b1b',  # AR    красный
]
zodiac_cmap = LinearSegmentedColormap.from_list('zodiac_cmap', colors, N=960)

'''
Огонь:      Овен, Лев, Стрелец          красным
Земля:      Телец, Дева, Козерог        коричневый
Воздух:     Близнецы, Весы, Водолей     синим
Вода:       Рак, Скорпион, Рыбы         зеленым
'''
colors = [
    '#2eeee1', '#02f991', '#02f991', '#02f991', '#2eeee1',  # Вода      зеленым

    '#f25500', '#ea2300', '#ea2300', '#ea2300', '#f25500',  # Огонь     красный     Белок, тепло
    '#543f2f', '#462e22', '#462e22', '#462e22', '#543f2f',  # Земля     коричневый  Соль, холод
    '#009fff', '#007dff', '#007dff', '#007dff', '#009fff',  # Воздух    синим       Жиры, свет
    '#90f0dc', '#02f991', '#02f991', '#02f991', '#90f0dc',  # Вода      зеленым     Углеводы, вода

    '#f25500', '#ea2300', '#ea2300', '#ea2300', '#f25500',  # Огонь     красный
]

elements_cmap = LinearSegmentedColormap.from_list('elements_cmap', colors, N=960)


OVERLAP_COEF = 0.91
if __name__ == '__main__':

    INT_BEG = 0
    INT_END = 360
    INT_BEG = 700
    INT_END = 800

    plt.style.use('_mpl-gallery-nogrid')
    fig, axes = plt.subplots(nrows=1, ncols=4, figsize=(4, 7))
    fig.subplots_adjust(top=0.95, bottom=.05, left=0.15, right=.95, wspace=0.00)
    # ************************************************************************

    xs = np.linspace(INT_BEG, INT_END, 1000)
    # ***********************************************************

    ycolors = np.mod(xs, 360)
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

    CYCLING_OVERLAP = 360 * (2/12)/2 * OVERLAP_COEF
    axes[1].imshow(Z, interpolation='nearest',  # 'nearest', 'bilinear', 'bicubic'
                   aspect='auto',
                   cmap=zodiac_cmap,
                   origin='upper',
                   # vmax=Z.max(), vmin=Z.min(),
                   vmin=0-CYCLING_OVERLAP, vmax=360+CYCLING_OVERLAP,
                   )


    # //////////////// ELEMENTS ////////////////////
    ycolors = np.mod(xs, 120)
    ys = ycolors

    axes[2].set_title(f'ypoints', fontsize=10)
    axes[2].grid()
    axes[2].axis(ymin=INT_END, ymax=INT_BEG)
    axes[2].plot(ys, xs, linestyle='dotted')


    arr_size = len(ys)
    gcolumn = 1
    Z = np.zeros(arr_size * gcolumn).reshape(arr_size, gcolumn)
    Z[:, 0] = ys

    axes[3].set_title(f"Elements", fontsize=10)
    axes[3].axis('off')
    CYCLING_OVERLAP = 120 * (2/4)/2 * OVERLAP_COEF
    axes[3].imshow(Z, interpolation='nearest',  # 'nearest', 'bilinear', 'bicubic'
                   aspect='auto',
                   cmap=elements_cmap,
                   origin='upper',
                   vmin=0 - CYCLING_OVERLAP, vmax=120 + CYCLING_OVERLAP,
                   )

    plt.show()
