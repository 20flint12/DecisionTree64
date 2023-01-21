
import pandas as pd
from datetime import datetime
from pprint import pprint
import os

import src.ephem_routines.ephem_package.geo_place as geo
import src.ephem_routines.ephem_package.moon_day as md
import src.ephem_routines.ephem_package.sun_rise_sett as sr
import src.ephem_routines.ephem_package.zodiac_phase as zd
import src.weather_package.main_openweathermap as wt
import src.mathplot_package.plot_DB_attr as mt


try:
    import os
    import sys
    import datetime
    import time
    import boto3
    print("All Modules Loaded ...... ")
except Exception as e:
    print("Error {}".format(e))


# class MyDb(object):
#
#     def __init__(self, table_name='DHT'):
#         self.Table_Name = table_name
#         self.db = boto3.resource('dynamodb', region_name='eu-west-1')
#         self.table = self.db.Table(table_name)
#         self.client = boto3.client('dynamodb')
#
#     # @property
#     def get(self, _pk=1, _sr=1):
#         response = self.table.get_item(
#             Key={
#                 "CHAT": _pk,    # CHAT with suffix (#REP, #ONCE, ...)
#                 "UTC": _sr      # UTC  yyyy-MM-dd HH:mm:ss,Z
#             }
#         )
#         return response
#
#     def put(self, data_dict):
#         response = self.table.put_item(
#             Item={
#                 "CHAT": data_dict["CHAT"],
#                 "UTC": data_dict["UTC"],
#                 # Attributes
#                 "location": str(data_dict["location"]),
#                 "weather": str(data_dict["weather"]),
#                 "zodiac": str(data_dict["zodiac"])
#             }
#         )
#         return response
#
#     def delete(self, _pk=1):
#         self.table.delete_item(
#             Key={
#                 "CHAT": _pk
#             }
#         )
#
#     def describe_table(self):
#
#         from botocore.exceptions import ClientError
#
#         # Assumes client is already initialized as DynamoDB client
#         try:
#             response = self.client.describe_table(TableName=self.Table_Name)
#             return response
#         except ClientError as err:
#             # This will not result in a failed assertion
#             assert err.response['Error']['Code'] == 'ResourceNotFoundException'
#             return err.response['Error']['Code']
#
#         # response = self.client.describe_table(TableName=self.Table_Name)
#         # return response
#
#     def create_table(self):
#         """
#         Creates a DynamoDB table.
#         """
#         str_info = "\nCreates a DynamoDB table."
#
#         # if self.table is not None:
#         #     str_info += "\n{self.Table_Name} ready..."
#         #     return self.table, str_info
#
#         params = {
#             'TableName': self.Table_Name,
#             'KeySchema': [
#                 {'AttributeName': 'CHAT', 'KeyType': 'HASH'},
#                 {'AttributeName': 'UTC', 'KeyType': 'RANGE'}
#             ],
#             'AttributeDefinitions': [
#                 {'AttributeName': 'CHAT', 'AttributeType': 'S'},
#                 {'AttributeName': 'UTC', 'AttributeType': 'S'}
#             ],
#             'ProvisionedThroughput': {
#                 'ReadCapacityUnits': 12,
#                 'WriteCapacityUnits': 12
#             }
#         }
#         self.table = self.db.create_table(**params)
#         str_info += f"\nCreating {self.Table_Name}..."
#         self.table.wait_until_exists()
#
#         return self.table, str_info
#
#     def table_query(self, _pk="", _between_low="", _between_high=""):
#
#         from boto3.dynamodb.conditions import Key, Attr
#
#         response = self.table.query(
#             KeyConditionExpression=Key('CHAT').eq(_pk) & Key('UTC').between(_between_low, _between_high)
#         )
#         items = response['Items']
#         return items


