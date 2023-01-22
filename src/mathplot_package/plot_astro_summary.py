
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
import src.mathplot_package._plot_Lunation as pl
import src.mathplot_package._plot_recordWeather as pe
import src.boto3_package.mainDB_weather as b3w


from babel.dates import format_datetime


def plot_color_of_the_days(observer=None, days=1., file_name="plot_astro_summary.png"):
    # print("unaware date2num=", mdates.date2num(observer.get_unaware))

    begin_unaware = observer.get_unaware - timedelta(days=days)
    end_unaware = observer.get_unaware + timedelta(days=days)
    # print(begin_unaware, " - ", end_unaware)

    unaware_dates = np.linspace(begin_unaware.timestamp(), end_unaware.timestamp(), 1000)

    moon_element = []
    moon_lunat = []
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
    annot_moon_elem = {}
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



        lunation = md.get_lunation(observer=observer)
        moon_lunat.append(lunation)



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
                elem = zd.elements_full_ukr[int(m_long / 30) % 4]
                # print(ecl_dict["moon_lon"], zd.format_zodiacal_longitude((ecl_dict["moon_lon"])), sign)
                annot_moon_zod[sign] = mdates.date2num(observer.get_unaware)
                annot_moon_elem[elem] = mdates.date2num(observer.get_unaware)
        else:
            if (m_long % 30) == 16:
                blocked_m_long = False



        moon_element.append(ecl_dict["moon_lon"] % 90)



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
    # fig, axes = plt.subplots(nrows=1, ncols=5, figsize=(5., 9.54))  # Figure(400x754)
    WW = 5.0
    HH = 9.8
    fig = plt.figure(figsize=(WW, HH))  # Figure(400x754)
    print(repr(fig), str(fig))
    fig.subplots_adjust(top=0.975, bottom=.025, left=0.0, right=1., wspace=0.00)

    axe0 = plt.subplot2grid((1, 10), (0, 0), colspan=1)
    axe0.set_title(f'Тиск', fontsize=10)

    axe1 = plt.subplot2grid((1, 10), (0, 1), colspan=1)
    axe1.set_title(f'Стихії', fontsize=10)

    axe2 = plt.subplot2grid((1, 10), (0, 2), colspan=1)
    axe2.set_title(f'Фази', fontsize=10)

    axe3 = plt.subplot2grid((1, 10), (0, 3), colspan=4)
    axe3.set_title(f'Сонце   ===   Місяць', loc='center', fontsize=10)

    axe4 = plt.subplot2grid((1, 10), (0, 7), colspan=2)
    axe4.set_title(f'Зодіак', fontsize=10)

    axe5 = plt.subplot2grid((1, 10), (0, 9), colspan=1)
    axe5.set_title(f'-', fontsize=10)


    axes = (axe0, axe1, axe2, axe3, axe4, axe5)
    for axe in axes:
        # print(str(axe), (axe.bbox.width, axe.bbox.height))
        axe.grid(axis='y', color='white', linestyle='-', linewidth=0.2)
        # axe.axis('off')
        axe.set_xticks([])
        # axe.set_yticks([])
        axe.set_yticklabels([])  # remove labels but keep grid
        # axe1.set_frame_on(True)
        # for spine in axe4.spines.values():
        #     spine.set_visible(False)
        axe.yaxis.set_major_locator(mdates.DayLocator(interval=1))


    arr_size = len(lbl_dates)

    # vert_range = lbl_dates[-1] - lbl_dates[0]
    vert_range = days * 2


    # ///////////////////////  WEATHER  /////////////////////////////////////

    print(begin_unaware, " - ", end_unaware)            # 2023-01-18 10:22:27.276605  -  2023-01-25 10:22:27.276605

    list_of_items = b3w.recordWeather_table.table_query(_pk="442763659#REP",
                                                        _between_low=str(begin_unaware),    # "2021-01-21 14:41:49"
                                                        _between_high=str(end_unaware)
                                                        )
    # pprint(list_of_items)


    data_dict, avg = b3w.main_query_filter(list_of_items, attr="weather", field="P")
    data_len = len(data_dict)
    print('len=', data_len, data_dict)


    # Create avg array of weather data
    # avg = 770    # np.average(ycolors)
    weather_array = np.full(arr_size, avg)


    # Modify avg array with weather data
    for item in data_dict:

        dt_cur = datetime.strptime(item, geo.dt_format_rev)

        # Find and replace origin element
        desired_date = mdates.date2num(dt_cur)
        idx = min(range(len(lbl_dates)), key=lambda i: abs(lbl_dates[i] - desired_date))

        value = data_dict[item]
        # print(item, dt_cur, desired_date, idx, value)

        # Replace value
        # weather_array[idx] = value
        weather_array[idx:idx+8] = value
        # weather_array[idx] = np.full(10, value)

    # print(weather_array)

    Z = np.zeros(arr_size).reshape(arr_size, 1)
    Z[:, 0] = weather_array

    horiz_half = vert_range / axe1.bbox.height * axe1.bbox.width / 2

    im = axe0.imshow(Z,
                     interpolation='bicubic',
                     aspect='auto',
                     cmap='summer',
                     origin='upper',
                     extent=[-horiz_half, horiz_half, lbl_dates[-1], lbl_dates[0]],
                     vmax=Z.max(), vmin=Z.min()
                     )



    # //////////////////////  ELEMENTS  /////////////////////////////////////
    elements_array = np.mod(moon_lon, 120)

    gcolumn = 1
    Z = np.zeros(arr_size * gcolumn).reshape(arr_size, gcolumn)
    Z[:, 0] = elements_array

    horiz_half = vert_range / axe1.bbox.height * axe1.bbox.width / 2

    _plot_annotations_of_moon_elements(annotation_elem_dict=annot_moon_elem, axe=axe1, horiz_range=horiz_half)

    CYCLING_OVERLAP = 120 * (2 / 4) / 2 * pz.OVERLAP_COEF
    im = axe1.imshow(Z,
                     interpolation='nearest',
                     cmap=pz.elements_cmap,
                     origin='upper',
                     extent=[-horiz_half, horiz_half, lbl_dates[-1], lbl_dates[0]],
                     # vmin=0.0, vmax=120.0,
                     vmin=0 - CYCLING_OVERLAP, vmax=120 + CYCLING_OVERLAP,
                     )



    # //////////////////////  LUNATION  /////////////////////////////////////

    moon_lun = np.array(moon_lunat)
    # moon_lun = np.array(moon_element)
    # moon_lun = np.linspace(10, 200, 1000)
    # sun_zod = np.array(sun_lon)

    gcolumn = 1
    Z = np.zeros(arr_size * gcolumn).reshape(arr_size, gcolumn)
    Z[:, 0] = moon_lun

    horiz_half = vert_range / axe2.bbox.height * axe2.bbox.width / 2
    _plot_annotations_of_moon_phases(observer=observer, days=days, axe=axe2, horiz_range=horiz_half)

    CYCLING_OVERLAP = 0.239
    im = axe2.imshow(Z,
                     interpolation='nearest',
                     cmap=pl.lunation_cmap,
                     origin='upper',
                     extent=[-horiz_half, horiz_half, lbl_dates[-1], lbl_dates[0]],
                     # vmin=0.0, vmax=1.0,
                     # vmin=-0.239, vmax=1.239,
                     vmin=0-CYCLING_OVERLAP, vmax=1+CYCLING_OVERLAP,
                     )


    # ////////////////////  SUN MOON DAYS  //////////////////////////////////

    s_angle = np.array(sun_angle)
    ycolors = ps.convert_colors(in_y_list=s_angle, thresh=0.3)
    s_angle = np.array(ycolors)

    m_angle = np.array(moon_angle)
    ycolors = ps.convert_colors(in_y_list=m_angle, thresh=0.3)
    m_angle = np.array(ycolors)

    gcolumn = 5
    Z = np.zeros(arr_size * gcolumn).reshape(arr_size, gcolumn)
    Z[:, 0] = s_angle
    Z[:, 1] = s_angle
    Z[:, 2] = (s_angle + m_angle) / 2
    Z[:, 3] = m_angle
    Z[:, 4] = m_angle

    horiz_half = vert_range / axe3.bbox.height * axe3.bbox.width / 2

    _plot_annotations_of_sun_days(observer=observer, days=days, axe=axe3, horiz_range=horiz_half)
    _plot_annotations_of_moon_days(observer=observer, days=days, axe=axe3, horiz_range=horiz_half)

    im = axe3.imshow(Z,
                     interpolation='nearest',  # 'nearest', 'bilinear', 'bicubic'
                     cmap="twilight_shifted",
                     origin='upper',
                     extent=[-horiz_half, horiz_half, lbl_dates[-1], lbl_dates[0]],
                     vmin=Z.min(), vmax=Z.max()
                     )


    # ///////////////////////  ZODIAC  //////////////////////////////////////

    moon_zod = np.array(moon_lon)
    sun_zod = np.array(sun_lon)

    gcolumn = 2
    Z = np.zeros(arr_size * gcolumn).reshape(arr_size, gcolumn)
    Z[:, 0] = moon_zod
    # Z[:, 1] = moon_zod
    # Z[:, 2] = moon_zod
    # Z[:, 3] = sun_zod
    Z[:, 1] = sun_zod

    horiz_half = vert_range / axe4.bbox.height * axe4.bbox.width / 2

    _plot_annotations_of_zodiacs(annotation_moon_dict=annot_moon_zod,
                                 annotation_sun_dict=annot_sun_zod,
                                 axe=axe4,
                                 horiz_range=horiz_half)

    CYCLING_OVERLAP = 360 * (2 / 12) / 2 * pz.OVERLAP_COEF
    im = axe4.imshow(Z,
                     interpolation='nearest',  # 'nearest', 'bilinear', 'bicubic'
                     cmap=pz.zodiac_cmap,
                     origin='upper',
                     extent=[-horiz_half, horiz_half, lbl_dates[-1], lbl_dates[0]],
                     # vmin=0, vmax=360,
                     vmin=0 - CYCLING_OVERLAP, vmax=360 + CYCLING_OVERLAP,
                     )


    # //////////////////////  FOOTPRINT  ////////////////////////////////////

    axe0.set_xlabel("Геолокація: " + observer._geo_name,
                    labelpad=6,
                    loc='left',
                    fontsize=9
                    )

    axe5.set_xlabel("" + format_datetime(observer.restore_unaware(), "d MMMM YYYY р., EEE ", locale='uk_UA'),
                    labelpad=6,
                    loc='right',
                    fontsize=9
                    )




    # ***********************************************************************
    res = plt.savefig(file_name)
    # print(res)

    plt.show()


