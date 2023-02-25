
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
import src.mathplot_package._plot_earthWeather as pew
import src.boto3_package.mainDB_weather as b3w


import babel.dates as bd
from babel.dates import format_datetime


ANN_DAYS_OFFSET = 0.02     # actually for font high
ANN_ELEM_OFFSET = 0.03     # actually for multiline high
ANN_PHAS_OFFSET = 0.03     # actually for multiline high
ANN_ZODC_OFFSET = 0.02     # actually for multiline high


def plot_color_of_the_days(observer=None, file_name="plot_astro_summary.png", job_name=''):

    begin_unaware, end_unaware = observer.get_span_unaware
    print("\n\n===", observer.get_geo_name, "=== ", begin_unaware, "-", end_unaware)

    DATES_SIZE = 1000
    unaware_timestamp = np.linspace(begin_unaware.timestamp(), end_unaware.timestamp(), DATES_SIZE)

    unaware_array = []

    moon_element = []
    moon_lunation = []
    sun_lon = []
    sun_lat = []
    moon_lon = []
    moon_lat = []
    sun_angle = []
    moon_angle = []

    blocked_m_long = False
    blocked_s_long = False
    annot_moon_zod = {}
    annot_elements = {}
    annot_sun_zod = {}
    last_sun_str = ""

    for cur_unaware_dt in unaware_timestamp:

        observer.unaware_update_utc((datetime.fromtimestamp(cur_unaware_dt)))
        unaware_array.append(mdates.date2num(observer.get_unaware))
        # print(cur_unaware_dt, " | ", observer.get_unaware, " / ", observer.get_utc)


        # if unaware_timestamp.index(cur_unaware_dt) == 0:
        # if np.where(unaware_timestamp == cur_unaware_dt)[0] == 0:
        #     print(zd.format_zodiacal_longitude())
        # else:
        #     print(zd.format_zodiacal_longitude())



        lunation = md.get_lunation(observer=observer)
        moon_lunation.append(lunation)



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
                annot_elements[elem] = mdates.date2num(observer.get_unaware)
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

        # print(cur_unaware_dt, " | ", observer.get_unaware, " \ ", observer.get_utc)

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
    axe5.set_title(f'Темпер.', fontsize=10)


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



    #
    span = observer.get_span
    vertical_full_span = span[0] + span[1]          # = unaware_array[-1] - unaware_array[0]


    # ///////////////////////  WEATHER  /////////////////////////////////////
    begin_utc, end_utc = observer.get_span_utc
    list_of_items = b3w.earthWeather_table.table_query(_pk=job_name,
                                                       _between_low=str(begin_utc),  # "2021-01-21 14:41:49"
                                                       _between_high=str(end_utc)
                                                       )
    # pprint(list_of_items)

    weather_dict = b3w.main_query_filter(list_of_items, geo_name=observer.get_geo_name, attr="weather", field="P")
    print("len_weather_dict=", len(weather_dict), "\n")
    # pprint(weather_dict)
    # #######################################################################################

    weather_P, weather_T = pew.prepare_data_4_plot(unaware_array=unaware_array, observer=observer,
                                                   data_dict=weather_dict, sett=(DATES_SIZE,))
    # #######################################################################################


    Z = np.zeros(DATES_SIZE).reshape(DATES_SIZE, 1)
    Z[:, 0] = weather_P

    horizont_full_span = vertical_full_span / axe0.bbox.height * axe0.bbox.width

    img0 = axe0.imshow(Z,
                       interpolation='bicubic',
                       cmap='summer', origin='upper',
                       extent=[-horizont_full_span/2, horizont_full_span/2, unaware_array[-1], unaware_array[0]],
                       vmax=Z.max(), vmin=Z.min()
                       )
    print("img0=", img0)



    Z = np.zeros(DATES_SIZE).reshape(DATES_SIZE, 1)
    Z[:, 0] = weather_T

    horizont_full_span = vertical_full_span / axe5.bbox.height * axe5.bbox.width

    img5 = axe5.imshow(Z,
                       interpolation='bicubic',
                       cmap='winter', origin='upper',
                       extent=[-horizont_full_span/2, horizont_full_span/2, unaware_array[-1], unaware_array[0]],
                       vmax=Z.max(), vmin=Z.min()
                       )
    print("img5=", img5)



    # //////////////////////  ELEMENTS  /////////////////////////////////////
    elements_array = np.mod(moon_lon, 120)

    gcolumn = 1
    Z = np.zeros(DATES_SIZE * gcolumn).reshape(DATES_SIZE, gcolumn)
    Z[:, 0] = elements_array

    horizont_full_span = vertical_full_span / axe1.bbox.height * axe1.bbox.width

    _plot_annotations_of_moon_elements(annotation_elem_dict=annot_elements, axe=axe1, observer=observer,
                                       ratio_v_h=(vertical_full_span, horizont_full_span))

    CYCLING_OVERLAP = 120 * (2 / 4) / 2 * pz.OVERLAP_COEF
    img1 = axe1.imshow(Z,
                       interpolation='nearest',
                       cmap=pz.elements_cmap, origin='upper',
                       extent=[-horizont_full_span/2, horizont_full_span/2, unaware_array[-1], unaware_array[0]],
                       vmin=0 - CYCLING_OVERLAP, vmax=120 + CYCLING_OVERLAP,
                       )
    print("img1=", img1)


    # //////////////////////  LUNATION  /////////////////////////////////////

    moon_lun = np.array(moon_lunation)
    # moon_lun = np.array(moon_element)
    # moon_lun = np.linspace(10, 200, 1000)
    # sun_zod = np.array(sun_lon)

    gcolumn = 1
    Z = np.zeros(DATES_SIZE * gcolumn).reshape(DATES_SIZE, gcolumn)
    Z[:, 0] = moon_lun

    horizont_full_span = vertical_full_span / axe2.bbox.height * axe2.bbox.width
    _plot_annotations_of_moon_phases(observer=observer, axe=axe2,
                                     ratio_v_h=(vertical_full_span/2, horizont_full_span/2))
    CYCLING_OVERLAP = 0.239
    img2 = axe2.imshow(Z,
                       interpolation='nearest',
                       cmap=pl.lunation_cmap, origin='upper',
                       extent=[-horizont_full_span/2, horizont_full_span/2, unaware_array[-1], unaware_array[0]],
                       vmin=0-CYCLING_OVERLAP, vmax=1+CYCLING_OVERLAP,
                       )
    print("img2=", img2)


    # ////////////////////  SUN MOON DAYS  //////////////////////////////////

    s_angle = np.array(sun_angle)
    ycolors = ps.convert_colors(in_y_list=s_angle, thresh=0.3)
    s_angle = np.array(ycolors)

    m_angle = np.array(moon_angle)
    ycolors = ps.convert_colors(in_y_list=m_angle, thresh=0.3)
    m_angle = np.array(ycolors)

    gcolumn = 5
    Z = np.zeros(DATES_SIZE * gcolumn).reshape(DATES_SIZE, gcolumn)
    Z[:, 0] = s_angle
    Z[:, 1] = s_angle
    Z[:, 2] = (s_angle + m_angle) / 2
    Z[:, 3] = m_angle
    Z[:, 4] = m_angle

    horizont_full_span = vertical_full_span / axe3.bbox.height * axe3.bbox.width

    _plot_annotations_of_sun_days(observer=observer, axe=axe3,
                                  ratio_v_h=(vertical_full_span/2, horizont_full_span/2))
    _plot_annotations_of_moon_days(observer=observer, axe=axe3,
                                   ratio_v_h=(vertical_full_span/2, horizont_full_span/2))

    img3 = axe3.imshow(Z,
                       interpolation='nearest',  # 'nearest', 'bilinear', 'bicubic'
                       cmap="twilight_shifted", origin='upper',
                       extent=[-horizont_full_span/2, horizont_full_span/2, unaware_array[-1], unaware_array[0]],
                       vmin=Z.min(), vmax=Z.max()
                       )
    print("img3=", img3)


    # ///////////////////////  ZODIAC  //////////////////////////////////////

    moon_zod = np.array(moon_lon)
    sun_zod = np.array(sun_lon)

    gcolumn = 2
    Z = np.zeros(DATES_SIZE * gcolumn).reshape(DATES_SIZE, gcolumn)
    Z[:, 0] = moon_zod
    # Z[:, 1] = moon_zod
    # Z[:, 2] = moon_zod
    # Z[:, 3] = sun_zod
    Z[:, 1] = sun_zod

    horizont_full_span = vertical_full_span / axe4.bbox.height * axe4.bbox.width

    _plot_annotations_of_zodiacs(annotation_moon_dict=annot_moon_zod, annotation_sun_dict=annot_sun_zod,
                                 observer=observer,
                                 axe=axe4, ratio_v_h=(vertical_full_span/2, horizont_full_span/2))

    CYCLING_OVERLAP = 360 * (2 / 12) / 2 * pz.OVERLAP_COEF
    img4 = axe4.imshow(Z,
                       interpolation='nearest',  # 'nearest', 'bilinear', 'bicubic'
                       cmap=pz.zodiac_cmap, origin='upper',
                       extent=[-horizont_full_span/2, horizont_full_span/2, unaware_array[-1], unaware_array[0]],
                       vmin=0 - CYCLING_OVERLAP, vmax=360 + CYCLING_OVERLAP,
                       )
    print("img4=", img4)


    # //////////////////////  FOOTPRINT  ////////////////////////////////////

    axe0.set_xlabel("Геолокація: " + observer.get_geo_name,
                    labelpad=6,
                    loc='left',
                    fontsize=9
                    )

    # axe5.set_xlabel("" + format_datetime(observer.restore_unaware(), "d MMMM YYYY р., EEEE, HH:mm:ss zzz", locale='uk_UA'),
    observer.restore_unaware()
    text = "" + format_datetime(observer.get_aware, "d MMMM YYYY р., EEEE, HH:mm, ", locale='uk_UA')
    text += bd.get_timezone_gmt(observer.get_aware, locale='en') + " "
    axe5.set_xlabel(text,
                    labelpad=6,
                    loc='right',
                    fontsize=9
                    )




    # ***********************************************************************
    res_savefig = plt.savefig(file_name)
    print("res_savefig=", res_savefig)

    plt.show()