class dynamoDB_table(object):

    _table_name = "table_name"
    _partition_key = 'part_key'
    _sort_key = 'sort_key'

    _df = None

    def __init__(self, path_file_csv=''):

        # import os

        self._df = pd.read_csv(path_file_csv)

        file_name_ext = os.path.basename(path_file_csv)
        # print(file_name_ext)
        file_name, file_ext = os.path.splitext(file_name_ext)
        # print(file_name)
        # print(file_ext)

        self._table_name = file_name
        self._partition_key = self._df.columns[0]
        self._sort_key = self._df.columns[1]

        self.db = boto3.resource('dynamodb', region_name='eu-west-1')
        self.table = self.db.Table(self._table_name)
        self.client = boto3.client('dynamodb')

    # @property
    def get(self, pk=1, sr=1):
        response = self.table.get_item(
            Key={
                self._partition_key: pk,
                self._sort_key: sr
            }
        )
        return response

    def put(self, chat_job='', data_dict=None):

        from decimal import Decimal
        import json

        utc_str = datetime.datetime.utcnow().strftime(geo.dt_format_rev)

        # Partition and Sorting keys
        rec_items_dict = {
                self._partition_key: chat_job,
                self._sort_key: utc_str
        }

        # print("data_dict=", data_dict)
        ddb_data = json.loads(json.dumps(data_dict), parse_float=Decimal)  # get rid of float
        rec_items_dict.update(ddb_data)  # !!!

        # print(self._partition_key, self._sort_key, rec_items_dict)
        response = self.table.put_item(Item=rec_items_dict)

        return response

    def delete(self, partition_key=''):
        self.table.delete_item(
            Key={
                self._partition_key: partition_key
            }
        )

    def describe_table(self):

        from botocore.exceptions import ClientError

        # Assumes client is already initialized as DynamoDB client
        try:
            response = self.client.describe_table(TableName=self._table_name)

            return True, response

        except ClientError as err:
            # This will not result in a failed assertion
            assert err.response['Error']['Code'] == 'ResourceNotFoundException'

            return False, err.response['Error']['Code']

    def create_table(self):
        """
        Creates a DynamoDB table.
        """
        params = {
            'TableName': self._table_name,
            'KeySchema': [
                {'AttributeName': self._partition_key, 'KeyType': 'HASH'},
                {'AttributeName': self._sort_key, 'KeyType': 'RANGE'}
            ],
            'AttributeDefinitions': [
                {'AttributeName': self._partition_key, 'AttributeType': 'S'},
                {'AttributeName': self._sort_key, 'AttributeType': 'S'}
            ],
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        }
        self.table = self.db.create_table(**params)
        self.table.wait_until_exists()

        return self.table

    def get_table_size(self):
        pass
        # init_id = int(table_dict["Table"]["ItemCount"])
        # init_id = int(table_dict["Table"]["TableSizeBytes"] / 2)

    # def table_query(self, partition_key=1):
    #
    #     from boto3.dynamodb.conditions import Key, Attr
    #
    #     response = self.table.query(
    #         KeyConditionExpression=Key(self._partition_key).eq(partition_key)
    #     )
    #     items = response['Items']
    #     # print(items)
    #     return items

    def table_query(self, _pk="", _between_low="", _between_high=""):

        from boto3.dynamodb.conditions import Key, Attr

        response = self.table.query(
            KeyConditionExpression=Key(self._partition_key).eq(_pk) & Key(self._sort_key).between(_between_low, _between_high)
        )
        items = response['Items']
        return items

    def populate_from_csv(self):
        text = ""

        for i in range(0, len(self._df)):
            moon_zodiac_dict = self._df.loc[i].to_dict()
            # print(moon_zodiac_dict)

            resp = recordWeather_table.put(moon_zodiac_dict)
            # print(".")
            text += str(resp) + "\n"

        return text


file_name = "record_weather.csv"
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, file_name)
print(file_path)

recordWeather_table = dynamoDB_table(path_file_csv=file_path)
print(recordWeather_table)


