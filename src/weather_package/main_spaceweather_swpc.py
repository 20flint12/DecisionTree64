# import spacepy.pycdf as pycdf
#
# # Открываем файл данных солнечной активности
# data = pycdf.CDF('http://spdf.gsfc.nasa.gov/pub/data/omni/high_res_omni/omni2_1998.dat')
#
# # Извлекаем данные о скорости солнечного ветра
# solar_wind_speed = data['V_GSE']
#
# # Закрываем файл данных
# data.close()
#
# # Выводим скорость солнечного ветра
# print(solar_wind_speed)

# import spacepy.pycdf as pycdf
# import datetime
# import pandas as pd
# import os
#
# import urllib.request
#
# url = 'https://spdf.gsfc.nasa.gov/pub/data/omni/high_res_omni/monthly_1min/omni_min202302.asc'
# # local_path = 'omni_min202302.asc'
# # urllib.request.urlretrieve(url, local_path)
#
# # Define the start and end times for the data
# start_time = datetime.datetime(2022, 1, 1)
# end_time = datetime.datetime(2022, 1, 31)
#
# # Load the Kp index data for the specified time range
# file_path = 'http://spdf.sci.gsfc.nasa.gov/pub/data/omni/high_res_omni/omni2_'+start_time.strftime('%Y%m%d')+'_v02.cdf'
# if not os.path.exists(url):
#     print(f"Error: CDF file does not exist at {file_path}")
#
# kp_data = pycdf.CDF(file_path)['kp']
#
# # Get the Kp index values for the time range
# kp_values = kp_data[(kp_data['time'] >= start_time) & (kp_data['time'] <= end_time)]['kp']
#
# # Print the Kp values for each day in the time range
# for date, kp in zip(pd.date_range(start_time, end_time), kp_values):
#     print(date.strftime('%Y-%m-%d'), kp)


# from swpc import get_latest_solar_wind, get_latest_goes_flare
#
# # Получаем данные о последней геомагнитной буре
# solar_wind_data = get_latest_solar_wind()
#
# # Выводим данные о геомагнитной буре
# print(solar_wind_data)

from pprint import pprint

from datetime import datetime
from pprint import pprint
import requests
import json

import src.ephem_routines.ephem_package.geo_place as geo


#
# # Replace YOUR_API_KEY with your actual API key
# # api_key = 'DEMO_KEY'
# api_key = 'bRusH78dCeaesJvAoUNyGV0D6QieAmRgk5zLPMuC'
# # https://api.nasa.gov/planetary/apod?api_key=bRusH78dCeaesJvAoUNyGV0D6QieAmRgk5zLPMuC
#
# # Get the current date and time
# end_date = datetime.datetime.now() - datetime.timedelta(days=2)
#
# # Subtract 30 days to get the start date
# start_date = end_date - datetime.timedelta(days=3)
#
# # Format the dates as strings in the required format (yyyy-MM-dd)
# start_date_str = start_date.strftime('%Y-%m-%d')
# end_date_str = end_date.strftime('%Y-%m-%d')
#
#
# # URL of the API endpoint
# # url = f'https://api.nasa.gov/DONKI/GST?startDate=2016-01-01&endDate=2016-01-30&api_key={api_key}'
# # url = f'https://api.nasa.gov/DONKI/GST?startDate=2016-01-01&api_key={api_key}'
# url = f'https://api.nasa.gov/DONKI/GST?start_date={start_date_str}&end_date={end_date_str}&api_key={api_key}'
# print(url)
# # "https://api.nasa.gov/DONKI/GST?start_date=2023-02-17&end_date=2023-02-20&api_key=DEMO_KEY"
#
# # Make a GET request to the API
# response = requests.get(url)
# print(response)
#
# # Check if the request was successful
# if response.status_code == 200:
#     # Print the response in JSON format
#     data = response.json()
#     pprint(data)
# else:
#     print(f'Request failed with error {response.status_code}: {response.reason}')


# # Replace YOUR_API_KEY with your actual API key
# api_key = 'YOUR_API_KEY'
#
# # Get the current date and time
# end_date = datetime.datetime.now()
#
# # Subtract 30 days to get the start date
# start_date = end_date - datetime.timedelta(days=30)
#
# # Format the dates as strings in the required format (yyyy-MM-dd)
# start_date_str = start_date.strftime('%Y-%m-%d')
# end_date_str = end_date.strftime('%Y-%m-%d')
#
# # URL of the API endpoint
# url = f'https://api.nasa.gov/DONKI/GST?start_date={start_date_str}&end_date={end_date_str}&api_key={api_key}'
#
# # Make a GET request to the API
# response = requests.get(url)
#
# # Check if the request was successful
# if response.status_code == 200:
#     # Print the response in JSON format
#     data = response.json()
#     print(data)
# else:
#     print(f'Request failed with error {response.status_code}: {response.reason}')


def main_spaceweather_k_index(observer=None):
    result_text = ""
    result_dict = {}

    # Define API URL
    # url = 'https://services.swpc.noaa.gov/products/solar-wind/mag-1-day.json'
    # url = 'https://services.swpc.noaa.gov/json/solar_regions.json'

    url = 'https://services.swpc.noaa.gov/json/planetary_k_index_1m.json'

    # Send API request
    response = requests.get(url)
    print(response)

    # Parse JSON response
    data = json.loads(response.content)
    # print(data)

    i = 0
    # Print space weather forecast
    for forecast in data:
        i += 1
        res_str = str(i) + ": \t" + str(forecast['time_tag']) + ': \t' + \
                  str(forecast['kp_index']) + ': ' + str(forecast['estimated_kp']) + \
                  ': \t' + str(forecast['kp'])
        # print(res_str)

    result_dict["time_tag"] = data[-1]["time_tag"]
    result_dict["estimated_kp"] = round(data[-1]["estimated_kp"], 1)
    result_dict["kp"] = data[-1]["kp"]

    # result_text += "\n\n*** weatherdata"
    result_text += "\n\ntime_tag=" + str(result_dict["time_tag"])
    result_text += " estimated_kp=" + str(result_dict["estimated_kp"])
    result_text += " kp=" + str(result_dict["kp"])

    return result_dict, result_text


def main_spaceweather_kp_7_day(observer=None):
    result_text = ""
    result_dict = {}

    url = 'https://services.swpc.noaa.gov/json/geospace/geospace_pred_est_kp_1_hour.json'
    url = 'https://services.swpc.noaa.gov/json/geospace/geospce_pred_est_kp_7_day.json'

    response = requests.get(url)
    print(response)
    data = json.loads(response.content)
    # print(data)

    i = 0
    for forecast in data:
        i += 1
        print(str(i) + ": \t" +
              str(forecast['model_prediction_time']) + ': \t' +
              str(forecast['k'])
              )

    return result_dict, result_text


if __name__ == '__main__':
    # geo_name = 'Mragowo'
    geo_name = 'ASTANA'
    # geo_name = 'Boston'
    # geo_name = 'Kharkiv'

    # local_unaware_datetime = datetime.strptime("1976-07-13 02:37:21", geo.dt_format_rev)  # "%Y-%m-%d %H:%M:%S"
    local_unaware_datetime = datetime.today()
    # local_unaware_datetime = datetime.now()

    observer_obj = geo.Observer(geo_name=geo_name, in_unaware_datetime=local_unaware_datetime)
    text = ""
    text += str(observer_obj)
    # ###########################################################################

    wt_dict, wt_text = main_spaceweather_k_index(observer=observer_obj)
    # pprint(wth_dict)
    text += wt_text
    print(text)
