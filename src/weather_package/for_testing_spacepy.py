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
import requests
import datetime


# Replace YOUR_API_KEY with your actual API key
# api_key = 'DEMO_KEY'
api_key = 'bRusH78dCeaesJvAoUNyGV0D6QieAmRgk5zLPMuC'
# https://api.nasa.gov/planetary/apod?api_key=bRusH78dCeaesJvAoUNyGV0D6QieAmRgk5zLPMuC

# Get the current date and time
end_date = datetime.datetime.now() - datetime.timedelta(days=2)

# Subtract 30 days to get the start date
start_date = end_date - datetime.timedelta(days=3)

# Format the dates as strings in the required format (yyyy-MM-dd)
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')


# URL of the API endpoint
# url = f'https://api.nasa.gov/DONKI/GST?startDate=2016-01-01&endDate=2016-01-30&api_key={api_key}'
# url = f'https://api.nasa.gov/DONKI/GST?startDate=2016-01-01&api_key={api_key}'
url = f'https://api.nasa.gov/DONKI/GST?start_date={start_date_str}&end_date={end_date_str}&api_key={api_key}'
print(url)
# "https://api.nasa.gov/DONKI/GST?start_date=2023-02-17&end_date=2023-02-20&api_key=DEMO_KEY"

# Make a GET request to the API
response = requests.get(url)
print(response)

# Check if the request was successful
if response.status_code == 200:
    # Print the response in JSON format
    data = response.json()
    pprint(data)
else:
    print(f'Request failed with error {response.status_code}: {response.reason}')




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