def main_create_populate_record_weather():

    text = ""

    result, responce = recordWeather_table.describe_table()

    if result:
        text += "\n*** Table already exists!"
        text += "\n" + str(responce)
    else:
        text += "\n--- " + str(responce)
        text += "\n*** Create table '" + recordWeather_table._table_name + "' ..."
        table = recordWeather_table.create_table()
        text += "\n*** Table created successfully!"
        text += "\n--- " + str(table)

    text += "\n*** Populate table from csv"
    text += "\n" + recordWeather_table.populate_from_csv()

    return text


def main_put_record(observer=None, _chat_job="12345678#REP1"):

    text = ""

    data_dict = {}

    # Location and timezone
    observer.get_coords_by_name()
    observer.get_tz_by_coord()
    data_dict["location"] = {"geo": observer._geo_name,
                             "tz": observer.timezone_name
                             }

    # Weather data
    wth_dict, str_head = wt.main_weather_now(observer)
    # data_dict["weather"] = {'erwe': 32.34}
    data_dict["weather"] = wth_dict

    resp = recordWeather_table.put(chat_job=_chat_job, data_dict=data_dict)

    text += "\n" + str(resp["ResponseMetadata"]["RequestId"])[:12] + "... "
    text += "" + str(resp["ResponseMetadata"]["HTTPStatusCode"]) + "/" + str(resp["ResponseMetadata"]["RetryAttempts"])

    return data_dict, text


# def main_get_record(_chat_job="12345678#REP"):
#
#     text = ""
#     list_of_items = obj.table_query(_pk=_chat_job, )
#     # print(res_item1["Item"])
#     text += "\n" + str(list_of_items) + "\n"
#
#     return list_of_items[0], text


def main_query_range(_chat_job="442763659#REP", _between_low="2022-12-11 21:11:17", _between_high="2022-12-11 21:13:17"):

    text = ""
    list_of_items = recordWeather_table.table_query(_pk=_chat_job, _between_low=_between_low, _between_high=_between_high)

    if len(list_of_items) > 0:

        text += "\n" + str(list_of_items) + "\n"
        return list_of_items, text

    else:

        text += "\nempty list"
        return [], text


def main_query_filter(lists_of_items, attr="weather", field="T"):

    import json
    import ast

    value_list = []

    for item in lists_of_items:
        # print(item[attr])
        # print(item[attr][field])
        # weather_dict = json.loads(str(item["weather"]))
        # weather_dict = ast.literal_eval(item[attr])
        # print(weather_dict)

        value = item[attr][field]
        # print(value)
        value_list.append(float(value))

    return value_list


if __name__ == '__main__':

    # text = main_create_populate_record_weather()
    # print(text)


    # geo_name = 'Mragowo'
    # local_unaware_datetime = datetime.datetime.now()
    # observer_obj = geo.Observer(geo_name=geo_name, unaware_datetime=local_unaware_datetime)
    # text = ""
    # text += str(observer_obj)
    # # ###########################################################################

    # data_dict, text = main_put_record(observer=observer_obj, _chat_job="12345678#REP1")
    # print(data_dict)
    # print(text)
    #
    # data_dict, text = main_put_record(observer=observer_obj, _chat_job="12345678#REP1")
    # print(data_dict)
    # print(text)
    #
    # data_dict, text = main_put_record(observer=observer_obj, _chat_job="12345678#REP1")
    # print(data_dict)
    # print(text)



    # list_of_items, text = main_query_range("442763659#REP", "2022-12-11 21:11:17", "2023-12-13 07:00:17")
    list_of_items = recordWeather_table.table_query(_pk="12345678#REP1",
                                                    _between_low="2023-01-21 11:19:46",
                                                    _between_high="2023-01-21 12:37:00")

    # pprint(list_of_items)
    # # print(text)
    data_list = main_query_filter(list_of_items, attr="weather", field="P")
    print(data_list)

    # mt.plot_list(data_list, file_name="user_photo2.jpg")
