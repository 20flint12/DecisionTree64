
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

import src.mathplot_package._plot_Sun_Moon as ps
import src.mathplot_package._plot_Zodiac as pz

from babel.dates import format_datetime
# format_datetime(datetime.today(), locale='uk_UA')


def plot_color_of_the_days(observer=None, days=1., file_name="plot_astro_summary.png"):
    # print("unaware date2num=", mdates.date2num(observer.get_unaware))

    begin_unaware = observer.get_unaware - timedelta(days=days)
    end_unaware = observer.get_unaware + timedelta(days=days)
    # print(begin_unaware, " - ", end_unaware)
    unaware_dates = np.linspace(begin_unaware.timestamp(), end_unaware.timestamp(), 1000)

    sun_lon = []
    sun_lat = []
    moon_lon = []
    moon_lat = []
    # sun_dist = []
    # moon_dist = []
    sun_angle = []
    moon_angle = []
    lbl_dates = []
    for cur_un_dt in unaware_dates:

        observer.unaware_update_utc((datetime.fromtimestamp(cur_un_dt)))
        lbl_dates.append(mdates.date2num(observer.get_unaware))
        # print(cur_un_dt, " | ", observer.get_unaware, " / ", observer.get_utc)

        ecl_dict, ecl_text = zd.main_zodiac_sun_moon(observer=observer)
        sun_lon.append(ecl_dict["sun_lon"])
        sun_lat.append(ecl_dict["sun_lat"])
        moon_lon.append(ecl_dict["moon_lon"])
        moon_lat.append(ecl_dict["moon_lat"])
        # sun_dist.append(ecl_dict["sun_dist"])
        # moon_dist.append(ecl_dict["moon_dist"])

        # sun_dict, sun_text = sr.main_sun_rise_sett(observer=observer)

        salt_dict, alt_text = sr.main_sun_altitude(observer=observer)
        sun_angle.append(salt_dict["sun_angle"])

        malt_dict, alt_text = zd.main_moon_altitude(observer=observer)
        moon_angle.append(malt_dict["moon_angle"])

        # print(cur_un_dt, " | ", observer.get_unaware, " \ ", observer.get_utc)

    # ************************************************************************
    plt.style.use('_mpl-gallery-nogrid')
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(4, 7))
    fig.subplots_adjust(top=0.95, bottom=.05, left=0.15, right=.95, wspace=0.00)
    print(fig, repr(axes), str(axes))

    # ////////////////////  SUN MOON DAYS  //////////////////////////////////
    # print(lbl_dates)
    # print(sun_lat)
    # print(moon_lon)
    # print(sun_angle.__len__())

    moon_zod = np.array(sun_angle)
    ycolors = ps.convert_colors(in_y_list=moon_zod, thresh=0.35)
    moon_zod = np.array(ycolors)

    sun_zod = np.array(moon_angle)
    ycolors = ps.convert_colors(in_y_list=sun_zod, thresh=0.35)
    sun_zod = np.array(ycolors)

    arr_size = len(moon_zod)
    gcolumn = 5
    Z = np.zeros(arr_size * gcolumn).reshape(arr_size, gcolumn)
    Z[:, 0] = moon_zod
    Z[:, 1] = moon_zod
    Z[:, 2] = (moon_zod + sun_zod) / 2
    Z[:, 3] = sun_zod
    Z[:, 4] = sun_zod
    # print(Z)

    # axes[0].set_title(f'Sun    ===   Moon', fontsize=10)
    axes[0].set_title(f'===', fontsize=10)
    axes[0].set_title('  Сонце', loc='left', fontsize=10)
    axes[0].set_title('Місяць  ', loc='right', fontsize=10)
    axes[0].grid(axis='y', color='white', linestyle='-', linewidth=0.2)
    # axes[0].axis('off')
    axes[0].set_xticks([])

    axes[0].yaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
    axes[0].yaxis.set_major_locator(mdates.DayLocator(interval=1))
    # axes[0].yaxis.set_label_coords(0.5, 0.35)

    _plot_annotations_of_the_days(observer=observer_obj, days=days, axes=axes)

    im = axes[0].imshow(Z,
                        interpolation='nearest',  # 'nearest', 'bilinear', 'bicubic'
                        cmap="twilight_shifted",
                        origin='upper',
                        extent=[-days/4, days/4, lbl_dates[-1], lbl_dates[0]],
                        vmin=Z.min(), vmax=Z.max()
                        )

    # ///////////////////////  ZODIAC  //////////////////////////////////////
    # print(len(moon_lon), max(moon_lon), min(moon_lon))

    moon_zod = np.array(moon_lon)
    sun_zod = np.array(sun_lon)

    arr_size = len(moon_zod)
    gcolumn = 5
    Z = np.zeros(arr_size * gcolumn).reshape(arr_size, gcolumn)
    Z[:, 0] = moon_zod
    Z[:, 1] = moon_zod
    Z[:, 2] = moon_zod
    Z[:, 3] = sun_zod
    Z[:, 4] = sun_zod

    axes[1].set_title(f'Zodiac', fontsize=10)
    # axes[1].axis('off')
    axes[1].grid(axis='y', color='white', linestyle='--', linewidth=0.2)
    axes[1].set_xticks([])
    axes[1].set_yticklabels([])     # remove labels but keep grid

    # axes[1].yaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
    axes[1].yaxis.set_major_locator(mdates.DayLocator(interval=1))

    im = axes[1].imshow(Z,
                        interpolation='nearest',  # 'nearest', 'bilinear', 'bicubic'
                        cmap=pz.zodiac_cmap,
                        origin='upper',
                        extent=[-days/4, days/4, lbl_dates[-1], lbl_dates[0]],
                        vmin=0, vmax=360
                        )

    # ***********************************************************************
    res = plt.savefig(file_name)
    # print(res)

    plt.show()


