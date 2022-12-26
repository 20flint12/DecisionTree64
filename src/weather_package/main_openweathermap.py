
from datetime import datetime
from pprint import pprint
import requests

import src.ephem_routines.ephem_package.geo_place as geo


def main_weather_now(observer=None):

    result_text = ""

    # *********************************************
    # api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=683d1608f3ac1dc0916acbed01d0d2e5
    api_key = "683d1608f3ac1dc0916acbed01d0d2e5"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = observer.geo_name
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name

    response = requests.get(complete_url)
    x = response.json()

    '''
    b'{"coord":{"lon":21.3051,"lat":53.8644},
    "weather":[{"id":600,"main":"Snow","description":"light snow","icon":"13d"}],"base":"stations",
    "main":{"temp":269.15,"feels_like":265.13,"temp_min":269.15,"temp_max":269.15,"pressure":1028,"humidity":93,"sea_level":1028,"grnd_level":1011},
    "visibility":175,
    "wind":{"speed":2.73,"deg":104,"gust":5.97},"snow":{"1h":0.48},"clouds":{"all":100},"dt":1670064707,
    "sys":{"type":1,"id":1709,"country":"PL","sunrise":1670049148,"sunset":1670077015},"timezone":3600,"id":764312,"name":"Mr\xc4\x85gowo",
    "cod":200}
    '''
    result_dict = {}
    if x["cod"] != "404":

        y = x["main"]
        # current_temperature = y["temp"] - 273.15
        # current_pressure =
        # current_humidity = y["humidity"]

        z = x["weather"]
        weather_description = z[0]["description"]
        # answer = str(round(answer, 2))
        result_dict["T"] = round(y["temp"] - 273.15, 1)
        result_dict["P"] = round(y["pressure"] / 1.33322387415, 1)
        result_dict["H"] = y["humidity"]

        # result_text += "\n\n*** weatherdata"
        result_text += "\n\nT=" + str(result_dict["T"])
        result_text += " P=" + str(result_dict["P"])
        result_text += " H=" + str(result_dict["H"])

    else:
        print(" City Not Found ")
        result_text += "\nCity Not Found"

    return result_dict, result_text


if __name__ == '__main__':

    geo_name = 'Mragowo'
    # geo_name = 'Boston'
    # geo_name = 'Kharkiv'

    # local_unaware_datetime = datetime.strptime("1976-07-13 02:37:21", geo.dt_format_rev)  # "%Y-%m-%d %H:%M:%S"
    local_unaware_datetime = datetime.today()
    # local_unaware_datetime = datetime.now()

    observer_obj = geo.Observer(geo_name=geo_name, unaware_datetime=local_unaware_datetime)
    text = ""
    text += str(observer_obj)
    # ###########################################################################

    wt_dict, wt_text = main_weather_now(observer=observer_obj)
    # pprint(wth_dict)
    text += wt_text
    print(text)