def _plot_annotations_of_sun_days(observer=None, days=1., axe=None, horiz_range=1):

    observer.restore_unaware()
    begin_unaware = observer.get_unaware - timedelta(days=days)
    end_unaware = observer.get_unaware + timedelta(days=days)
    cur_unaware = begin_unaware
    # print(begin_unaware, " - ", end_unaware)

    while end_unaware > cur_unaware:

        if cur_unaware == begin_unaware:                        # init pass
            pass
        else:
            cur_unaware = cur_unaware + timedelta(days=1)       # next position of annotation

        observer.unaware_update_utc12(cur_unaware)              # adjusting calculation (between rise and setting)
        sun_dict, sun_text = sr.main_sun_rise_sett(observer=observer)   # modified observer
        zenit_day = ephem.Date((sun_dict['sun_sett'] + sun_dict['sun_rise']) / 2)
        cur_unaware = zenit_day.datetime()

        annot_text = format_datetime(cur_unaware, "d MMM EEE", locale='uk_UA')
        # annot_text = str(cur_unaware.strftime(geo.dt_format_plot))
        coords = (-0.6 * horiz_range, mdates.date2num(cur_unaware))

        axe.annotate(annot_text,
                     xy=coords,
                     fontsize=8.5,
                     horizontalalignment='center',
                     verticalalignment='top'
                     )