def _plot_annotations_of_the_days(observer=None, days=2, axes=None):

    observer.restore_unaware()
    # print("unaware date2num=", mdates.date2num(observer.get_unaware))

    begin_unaware = observer.get_unaware - timedelta(days=days)
    end_unaware = observer.get_unaware + timedelta(days=days)
    # print(begin_unaware, " - ", end_unaware)

    # получить метку на 12 часов первого дня диапазона
    observer.unaware_update_utc12(begin_unaware)
    sun_dict, sun_text = sr.main_sun_rise_sett(observer=observer)
    lbl_begin = ephem.Date((sun_dict['sun_sett']+sun_dict['sun_rise'])/2)
    cur_unaware = lbl_begin.datetime()
    # print(sun_dict, lbl_begin, cur_unaware)

    while end_unaware > cur_unaware:

        date_str = format_datetime(cur_unaware, "d MMM EEE", locale='uk_UA')
        # date_str = str(cur_unaware.strftime(geo.dt_format_plot))

        coords = (-0.80, mdates.date2num(cur_unaware))

        axes[0].annotate(date_str,
                         xy=coords,
                         fontsize=8,
                         horizontalalignment='left',
                         verticalalignment='top'
                         )

        cur_unaware = cur_unaware + timedelta(days=1)
        # print(date_str)




if __name__ == '__main__':

    geo_name = 'Mragowo'
    # geo_name = 'Boston'
    # geo_name = 'Kharkiv'

    # local_unaware_datetime = datetime.strptime("1976-07-20 02:37:21", geo.dt_format_rev)  # "%Y-%m-%d %H:%M:%S"
    in_unaware_datetime = datetime.today()
    observer_obj = geo.Observer(geo_name=geo_name, unaware_datetime=in_unaware_datetime)
    text = ""
    text += str(observer_obj)
    # print(text)
    # #######################################################################################
    plot_color_of_the_days(observer=observer_obj, days=3.5, file_name="plot_astro_summary.png")

    # observer_obj.unaware_update_utc(in_unaware_datetime)
    # plot_color_of_the_days(observer=observer_obj, days=3, file_name="plot_astro_summary.png")
    #
    # observer_obj.unaware_update_utc(in_unaware_datetime)
    # plot_color_of_the_days(observer=observer_obj, days=5, file_name="plot_astro_summary.png")
    #
    # # observer_obj.unaware_update_utc(in_unaware_datetime)
    # plot_color_of_the_days(observer=observer_obj, days=6, file_name="plot_astro_summary.png")
    #
    # observer_obj.unaware_update_utc(in_unaware_datetime)
    # plot_color_of_the_days(observer=observer_obj, days=10, file_name="plot_astro_summary.png")
    #
    # observer_obj.unaware_update_utc(in_unaware_datetime)
    # plot_color_of_the_days(observer=observer_obj, days=15, file_name="plot_astro_summary.png")