def _plot_annotations_of_sun_days(observer=None, axe=None, ratio_v_h=(1., 1.)):

    observer.restore_unaware()
    begin_unaware, end_unaware = observer.get_span_unaware
    cur_unaware = begin_unaware

    while end_unaware > cur_unaware:

        if cur_unaware == begin_unaware:                                # init pass
            pass
        else:
            cur_unaware = cur_unaware + timedelta(days=1)               # next position of annotation

        observer.unaware_update_utc12(cur_unaware)                      # adjusting calculation (between rise and setting)
        sun_dict, sun_text = sr.main_sun_rise_sett(observer=observer)   # modified observer
        zenit_sun_utc = ephem.Date((sun_dict['sun_sett'] + sun_dict['sun_rise']) / 2)

        # Convert to unaware
        cur_unaware = observer.dt_utc_to_unaware(in_utc=zenit_sun_utc.datetime())
        # print("@@@", zenit_sun_utc, " --- ", cur_unaware)

        if begin_unaware + timedelta(days=ratio_v_h[0] * ANN_DAYS_OFFSET) < cur_unaware < \
                end_unaware - timedelta(days=ratio_v_h[0] * ANN_DAYS_OFFSET):

            annot_text = format_datetime(cur_unaware, "d MMM EEE", locale='uk_UA')
            # annot_text = str(cur_unaware.strftime(geo.dt_format_plot))
            # coords = (-0.6 * ratio_v_h[1], mdates.date2num(cur_unaware))
            coords = (-0.6 * ratio_v_h[1], cur_unaware)

            axe.annotate(annot_text,
                         xy=coords,
                         fontsize=8.5,
                         horizontalalignment='center',
                         verticalalignment='center'
                         )