def _plot_annotations_of_moon_days(observer=None, days=1., axe=None, horiz_range=1):

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
        coords = (0.6 * horiz_range, mdates.date2num(cur_unaware))

        axe.annotate(annot_text,
                         xy=coords,
                         fontsize=8,
                         horizontalalignment='center',
                         verticalalignment='center'
                         )


def _plot_annotations_of_moon_phases(observer=None, days=1., axe=None, horiz_range=1):

    observer.restore_unaware()
    begin_unaware = observer.get_unaware - timedelta(days=days)
    end_unaware = observer.get_unaware + timedelta(days=days)
    cur_unaware = begin_unaware

    while end_unaware > cur_unaware:
        if cur_unaware == begin_unaware:                            # init pass
            pass                                                    # init calculation
        else:
            cur_unaware = cur_unaware + timedelta(days=29.53/2)     # next calculation

        observer.unaware_update_utc(cur_unaware)
        moonph_dict, moon_text = md.main_moon_phase(observer=observer)
        lbl_moon_phmiddle = ephem.Date((moonph_dict['prev_utc'] + moonph_dict['next_utc']) / 2)
        cur_unaware = lbl_moon_phmiddle.datetime()

        annot_text = str(moonph_dict["prev"]).replace(" ", "\n")
        coords = (-0.0 * horiz_range, ephem.Date(moonph_dict['prev_utc']).datetime())
        # print(annot_text, coords)
        axe.annotate(annot_text,
                     xy=coords,
                     fontsize=7.5,
                     horizontalalignment='center',
                     verticalalignment='center',
                     )
        annot_text = str(moonph_dict["next"]).replace(" ", "\n")
        coords = (-0.0 * horiz_range, ephem.Date(moonph_dict['next_utc']).datetime())
        # print(annot_text, coords)
        axe.annotate(annot_text,
                     xy=coords,
                     fontsize=7.5,
                     horizontalalignment='center',
                     verticalalignment='center',
                     )


