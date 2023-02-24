
import pandas as pd
from datetime import datetime
from pprint import pprint
import os
import json

import src.boto3_package.mainDB_weather as mdbw
import src.ephem_routines.ephem_package.geo_place as geo
import src.weather_package.main_spaceweather_swpc as swt
import src.mathplot_package._plot_spaceWeather as psw
import src.boto3_package.dynamodb_assumed_role_test as drs



try:
    import os
    import sys
    import datetime
    import time
    import boto3
    print("All Modules Loaded ...... ")
except Exception as e:
    print("Error {}".format(e))


def main_create_populate_record_weather():

    text = ""

    result, responce = spaceWeather_table.describe_table()

    if result:
        text += "\n*** Table already exists!"
        text += "\n" + str(responce)
    else:
        text += "\n--- " + str(responce)
        text += "\n*** Create table '" + spaceWeather_table.get_table_name + "' ..."
        table = spaceWeather_table.create_table()
        text += "\n*** Table created successfully!"
        text += "\n--- " + str(table)

    text += "\n*** Populate table from csv"
    text += "\n" + spaceWeather_table.populate_from_csv()

    return text


def main_put_record(observer=None, job_name="12345678#REP1"):

    text = ""

    data_dict = {}

    # Location and timezone
    observer.get_coords_by_name()
    observer.get_tz_by_coord()

    # Observer data
    # observer_dict = {"geo": observer.get_geo_name, "tz": observer.timezone_name}
    observer_dict = {"geo": observer.get_geo_name}
    data_dict["location"] = json.dumps(observer_dict)

    # Weather data
    wth_dict, str_head = swt.main_spaceweather_k_index(observer)
    data_dict["spaceweather"] = json.dumps(wth_dict)

    resp = spaceWeather_table.put(job_name=job_name, data_dict=data_dict)

    text += "\n" + str(resp["ResponseMetadata"]["RequestId"])[:12] + "... "
    text += "" + str(resp["ResponseMetadata"]["HTTPStatusCode"]) + "/" + str(resp["ResponseMetadata"]["RetryAttempts"])

    return data_dict, text


def main_query_filter(list_of_dicts, geo_name="", attr="spaceweather", field=None):
    '''
    :param list_of_dicts:
    :param geo_name:
    :param attr:
    :param field:
    :return:
    '''

    if field is None:
        field = ["P", "T"]

    value_list = []
    value_dict = {}

    # print(">", geo_name)

    for item in list_of_dicts:

        sort_key_val = item[spaceWeather_table.get_sort_key]

        location_dict = json.loads(item['location'])
        attr_dict = json.loads(item[attr])

        city = location_dict['geo']

        # # ToDo do not use invalid dict!
        # if field in attr_dict:
        #     value = attr_dict[field]
        # else:
        #     value = 0
        # # print(">", sort_key_val, city, item[attr], value)

        # Filter by city
        if geo_name.upper() == city:

            value_dict[sort_key_val] = attr_dict
            # value_list.append(float(value))

    # average = 0
    # if len(value_list) > 0:
    #     average = sum(value_list) / len(value_list)

    return value_dict


file_name = "record_spaceweather.csv"
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, file_name)

spaceWeather_table = mdbw.dynamoDB_table(path_file_csv=file_path)

print(os.path.basename(__file__), ">>>", file_path)
print(os.path.basename(__file__), ">>>", spaceWeather_table)


if __name__ == '__main__':

    # text = main_create_populate_record_weather()
    # print(text)


    # geo_name = 'Mragowo'
    # geo_name = 'ASTANA'
    geo_name = 'Kremenchuk'
    local_unaware_datetime = datetime.datetime.now()
    observer_obj = geo.Observer(geo_name=geo_name, input_unaware_datetime=local_unaware_datetime)
    text = ""
    text += str(observer_obj)
    # ###########################################################################

    # data_dict, text = main_put_record(observer=observer_obj, job_name="12345678#TEST")
    # print(data_dict)
    # print(text)

    # data_dict, text = main_put_record(observer=observer_obj, job_name="12345678#REP1")
    # print(data_dict)
    # print(text)
    #
    # data_dict, text = main_put_record(observer=observer_obj, job_name="12345678#REP1")
    # print(data_dict)
    # print(text)



    list_of_items = spaceWeather_table.table_query(_pk="5354533983#345369460#REP",
                                                    _between_low="2021-01-21 14:41:49",
                                                    _between_high="2024-01-21 12:37:00")

    # pprint(list_of_items)
    # print(text)
    data_dict = main_query_filter(list_of_items, geo_name=geo_name, attr="spaceweather", field=["P", "T"])
    print(geo_name)
    pprint(data_dict)

    psw.plot_spaceWeather(data_dict=data_dict, file_name="image_spaceWeather.jpg")
