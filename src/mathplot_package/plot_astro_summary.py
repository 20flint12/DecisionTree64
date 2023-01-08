
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
import src.ephem_routines.ephem_package.moon_day as md

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

    blocked_m_long = False
    blocked_s_long = False
    annot_moon_zod = {}
    annot_sun_zod = {}
    last_sun_str = ""

    for cur_un_dt in unaware_dates:

        observer.unaware_update_utc((datetime.fromtimestamp(cur_un_dt)))
        lbl_dates.append(mdates.date2num(observer.get_unaware))
        # print(cur_un_dt, " | ", observer.get_unaware, " / ", observer.get_utc)


        # if unaware_dates.index(cur_un_dt) == 0:
        # if np.where(unaware_dates == cur_un_dt)[0] == 0:
        #     print(zd.format_zodiacal_longitude())
        # else:
        #     print(zd.format_zodiacal_longitude())


        ecl_dict, ecl_text = zd.main_zodiac_sun_moon(observer=observer)     # unmodified observer
        sun_lon.append(ecl_dict["sun_lon"])
        sun_lat.append(ecl_dict["sun_lat"])
        moon_lon.append(ecl_dict["moon_lon"])
        moon_lat.append(ecl_dict["moon_lat"])
        # sun_dist.append(ecl_dict["sun_dist"])
        # moon_dist.append(ecl_dict["moon_dist"])



        m_long = int(ecl_dict["moon_lon"])
        if not blocked_m_long:
            if (m_long % 30) == 15:
                blocked_m_long = True

                sign = zd.zodiac_full_ukr[int(m_long / 30)]
                # print(ecl_dict["moon_lon"], zd.format_zodiacal_longitude((ecl_dict["moon_lon"])), sign)
                annot_moon_zod[sign] = mdates.date2num(observer.get_unaware)
        else:
            if (m_long % 30) == 16:
                blocked_m_long = False



        res_sun_str = zd.format_zodiacal_longitude((ecl_dict["sun_lon"]))
        # print(ecl_dict["sun_lon"], res_sun_str)
        if res_sun_str != last_sun_str:
            last_sun_str = res_sun_str

            if not blocked_s_long:      # bypass first annotation
                blocked_s_long = True
            else:
                annot_sun_zod[res_sun_str] = mdates.date2num(observer.get_unaware)



        salt_dict, alt_text = sr.main_sun_altitude(observer=observer)       # unmodified observer
        sun_angle.append(salt_dict["sun_angle"])

        malt_dict, alt_text = zd.main_moon_altitude(observer=observer)      # unmodified observer
        moon_angle.append(malt_dict["moon_angle"])

        # print(cur_un_dt, " | ", observer.get_unaware, " \ ", observer.get_utc)

    # ************************************************************************
    plt.style.use('_mpl-gallery-nogrid')
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(4, 7))
    fig.subplots_adjust(top=0.95, bottom=.05, left=0.15, right=.95, wspace=0.00)
    print(fig, repr(axes), str(axes))

    # ////////////////////  SUN MOON DAYS  //////////////////////////////////
    # print(lbl_dates)
    # print(annot_moon_zod)
    # print(moon_lon)

    s_angle = np.array(sun_angle)
    ycolors = ps.convert_colors(in_y_list=s_angle, thresh=0.35)
    s_angle = np.array(ycolors)

    m_angle = np.array(moon_angle)
    ycolors = ps.convert_colors(in_y_list=m_angle, thresh=0.35)
    m_angle = np.array(ycolors)

    arr_size = len(s_angle)
    gcolumn = 5
    Z = np.zeros(arr_size * gcolumn).reshape(arr_size, gcolumn)
    Z[:, 0] = s_angle
    Z[:, 1] = s_angle
    Z[:, 2] = (s_angle + m_angle) / 2
    Z[:, 3] = m_angle
    Z[:, 4] = m_angle

    axes[0].set_title(f'===', fontsize=10)
    axes[0].set_title('  Сонце', loc='left', fontsize=10)
    axes[0].set_title('Місяць ', loc='right', fontsize=10)
    axes[0].grid(axis='y', color='white', linestyle='-', linewidth=0.3)
    # axes[0].axis('off')
    axes[0].set_xticks([])

    axes[0].yaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
    axes[0].yaxis.set_major_locator(mdates.DayLocator(interval=1))
    # axes[0].yaxis.set_label_coords(0.5, 0.35)

    _plot_annotations_of_sun_days(observer=observer, days=days, axes=axes)
    _plot_annotations_of_moon_days(observer=observer, days=days, axes=axes)

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

    axes[1].set_title(f'Зодіак', fontsize=10)
    # axes[1].axis('off')
    axes[1].grid(axis='y', color='white', linestyle='--', linewidth=0.2)
    axes[1].set_xticks([])
    axes[1].set_yticklabels([])     # remove labels but keep grid

    # axes[1].yaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
    axes[1].yaxis.set_major_locator(mdates.DayLocator(interval=1))

    _plot_annotations_of_zodiacs(annotation_moon_dict=annot_moon_zod, annotation_sun_dict=annot_sun_zod, axes=axes)

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


