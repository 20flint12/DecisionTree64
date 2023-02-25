
from pprint import pprint
from datetime import datetime, timedelta
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib.colors as mcolors
import matplotlib.dates as mdates

import src.ephem_routines.ephem_package.geo_place as geo
import src.boto3_package.mainDB_weather as b3w


# Create colormap
colors = [
    '#ba1b1b', '#e75321', '#e75321', '#e75321', '#ba1b1b',  # AR    красный
    '#073763', '#0c343d', '#0c343d', '#0c343d', '#073763',  # TA    пастельные тона розового и зеленого
]

weather_cmap = LinearSegmentedColormap.from_list('elements_cmap', colors, N=960)


def prepare_data_4_plot(unaware_array=None, observer=None, data_dict=None):

    KEEP_POINTS = 8

    # Find min for fill empty array (maybe needed average value)
    if spaceweather_dict:
        # min_P = min(data_dict.values()['P'])
        min_PT = min((int(d['P']), int(d['T'])) for d in spaceweather_dict.values())
        print('len=', spaceweather_len, min_PT)
    else:
        min_PT = (0, 0)

    # Create avg empty array of weather data
    weather_P = np.full(DATES_SIZE, min_PT[0])
    weather_T = np.full(DATES_SIZE, min_PT[1])

    # Fill np.array
    for item in spaceweather_dict:
        dt_utc_cur = datetime.strptime(item, geo.dt_format_rev)

        # ToDo Convert to unaware_date
        dt_unaware_cur = observer.dt_utc_to_unaware(dt_utc_cur)
        # print(dt_utc_cur, dt_unaware_cur)

        # Find and replace origin element
        desired_date = mdates.date2num(dt_unaware_cur)
        idx = min(range(len(unaware_array)), key=lambda i: abs(unaware_array[i] - desired_date))

        value_P = spaceweather_dict[item]['P']
        value_T = spaceweather_dict[item]['T']
        # print(idx, item, dt_utc_cur, desired_date, value_P)

        # Replace value_P
        weather_P[idx:idx + KEEP_POINTS] = value_P      # and N elements more
        weather_T[idx:idx + KEEP_POINTS] = value_T      # and N elements more
        # weather_P[idx] = np.full(10, value_P)

    return weather_P, weather_T


def plot_earthWeather(xs=None, ys=None, file_name="user_photo.jpg"):

    # plt.style.use('_mpl-gallery-nogrid')
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(4, 7))
    fig.subplots_adjust(top=0.95, bottom=.05, left=0.25, right=.95, wspace=0.00)
    # ************************************************************************

    xs = xs
    y1s = ys[0]
    y2s = ys[1]

    arr_size = len(xs)
    vert_range = xs[-1] - xs[0]
    # ************************************************************************

    axes[0].set_title(f'P, mmGh', fontsize=10)
    axes[0].grid()
    axes[0].axis(ymin=xs[-1], ymax=xs[0])

    # axes[0].grid(axis='y')
    # axes[0].yaxis.set_major_formatter(mdates.DateFormatter('%D %H:%M'))
    # datetime_format = mdates.DateFormatter('%d%b %H:%M')
    # axes[0].yaxis.set_major_locator(mdates.HourLocator(interval=12))
    datetime_format = mdates.DateFormatter('%d%b')
    axes[0].yaxis.set_major_locator(mdates.DayLocator(interval=1))
    axes[0].yaxis.set_major_formatter(datetime_format)
    axes[0].yaxis.set_major_locator(mdates.AutoDateLocator(minticks=3, maxticks=10))

    axes[0].plot(y1s, xs, linestyle='dotted')

    # ############################################################
    Z = np.zeros(arr_size).reshape(arr_size, 1)
    Z[:, 0] = y1s

    axes[1].set_title(f"P, mmGh", fontsize=10)
    # axes[1].axis('off')
    axes[1].grid()
    axes[1].set_xticks([])

    horiz_full = vert_range / axes[1].bbox.height * axes[1].bbox.width

    axes[1].imshow(Z, interpolation='bicubic',  # 'nearest', 'bilinear', 'bicubic'
                   aspect='auto',
                   cmap='summer',
                   origin='upper',
                   extent=[-horiz_full/2, horiz_full/2, vert_range, 0],             # to view the range!!!
                   # extent=[-horiz_full/2, horiz_full/2, unaware_labels[-1], unaware_labels[0]],
                   vmax=Z.max(), vmin=Z.min())

    # ############################################################
    Z = np.zeros(arr_size).reshape(arr_size, 1)
    Z[:, 0] = y2s

    axes[2].set_title(f"T,°C", fontsize=10)
    # axes[1].axis('off')
    axes[2].grid()
    axes[2].set_xticks([])

    horiz_full = vert_range / axes[2].bbox.height * axes[2].bbox.width

    axes[2].imshow(Z, interpolation='bicubic',  # 'nearest', 'bilinear', 'bicubic'
                   aspect='auto',
                   cmap='winter',
                   origin='upper',
                   extent=[-horiz_full/2, horiz_full/2, vert_range, 0],             # to view the range!!!
                   # extent=[-horiz_full/2, horiz_full/2, unaware_labels[-1], unaware_labels[0]],
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
    observer_obj = geo.Observer(geo_name=geo_name, input_unaware_datetime=in_unaware_datetime, span=(5., 1.))
    text = ""
    text += str(observer_obj)
    # print(text)
    # #######################################################################################

    begin_utc, end_utc = observer_obj.get_span_utc
    list_of_items = b3w.earthWeather_table.table_query(_pk="job_name",
                                                       _between_low=str(begin_utc),  # "2021-01-21 14:41:49"
                                                       _between_high=str(end_utc)
                                                       )
    # pprint(list_of_items)

    spaceweather_dict = b3w.main_query_filter(list_of_items, geo_name=observer_obj.get_geo_name, attr="weather")
    spaceweather_len = len(spaceweather_dict)
    print("spaceweather_len=", spaceweather_len, "\n")
    # pprint(spaceweather_dict)
    # #######################################################################################

    # Prepare spaceWeather data
    begin_unaware, end_unaware = observer_obj.get_span_unaware

    DATES_SIZE = 1000
    unaware_timestamp = np.linspace(begin_unaware.timestamp(), end_unaware.timestamp(), DATES_SIZE)
    unaware_array = []
    for cur_unaware_dt in unaware_timestamp:
        observer_obj.unaware_update_utc((datetime.fromtimestamp(cur_unaware_dt)))
        unaware_array.append(mdates.date2num(observer_obj.get_unaware))
        # print(cur_unaware_dt, " | ", observer.get_unaware, " / ", observer.get_utc)

    weather_P, weather_T = prepare_data_4_plot(unaware_array=unaware_array, observer=observer_obj, data_dict=spaceweather_dict)
    # #######################################################################################

    # Plot spaceWeather data
    plot_earthWeather(xs=unaware_array, ys=(weather_P, weather_T), file_name="image_earthWeather.jpg")