def _plot_annotations_of_moon_days(observer=None, axe=None, ratio_v_h=(1., 1.)):

    observer.restore_unaware()
    begin_unaware, end_unaware = observer.get_span_unaware
    cur_unaware = begin_unaware

    counter = 0
    while not((end_unaware < cur_unaware) or (counter > 25)):
        # print('|||', counter, (end_unaware < cur_unaware), " or ", (counter > 5))
        counter += 1
        if cur_unaware == begin_unaware:                            # init pass
            pass                                                    # init calculation
        else:
            cur_unaware = cur_unaware + timedelta(days=24.5 / 24)   # next calculation

        observer.unaware_update_utc(cur_unaware)
        moon_dict, moon_text = md.main_moon_day(observer=observer)  # modified observer
        # print(moon_text[0], moon_text[1], moon_text[2])
        zenit_moon = ephem.Date((moon_dict['moon_sett'] + moon_dict['moon_rise']) / 2)
        zenit_moon_unaware = observer.dt_utc_to_unaware(in_utc=zenit_moon.datetime())       # only monitoring!!!

        # print(counter, ":: ", moon_dict['moon_day'], "\t*cur_unaware=", cur_unaware, "\tzenit_moon_unaware=", zenit_moon_unaware,
        #       (moon_dict['moon_sett'] - moon_dict['moon_rise']))
        # pprint(moon_dict)

        # Convert to unaware
        cur_unaware = observer.dt_utc_to_unaware(in_utc=zenit_moon.datetime())

        if begin_unaware + timedelta(days=ratio_v_h[0] * ANN_DAYS_OFFSET) < cur_unaware < \
                end_unaware - timedelta(days=ratio_v_h[0] * ANN_DAYS_OFFSET):

            annot_text = str(moon_dict["moon_day"]) + " міс. д."
            coords = (0.6 * ratio_v_h[1], mdates.date2num(zenit_moon_unaware))

            axe.annotate(annot_text,
                         xy=coords,
                         fontsize=8,
                         horizontalalignment='center',
                         verticalalignment='center'
                         )


