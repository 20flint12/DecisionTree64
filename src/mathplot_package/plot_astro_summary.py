
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

import src.mathplot_package._plot_Sun_Moon as ps
import src.mathplot_package._plot_Zodiac as pz


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
        sun_lat.append(ecl_dict["sun_lat"])
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


    # ************************************************************************
    plt.style.use('_mpl-gallery-nogrid')
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(4, 7))
    fig.subplots_adjust(top=0.95, bottom=.05, left=0.15, right=.95, wspace=0.00)

    # ////////////////////  SUN MOON DAYS  //////////////////////////////////
    # print(lbl_dates)
    # print(sun_lat)
    # print(moon_lon)
    # print(sun_angle.__len__())

    ys = np.array(sun_angle)
    ycolors = ps.convert_colors(in_y_list=ys, thresh=0.35)
    ys = np.array(ycolors)

    y2s = np.array(moon_angle)
    ycolors = ps.convert_colors(in_y_list=y2s, thresh=0.35)
    y2s = np.array(ycolors)

    arr_size = len(ys)
    gcolumn = 5
    Z = np.zeros(arr_size * gcolumn).reshape(arr_size, gcolumn)
    Z[:, 0] = ys
    Z[:, 1] = ys
    Z[:, 2] = (ys + y2s) / 2
    Z[:, 3] = y2s
    Z[:, 4] = y2s
    # print(Z)

    axes[0].set_title(f'Sun    ===   Moon', fontsize=10)
    axes[0].grid(axis='y')
    # axes[0].axis('off')
    axes[0].set_xticks([])
    im = axes[0].imshow(Z,
                        interpolation='nearest',  # 'nearest', 'bilinear', 'bicubic'
                        cmap="twilight_shifted",
                        origin='lower',
                        extent=[-days / 4, days / 4, lbl_dates[0], lbl_dates[-1]],
                        vmax=Z.max(), vmin=Z.min())

    axes[0].yaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
    axes[0].yaxis.set_major_locator(mdates.DayLocator(interval=1))


    # ///////////////////////  ZODIAC  //////////////////////////////////////
    # gradient = np.linspace(0, 1, 360)
    # gradient = np.vstack((gradient, gradient))

    ys = np.array(moon_lon)
    y2s = np.array(sun_lon)

    arr_size = len(ys)
    gcolumn = 5
    Z = np.zeros(arr_size * gcolumn).reshape(arr_size, gcolumn)
    Z[:, 0] = ys
    Z[:, 1] = ys
    Z[:, 2] = ys
    Z[:, 3] = y2s
    Z[:, 4] = y2s

    axes[1].set_title(f'Zodiac', fontsize=10)
    axes[1].grid(axis='y')
    # axes[1].axis('off')
    # axes[1].imshow(gradient, aspect='auto', cmap=pz.zodiac_cmap)
    axes[1].set_xticks([])
    axes[1].set_yticks([])
    im = axes[1].imshow(Z,
                        interpolation='nearest',  # 'nearest', 'bilinear', 'bicubic'
                        cmap=pz.zodiac_cmap,
                        origin='lower',
                        extent=[-days / 4, days / 4, lbl_dates[0], lbl_dates[-1]],
                        vmax=Z.max(), vmin=Z.min())


    res = plt.savefig(file_name)
    print(res)

    plt.show()


if __name__ == '__main__':

    geo_name = 'Mragowo'
    # geo_name = 'Boston'
    # geo_name = 'Kharkiv'

    # local_unaware_datetime = datetime.strptime("1976-07-20 02:37:21", geo.dt_format_rev)  # "%Y-%m-%d %H:%M:%S"
    local_unaware_datetime = datetime.today()

    observer_obj = geo.Observer(geo_name=geo_name, unaware_datetime=local_unaware_datetime)
    text = ""
    text += str(observer_obj)
    # ##########################################################

    plot_color_of_the_days(observer=observer_obj, days=3, file_name="plot_astro_summary.png")
