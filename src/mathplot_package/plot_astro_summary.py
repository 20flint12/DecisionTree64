import ephem
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


def convert_colors(in_y_list=None, thresh=0.2):
    """
    :param in_y_list:
    :param thresh:    threshold
    :return:
    """

    # y_max = (max(in_y_list) + abs(min(in_y_list))) / 2
    y_max = min(max(in_y_list), abs(min(in_y_list)))

    y_thr = y_max * thresh
    print("y_max=", y_max, " y_thr=", y_thr)

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

    print("len=", len(res_color_list), " min=", min(res_color_list), " max=", max(res_color_list))

    return res_color_list


def plot_color_of_the_days(observer=None, days=1, file_name="plot_astro_summary.png"):
    # print("=======", observer)
    begin_date = observer.utc - timedelta(days=days)
    # print(begin_date, begin_date.timestamp(), mdates.epoch2num(begin_date))
    # begin_date = mdates.epoch2num(begin_date)
    end_date = observer.utc + timedelta(days=days)
    # end_date = mdates.epoch2num(end_date)
    # print(begin_date, " - ", end_date)
    dates = np.linspace(begin_date.timestamp(), end_date.timestamp(), 1000)
    # dates = mdates.epoch2num(dates)

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
    moon_angle = []
    lbl_dates = []
    for cur_dt in dates:

        observer.unaware_update_utc((datetime.fromtimestamp(cur_dt)))
        lbl_dates.append(mdates.date2num(observer.unaware))
        # print(cur_dt, " | ", observer.utc, " / ", observer.place.date)
        ecl_dict, ecl_text = zd.main_zodiac_sun_moon(observer=observer)
        sun_lon.append(ecl_dict["sun_lon"])
        sun_lat.append(ecl_dict["sun_lat"])  # sun.alt
        moon_lon.append(ecl_dict["moon_lon"])
        moon_lat.append(ecl_dict["moon_lat"])
        # sun_dist.append(ecl_dict["sun_dist"])
        # moon_dist.append(ecl_dict["moon_dist"])

        # observer.utc_update_utc(datetime.fromtimestamp(cur_dt))
        # print(observer)

        sun_dict, sun_text = sr.main_sun_rise_sett(observer=observer)

        alt_dict, alt_text = sr.main_sun_altitude(observer=observer)
        sa = alt_dict["sun_angle"]
        sun_angle.append(sa)

        alt_dict, alt_text = zd.main_moon_altitude(observer=observer)
        moon_angle.append(alt_dict["moon_angle"])

        # print(cur_dt, " | ", observer.utc, " \ ", observer.place.date)


    # print(lbl_dates)
    # print(sun_lat)
    # print(moon_lon)
    # print(sun_angle.__len__())

    # y = np.array(sun_angle)
    # y *= 0.5/y.max() + 0.5
    # y = np.power(sun_angle, 4)
    # y2 = np.array(moon_angle)
    # y2 = np.power(moon_angle, 4)

    # *************************************
    ys = np.array(sun_angle)
    print(len(ys), np.amin(ys), np.amax(ys))
    ycolors = convert_colors(in_y_list=ys, thresh=0.35)
    ys = np.array(ycolors)

    y2s = np.array(moon_angle)
    print(len(y2s), np.amin(y2s), np.amax(y2s))
    ycolors = convert_colors(in_y_list=y2s, thresh=0.35)
    y2s = np.array(ycolors)

    # yss = ys + y2s
    # print(len(yss), np.amin(yss), np.amax(yss))
    # ycolors = convert_colors(in_y_list=yss, thresh=0.35)
    # yss = np.array(ycolors)



    plt.style.use('_mpl-gallery-nogrid')
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(4, 7))
    fig.subplots_adjust(top=0.95, bottom=.05, left=0.15, right=.95, wspace=0.00)
    # ************************************************************************

    arr_size = len(ys)
    gcolumn = 5
    Z = np.zeros(arr_size * gcolumn).reshape(arr_size, gcolumn)
    Z[:, 0] = ys
    Z[:, 1] = ys
    Z[:, 2] = (ys + y2s) / 2
    Z[:, 3] = y2s
    Z[:, 4] = y2s
    # print(Z)

    axes[0].grid(axis='y')
    mdate_begin = lbl_dates[0]
    mdate_end = lbl_dates[-1]  # days+data_offset
    # axes[0].axis('off')
    im = axes[0].imshow(Z, interpolation='nearest',  # 'nearest', 'bilinear', 'bicubic'
                    # cmap=cm.RdYlGn,  # gray
                    cmap="twilight_shifted",
                    origin='lower',
                    # aspect='auto',
                    extent=[-days / 4, days / 4, mdate_begin, mdate_end],
                    vmax=Z.max(), vmin=Z.min())

    axes[0].yaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
    axes[0].yaxis.set_major_locator(mdates.DayLocator(interval=1))

    # /////////////////////////////////////////////////////////////
    # Create the colormap
    colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (0.7, 0.4, 0.1)]  # R -> G -> B
    my_cmap = LinearSegmentedColormap.from_list('my_list', colors, N=100)

    gradient = np.linspace(0, 1, 20)
    gradient = np.vstack((gradient, gradient))

    axes[1].set_title(f'my_list', fontsize=10)
    axes[1].axis('off')
    axes[1].imshow(gradient, aspect='auto', cmap=my_cmap)

    res = plt.savefig(file_name)
    print(res)

    plt.show()


if __name__ == '__main__':

    geo_name = 'Mragowo'
    # geo_name = 'Boston'
    # geo_name = 'Kharkiv'

    local_unaware_datetime = datetime.strptime("1976-07-20 02:37:21", geo.dt_format_rev)  # "%Y-%m-%d %H:%M:%S"
    # local_unaware_datetime = datetime.today()

    observer_obj = geo.Observer(geo_name=geo_name, unaware_datetime=local_unaware_datetime)
    text = ""
    text += str(observer_obj)
    # ##########################################################

    plot_color_of_the_days(observer=observer_obj, days=3, file_name="plot_astro_summary.png")