def _plot_annotations_of_moon_elements(annotation_elem_dict=None, axe=None, horiz_range=1):

    for i in annotation_elem_dict:
        # print(i, annotation_elem_dict[i])

        annot_text = str(i).replace(" ", "\n")
        coords = (-0.0 * horiz_range, annotation_elem_dict[i])

        axe.annotate(annot_text,
                     xy=coords,
                     fontsize=9,
                     horizontalalignment='center',
                     verticalalignment='center'
                     )


def _plot_annotations_of_zodiacs(annotation_moon_dict=None, annotation_sun_dict=None, axe=None, horiz_range=1):

    for i in annotation_moon_dict:
        # print(i, annotation_moon_dict[i])

        annot_text = str(i)
        coords = (-0.5 * horiz_range, annotation_moon_dict[i])

        axe.annotate(annot_text,
                     xy=coords,
                     fontsize=9,
                     horizontalalignment='center',
                     verticalalignment='center'
                     )

    for i in annotation_sun_dict:
        # print(i, annotation_sun_dict[i])

        annot_text = str(i)
        coords = (0.5 * horiz_range, annotation_sun_dict[i])

        axe.annotate(annot_text,
                     xy=coords,
                     fontsize=9,
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
    # observer_obj.unaware_update_utc(in_unaware_datetime)
    # plot_color_of_the_days(observer=observer_obj, days=6, file_name="plot_astro_summary.png")
    #
    # observer_obj.unaware_update_utc(in_unaware_datetime)
    # plot_color_of_the_days(observer=observer_obj, days=10, file_name="plot_astro_summary.png")
    #
    # observer_obj.unaware_update_utc(in_unaware_datetime)
    # plot_color_of_the_days(observer=observer_obj, days=15, file_name="plot_astro_summary.png")