def _plot_annotations_of_moon_phases(observer=None, axe=None, ratio_v_h=(1., 1.)):

    observer.restore_unaware()
    begin_unaware, end_unaware = observer.get_span_unaware
    cur_unaware = begin_unaware

    while end_unaware > cur_unaware:
        if cur_unaware == begin_unaware:                            # init pass
            pass                                                    # init calculation
        else:
            cur_unaware = cur_unaware + timedelta(days=29.53/2)     # next calculation

        observer.unaware_update_utc(cur_unaware)
        moon_phase_dict, moon_text = md.main_moon_phase(observer=observer)
        middle_moon_phase = ephem.Date((moon_phase_dict['prev_utc'] + moon_phase_dict['next_utc']) / 2)

        # Convert middle_moon_phase to unaware (to next step in unaware!)
        cur_unaware = observer.dt_utc_to_unaware(in_utc=middle_moon_phase.datetime())

        # Convert 'prev_utc' to unaware
        prev_unaware = observer.dt_utc_to_unaware(in_utc=ephem.Date(moon_phase_dict['prev_utc']).datetime())

        # Convert 'next_utc' to unaware
        next_unaware = observer.dt_utc_to_unaware(in_utc=ephem.Date(moon_phase_dict['next_utc']).datetime())

        # if True:
        if begin_unaware + timedelta(days=ratio_v_h[0] * ANN_PHAS_OFFSET) < prev_unaware:

            annot_text = str(moon_phase_dict["prev"]).replace(" ", "\n")

            coords = (-0.0 * ratio_v_h[1], prev_unaware)
            # print(annot_text, coords)
            axe.annotate(annot_text,
                         xy=coords,
                         fontsize=7.5,
                         horizontalalignment='center',
                         verticalalignment='center',
                         )

        # if True:
        if next_unaware < end_unaware - timedelta(days=ratio_v_h[0] * ANN_PHAS_OFFSET):

            annot_text = str(moon_phase_dict["next"]).replace(" ", "\n")

            coords = (-0.0 * ratio_v_h[1], next_unaware)
            # print(annot_text, coords)
            axe.annotate(annot_text,
                         xy=coords,
                         fontsize=7.5,
                         horizontalalignment='center',
                         verticalalignment='center',
                         )


def _plot_annotations_of_moon_elements(annotation_elem_dict=None, observer=None, axe=None, ratio_v_h=(1., 1.)):

    begin_unaware, end_unaware = observer.get_span_unaware

    for elem_item in annotation_elem_dict:

        cur_unaware_dt = mdates.num2date(annotation_elem_dict[elem_item]).replace(tzinfo=None)    # observer.get_unaware
        # print(begin_unaware, ' --- ', cur_unaware_dt, ' --- ', end_unaware, cur_unaware_dt.tzinfo)

        if begin_unaware + timedelta(days=ratio_v_h[0] * ANN_ELEM_OFFSET) < cur_unaware_dt < \
                end_unaware - timedelta(days=ratio_v_h[0] * ANN_ELEM_OFFSET):

            annot_text = str(elem_item).replace(" ", "\n")
            coords = (-0.0 * ratio_v_h[1], annotation_elem_dict[elem_item])

            axe.annotate(annot_text,
                         xy=coords,
                         fontsize=9,
                         horizontalalignment='center',
                         verticalalignment='center'
                         )


