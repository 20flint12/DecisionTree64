
from datetime import datetime
from pprint import pprint
import requests

import src.ephem_routines.ephem_package.geo_place as geo


def main_weather_now(geographical_name, local_unaware_datetime):

    str_head = ""
    observer = geo.Observer(geo_name=geographical_name)
    observer.get_coords_by_name()
    observer.get_tz_by_coord()
    str_head += "geo_name= " + observer.geo_name + "\n[lat=" + str(observer.location.latitude) + " lon=" + str(
        observer.location.longitude) + "]"
    str_head += "\ntimezone= " + observer.timezone_name

    str_head += "\n\n*** unaware -> aware -> utc"
    observer.unaware = local_unaware_datetime
    observer.unaware_to_aware_by_tz()  # aware_datetime
    observer.aware_to_utc()  # utc_datetime
    str_head += "\nuna= " + observer.unaware.strftime(geo.dt_format)
    str_head += "\nawa= " + observer.aware.strftime(geo.dt_format)
    str_head += "\nutc= " + observer.utc.strftime(geo.dt_format)

    # *********************************************
    # api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=683d1608f3ac1dc0916acbed01d0d2e5
    api_key = "683d1608f3ac1dc0916acbed01d0d2e5"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = geographical_name
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
    wth_dict = {}
    if x["cod"] != "404":

        y = x["main"]
        # current_temperature = y["temp"] - 273.15
        # current_pressure =
        # current_humidity = y["humidity"]

        z = x["weather"]
        weather_description = z[0]["description"]
        # answer = str(round(answer, 2))
        wth_dict["T"] = round(y["temp"] - 273.15, 1)
        wth_dict["P"] = round(y["pressure"] / 1.33322387415, 1)
        wth_dict["H"] = y["humidity"]

        str_head += "\n\n*** weatherdata"
        # print(" Temperature (in kelvin unit) = " +
        #       str(current_temperature) +
        #       "\n atmospheric pressure (in hPa unit) = " +
        #       str(current_pressure) +
        #       "\n humidity (in percentage) = " +
        #       str(current_humidity) +
        #       "\n description = " +
        #       str(weather_description))

        str_head += "\nT= " + str(wth_dict["T"])
        str_head += "\nP= " + str(wth_dict["P"])
        str_head += "\nH= " + str(wth_dict["H"])

    else:
        print(" City Not Found ")
        str_head += "\nCity Not Found"

    return wth_dict, str_head


if __name__ == '__main__':

    geo_name = 'Mragowo'
    # geo_name = 'Boston'
    # geo_name = 'Kharkiv'

    # local_unaware_datetime = datetime.strptime("1976-07-13 02:37:21", geo.dt_format_rev)  # "%Y-%m-%d %H:%M:%S"
    local_unaware_datetime = datetime.today()
    # local_unaware_datetime = datetime.now()
    # ###########################################################################

    wth_dict, str_head = main_weather_now(geo_name, local_unaware_datetime)
    # pprint(wth_dict)
    print(str_head)
