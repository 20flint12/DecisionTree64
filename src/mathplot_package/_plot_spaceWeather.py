
from pprint import pprint
from datetime import datetime, timedelta
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.dates as mdates
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

import src.ephem_routines.ephem_package.geo_place as geo
import src.boto3_package.mainDB_spaceweather as b3sw



# Create colormap
colors = [
    '#ba1b1b', '#e75321', '#e75321', '#e75321', '#ba1b1b',  # AR    красный
    '#073763', '#0c343d', '#0c343d', '#0c343d', '#073763',  # TA    пастельные тона розового и зеленого
]

weather_cmap = LinearSegmentedColormap.from_list('elements_cmap', colors, N=960)


def plot_spaceWeather(xs=None, ys=None, file_name="user_photo2.jpg"):

    # plt.style.use('_mpl-gallery-nogrid')
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(4, 7))
    fig.subplots_adjust(top=0.95, bottom=.05, left=0.15, right=.95, wspace=0.00)
    # ************************************************************************

    len_arr = len(xs)
    xs = xs
    ys = ys
    # ***********************************************************

    axes[0].set_title(f'ypoints', fontsize=10)
    axes[0].grid()
    axes[0].axis(ymin=unaware_labels[-1], ymax=unaware_labels[0])
    axes[0].yaxis.set_major_locator(mdates.DayLocator(interval=1))

    axes[0].plot(ys, xs, linestyle='dotted')


    # ############################################################
    arr_size = len(ys); gcolumn = 1
    Z = np.zeros(arr_size * gcolumn).reshape(arr_size, gcolumn)
    Z[:, 0] = ys

    axes[1].set_title(f"Weather", fontsize=10)
    # axes[1].axis('off')

    # vert_range = lbl_dates[-1] - lbl_dates[0]
    # vert_range = days * 2
    vert_range = len_arr
    horiz_half = vert_range / axes[1].bbox.height * axes[1].bbox.width / 2

    axes[1].imshow(Z, interpolation='bicubic',  # 'nearest', 'bilinear', 'bicubic'
                   aspect='auto',
                   cmap='summer',
                   origin='upper',
                   extent=[-horiz_half, horiz_half, vert_range, 0],
                   vmax=Z.max(), vmin=Z.min())

    plt.show()


if __name__ == '__main__':

    # geo_name = 'Kremenchuk'
    # geo_name = 'Astana'
    geo_name = 'MRAGOWO'
    # geo_name = 'Boston'
    # geo_name = 'London'
    # geo_name = 'Kharkiv'

    # in_unaware_datetime = datetime.strptime("1976-07-28 02:37:21", geo.dt_format_rev)  # "%Y-%m-%d %H:%M:%S"
    in_unaware_datetime = datetime.utcnow()
    observer_obj = geo.Observer(geo_name=geo_name, input_unaware_datetime=in_unaware_datetime, span=(5., 2.))
    text = ""
    text += str(observer_obj)
    # print(text)
    # #######################################################################################

    begin_unaware, end_unaware = observer_obj.get_span_unaware
    begin_utc, end_utc = observer_obj.get_span_utc

    DATES_SIZE = 1000
    unaware_timestamp = np.linspace(begin_unaware.timestamp(), end_unaware.timestamp(), DATES_SIZE)

    points_per_hour = 6

    unaware_labels = []
    for cur_unaware_dt in unaware_timestamp:
        observer_obj.unaware_update_utc((datetime.fromtimestamp(cur_unaware_dt)))
        unaware_labels.append(mdates.date2num(observer_obj.get_unaware))

    list_of_items = b3sw.spaceWeather_table.table_query(_pk="job_name",
                                                        _between_low=str(begin_utc),  # "2021-01-21 14:41:49"
                                                        _between_high=str(end_utc)
                                                        )
    # pprint(list_of_items)

    spaceweather_dict = b3sw.main_query_filter(list_of_items, geo_name=observer_obj.get_geo_name,
                                               attr="spaceweather", field="P")
    spaceweather_len = len(spaceweather_dict)
    print("spaceweather_len=", spaceweather_len, "\n")
    pprint(spaceweather_dict)

    # Find min for fill empty array (maybe needed average value)
    if spaceweather_dict:
        # min_P = min(data_dict.values()['P'])
        min_KPs = min((int(d['estimated_kp']), int(d['estimated_kp'])) for d in spaceweather_dict.values())
        print('len=', spaceweather_len, min_KPs)
    else:
        min_KPs = (0, 0)

    # Create avg empty array of weather data
    weather_P = np.full(DATES_SIZE, min_KPs[0])
    weather_T = np.full(DATES_SIZE, min_KPs[1])

    # Fill np.array
    for item in spaceweather_dict:

        dt_utc_cur = datetime.strptime(item, geo.dt_format_rev)

        # ToDo Convert to unaware_date
        dt_unaware_cur = observer_obj.dt_utc_to_unaware(dt_utc_cur)
        # print(dt_utc_cur, dt_unaware_cur)

        # Find and replace origin element
        desired_date = mdates.date2num(dt_unaware_cur)
        idx = min(range(len(unaware_labels)), key=lambda i: abs(unaware_labels[i] - desired_date))

        value_P = spaceweather_dict[item]['estimated_kp']
        # value_T = spaceweather_dict[item]['T']
        print(item, dt_utc_cur, desired_date, idx, value_P)

        # Replace value_P
        # weather_P[idx] = value_P
        weather_P[idx:idx+points_per_hour] = value_P            # and N elements more
        # weather_T[idx:idx+points_per_hour] = value_T            # and N elements more
        # weather_P[idx] = np.full(10, value_P)

    #
    plot_spaceWeather(xs=unaware_labels, ys=weather_P, file_name="user_photo2.jpg")




