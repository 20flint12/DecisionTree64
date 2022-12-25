
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

import numpy as np
from datetime import datetime, timedelta
from pprint import pprint

import src.ephem_routines.ephem_package.geo_place as geo
import src.ephem_routines.ephem_package.sun_rise_sett as sr
import src.ephem_routines.ephem_package.zodiac_phase as zd


def plot_color_of_the_days(observer=None, days=1, file_name="plot_astro_summary.png"):

    begin_date = observer.utc - timedelta(days=days)
    end_date = observer.utc + timedelta(days=days)
    dates = np.linspace(begin_date.timestamp(), end_date.timestamp(), 10)

    # begin_date = datetime.now()
    # then = begin_date + dt.timedelta(days=100)
    # days = mdates.drange(now, then, dt.timedelta(days=1))
    # print(dates)

    sun_lon = []
    sun_lat = []
    moon_lon = []
    moon_lat = []
    # sun_dist = []
    # moon_dist = []
    sun_angle = []

    for cur_dt in dates:
        observer.utc = datetime.fromtimestamp(cur_dt)
        ecl_dict, ecl_text = zd.main_zodiac_sun_moon(observer=observer)
        # print(observer.utc)
        sun_lon.append(ecl_dict["sun_lon"])
        sun_lat.append(ecl_dict["sun_lat"])  # sun.alt
        moon_lon.append(ecl_dict["moon_lon"])
        moon_lat.append(ecl_dict["moon_lat"])

        # sun_dist.append(ecl_dict["sun_dist"])
        # moon_dist.append(ecl_dict["moon_dist"])

        sun_dict, sun_text = sr.main_sun_rise_sett(observer=observer)
        sun_angle.append(sun_dict["sun_angle"])


    # print(sun_lon)
    # print(sun_lat)
    # print(moon_lon)
    # print(sun_angle.__len__())

    y = np.array(sun_angle)
    # y = np.power(sun_angle, 2)

    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(4, 7))
    fig.subplots_adjust(top=0.95, bottom=.05, left=0.15, right=.95, wspace=0.00)
    # ************************************************************************

    arr_size = len(y)
    Z = np.zeros(arr_size * 3).reshape(arr_size, 3)
    dates = np.ones(arr_size)
    # Z[:, 0] = y
    Z[:, 1] = y
    # Z[:, 2] = y
    # print(Z)

    axs[0].grid(axis='y')
    im = axs[0].imshow(Z, interpolation='bicubic',  # 'nearest', 'bilinear', 'bicubic'
                    cmap=cm.RdYlGn,  # gray
                    origin='lower',
                    extent=[-days / 4, days / 4, -days, days],
                    vmax=Z.max(), vmin=Z.min())

    axs[0].yaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
    axs[0].yaxis.set_major_locator(mdates.DayLocator(interval=1))

    # /////////////////////////////////////////////////////////////
    # Create the colormap
    colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (0.7, 0.4, 0.1)]  # R -> G -> B
    my_cmap = LinearSegmentedColormap.from_list('my_list', colors, N=100)

    gradient = np.linspace(0, 1, 20)
    gradient = np.vstack((gradient, gradient))

    axs[1].set_title(f'my_list', fontsize=10)
    # axs[1].grid()
    # axs[1].swap_axes()
    # axs[1].invert_yaxis()
    axs[1].imshow(gradient, aspect='auto', cmap=my_cmap)

    res = plt.savefig(file_name)
    print(res)

    plt.show()


if __name__ == '__main__':

    geo_name = 'Mragowo'
    # geo_name = 'Boston'
    # geo_name = 'Kharkiv'

    # local_unaware_datetime = datetime.strptime("1976-07-13 02:37:21", geo.dt_format_rev)  # "%Y-%m-%d %H:%M:%S"
    local_unaware_datetime = datetime.today()

    observer_obj, observer_text = geo.main_observer(geo_name=geo_name, unaware_datetime=local_unaware_datetime)
    text = ""
    text += observer_text[0]
    # text += observer_text[1]
    text += observer_text[2]
    # ##########################################################

    plot_color_of_the_days(observer=observer_obj, days=4, file_name="plot_astro_summary.png")
