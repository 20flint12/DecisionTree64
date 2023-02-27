
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


def prepare_data_4_plot(unaware_array=None, observer=None, data_dict=None, sett=None):

    span = observer.get_span

    DATES_SIZE = sett[0]
    # ToDo apply time interval
    SAMPLES_PER_HOUR = sett[1]  # sample every 1 hour!

    KEEP_POINTS = int(DATES_SIZE / (span[0] + span[1]) / 24 / SAMPLES_PER_HOUR) + 1
    print("DATES_SIZE=", DATES_SIZE, "days=", span[0] + span[1], "KEEP_POINTS=", KEEP_POINTS)

    # Find min for fill empty array (maybe needed average value)
    if data_dict:
        min_KP = min(data_dict.values())
        print('min_KP=', min_KP)
    else:
        min_KP = 0

    # Create avg empty array of weather data
    space_KP = np.full(DATES_SIZE, min_KP)
    # weather_T = np.full(DATES_SIZE, min_KPs[1])

    # Fill np.array
    for item in data_dict:
        dt_utc_cur = datetime.strptime(item, geo.dt_format_rev)

        # ToDo Convert to unaware_date
        dt_unaware_cur = observer.dt_utc_to_unaware(dt_utc_cur)
        # print(dt_utc_cur, dt_unaware_cur)

        # Find and replace origin element
        desired_date = mdates.date2num(dt_unaware_cur)
        idx = min(range(len(unaware_array)), key=lambda i: abs(unaware_array[i] - desired_date))

        estimated_kp = data_dict[item]
        # print(idx, item, dt_utc_cur, desired_date, estimated_kp)

        # Replace value_P
        space_KP[idx:idx + KEEP_POINTS] = estimated_kp  # and N elements more
        # weather_T[idx:idx+KEEP_POINTS] = value_T            # and N elements more

    return space_KP


def plot_spaceWeather(xs=None, ys=None, file_name="user_photo2.jpg", sett=None):

    # plt.style.use('_mpl-gallery-nogrid')
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(4, 7))
    fig.subplots_adjust(top=0.95, bottom=.05, left=0.25, right=.95, wspace=0.00)
    # ************************************************************************

    arr_size = len(xs)
    xs = xs
    ys = ys
    # ***********************************************************

    axes[0].set_title(f"size={sett[0]} pph={sett[1]}", fontsize=10)
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

    axes[0].plot(ys, xs, linestyle='dotted')

    # ############################################################
    Z = np.zeros(arr_size).reshape(arr_size, 1)
    Z[:, 0] = ys

    axes[1].set_title(f"Space weather, kp", fontsize=10)
    # axes[1].axis('off')
    axes[1].grid()
    axes[1].set_xticks([])

    vert_range = xs[-1] - xs[0]
    horiz_full = vert_range / axes[1].bbox.height * axes[1].bbox.width

    axes[1].imshow(Z, interpolation='bicubic',  # 'nearest', 'bilinear', 'bicubic'
                   aspect='auto',
                   cmap='turbo',
                   origin='upper',
                   extent=[-horiz_full/2, horiz_full/2, vert_range, 0],
                   # extent=[-horiz_full/2, horiz_full/2, unaware_labels[-1], unaware_labels[0]],
                   # vmax=Z.max(), vmin=Z.min()
                   vmax=9, vmin=0
                   )

    plt.show()


if __name__ == '__main__':

    # geo_name = 'Kremenchuk'
    geo_name = 'Astana'
    # geo_name = 'MRAGOWO'
    # geo_name = 'Boston'
    # geo_name = 'London'
    # geo_name = 'Kharkiv'

    # in_unaware_datetime = datetime.strptime("1976-07-28 02:37:21", geo.dt_format_rev)  # "%Y-%m-%d %H:%M:%S"
    in_unaware_datetime = datetime.utcnow()
    observer_obj = geo.Observer(geo_name=geo_name, in_unaware_datetime=in_unaware_datetime, span=(4., 1.))
    text = ""
    text += str(observer_obj)
    # print(text)
    # #######################################################################################

    begin_utc, end_utc = observer_obj.get_span_utc
    list_of_items = b3sw.spaceWeather_table.table_query(_pk="job_name",
                                                        _between_low=str(begin_utc),  # "2021-01-21 14:41:49"
                                                        _between_high=str(end_utc)
                                                        )
    # pprint(list_of_items)

    spaceweather_dict = b3sw.main_query_filter(list_of_items, geo_name=observer_obj.get_geo_name, attr="spaceweather")
    spaceweather_len = len(spaceweather_dict)
    print("spaceweather_len=", spaceweather_len, "\n")
    # pprint(spaceweather_dict)
    # #######################################################################################

    # Prepare spaceWeather data
    begin_unaware, end_unaware = observer_obj.get_span_unaware

    DATES_SIZE = 1000
    SAMPLES_PER_HOUR = 5
    unaware_timestamp = np.linspace(begin_unaware.timestamp(), end_unaware.timestamp(), DATES_SIZE)
    unaware_array = []
    for cur_unaware_dt in unaware_timestamp:
        observer_obj.unaware_update_utc((datetime.fromtimestamp(cur_unaware_dt)))
        unaware_array.append(mdates.date2num(observer_obj.get_unaware))
        # print(cur_unaware_dt, " | ", observer.get_unaware, " / ", observer.get_utc)

    space_KP = prepare_data_4_plot(unaware_array=unaware_array, observer=observer_obj,
                                   data_dict=spaceweather_dict, sett=(DATES_SIZE, SAMPLES_PER_HOUR))
    # #######################################################################################

    # Plot spaceWeather data
    plot_spaceWeather(xs=unaware_array, ys=space_KP, file_name="spaceWeather.jpg", sett=(DATES_SIZE, SAMPLES_PER_HOUR))