def _plot_annotations_of_zodiacs(annotation_moon_dict=None, annotation_sun_dict=None,
                                 observer=None, axe=None, ratio_v_h=(1, 1)):

    begin_unaware, end_unaware = observer.get_span_unaware

    for zodiac_item in annotation_moon_dict:
        # print(zodiac_item, annotation_moon_dict[zodiac_item])

        cur_unaware_dt = mdates.num2date(annotation_moon_dict[zodiac_item]).replace(tzinfo=None)    # observer.get_unaware

        if begin_unaware + timedelta(days=ratio_v_h[0] * ANN_ZODC_OFFSET) < cur_unaware_dt < \
                end_unaware - timedelta(days=ratio_v_h[0] * ANN_ZODC_OFFSET):

            annot_text = str(zodiac_item)
            coords = (-0.5 * ratio_v_h[1], annotation_moon_dict[zodiac_item])

            axe.annotate(annot_text,
                         xy=coords,
                         fontsize=9,
                         horizontalalignment='center',
                         verticalalignment='center'
                         )

    for zodiac_item in annotation_sun_dict:
        # print(zodiac_item, annotation_sun_dict[zodiac_item])

        cur_unaware_dt = mdates.num2date(annotation_sun_dict[zodiac_item]).replace(tzinfo=None)    # observer.get_unaware

        if begin_unaware + timedelta(days=ratio_v_h[0] * ANN_ZODC_OFFSET) < cur_unaware_dt < \
                end_unaware - timedelta(days=ratio_v_h[0] * ANN_ZODC_OFFSET):

            annot_text = str(zodiac_item)
            coords = (0.5 * ratio_v_h[1], annotation_sun_dict[zodiac_item])

            axe.annotate(annot_text,
                         xy=coords,
                         fontsize=9,
                         horizontalalignment='center',
                         verticalalignment='center'
                         )


if __name__ == '__main__':

    # geo_name = 'Kremenchuk'
    # geo_name = 'Astana'
    # geo_name = 'Mragowo'
    # geo_name = 'Boston'
    # geo_name = 'London'
    geo_name = 'Kharkiv'

    # in_unaware_datetime = datetime.strptime("1976-07-28 02:37:21", geo.dt_format_rev)  # "%Y-%m-%d %H:%M:%S"
    in_unaware_datetime = datetime.utcnow()
    observer_obj = geo.Observer(geo_name=geo_name, in_unaware_datetime=in_unaware_datetime, span=(7., 2.))
    text = ""
    text += str(observer_obj)
    # print(text)
    # #######################################################################################
    plot_color_of_the_days(observer=observer_obj, file_name="plot_astro_summary.png", job_name="442763659#REP")

    # observer_obj.unaware_update_utc(in_unaware_datetime)
    # observer_obj = geo.Observer(geo_name="Mragowo", input_unaware_datetime=in_unaware_datetime, span=(6., 1.))
    # plot_color_of_the_days(observer=observer_obj, file_name="plot_astro_summary.png", job_name="442763659#REP")

    # observer_obj.unaware_update_utc(in_unaware_datetime)
    # observer_obj = geo.Observer(geo_name="Kremenchuk", in_unaware_datetime=in_unaware_datetime, span=(7., 2.))
    # plot_color_of_the_days(observer=observer_obj, file_name="plot_astro_summary.png", job_name="442763659#REP")

    # observer_obj.unaware_update_utc(in_unaware_datetime)
    # observer_obj = geo.Observer(geo_name="Astana", input_unaware_datetime=in_unaware_datetime, span=(7, 3))
    # plot_color_of_the_days(observer=observer_obj, file_name="plot_astro_summary.png", job_name="442763659#REP")

    # observer_obj.unaware_update_utc(in_unaware_datetime)
    # plot_color_of_the_days(observer=observer_obj, file_name="plot_astro_summary.png", job_name="442763659#REP")
    #
    # observer_obj.unaware_update_utc(in_unaware_datetime)
    # plot_color_of_the_days(observer=observer_obj, file_name="plot_astro_summary.png", job_name="442763659#REP")