def _plot_annotations_of_sun_days(observer=None, days=1., axes=None):

    observer.restore_unaware()
    begin_unaware = observer.get_unaware - timedelta(days=days)
    end_unaware = observer.get_unaware + timedelta(days=days)
    cur_unaware = begin_unaware
    # print(begin_unaware, " - ", end_unaware)

    while end_unaware > cur_unaware:

        if cur_unaware == begin_unaware:                            # init pass
            observer.unaware_update_utc12(begin_unaware)            # init calculation (at noon of the first day)
            sun_dict, sun_text = sr.main_sun_rise_sett(observer=observer)   # modified observer
            zenit_begin = ephem.Date((sun_dict['sun_sett'] + sun_dict['sun_rise']) / 2)
            cur_unaware = zenit_begin.datetime()
        else:
            cur_unaware = cur_unaware + timedelta(days=1)           # next position of annotation

        annot_text = format_datetime(cur_unaware, "d MMM EEE", locale='uk_UA')
        # annot_text = str(cur_unaware.strftime(geo.dt_format_plot))
        coords = (-0.84, mdates.date2num(cur_unaware))

        axes[0].annotate(annot_text,
                         xy=coords,
                         fontsize=8,
                         horizontalalignment='left',
                         verticalalignment='top'
                         )

    axes[0].set_xlabel("Геолокація: " + observer._geo_name,
                       labelpad=8,
                       loc='right',
                       fontsize=9
                       )

    axes[1].set_xlabel("" + format_datetime(observer.restore_unaware(), "d MMMM YYYY р., EEEE", locale='uk_UA'),
                       labelpad=8,
                       loc='right',
                       fontsize=9
                       )


def _plot_annotations_of_moon_days(observer=None, days=1., axes=None):

    observer.restore_unaware()
    begin_unaware = observer.get_unaware - timedelta(days=days)
    end_unaware = observer.get_unaware + timedelta(days=days)
    cur_unaware = begin_unaware

    while end_unaware > cur_unaware:
        if cur_unaware == begin_unaware:                            # init pass
            pass                                                    # init calculation
        else:
            cur_unaware = cur_unaware + timedelta(days=24.5 / 24)   # next calculation

        observer.unaware_update_utc(cur_unaware)
        moon_dict, moon_text = md.main_moon_day(observer=observer)  # modified observer
        lbl_moon_noon = ephem.Date((moon_dict['moon_sett'] + moon_dict['moon_rise']) / 2)
        cur_unaware = lbl_moon_noon.datetime()

        annot_text = str(moon_dict["moon_day"]) + " міс. д."
        coords = (0.2, mdates.date2num(cur_unaware))

        axes[0].annotate(annot_text,
                         xy=coords,
                         fontsize=8,
                         horizontalalignment='left',
                         verticalalignment='center'
                         )


def _plot_annotations_of_zodiacs(annotation_moon_dict=None, annotation_sun_dict=None, axes=None):
    for i in annotation_moon_dict:
        # print(i, annotation_moon_dict[i])

        annot_text = str(i)
        coords = (-0.4, annotation_moon_dict[i])

        axes[1].annotate(annot_text,
                         xy=coords,
                         fontsize=10,
                         horizontalalignment='center',
                         verticalalignment='center'
                         )

    for i in annotation_sun_dict:
        # print(i, annotation_sun_dict[i])

        annot_text = str(i)
        coords = (0.5, annotation_sun_dict[i])

        axes[1].annotate(annot_text,
                         xy=coords,
                         fontsize=9.5,
                         horizontalalignment='center',
                         verticalalignment='center'
                         )


if __name__ == '__main__':

    geo_name = 'Kremenchuk'
    # geo_name = 'Mragowo'
    # geo_name = 'Boston'
    # geo_name = 'Kharkiv'

    # in_unaware_datetime = datetime.strptime("1976-07-25 02:37:21", geo.dt_format_rev)  # "%Y-%m-%d %H:%M:%S"
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
