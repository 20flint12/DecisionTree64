
import pandas as pd
from datetime import datetime as dt
from pprint import pprint
import src.ephem_routines.ephem_package.moon_day as md
import src.ephem_routines.ephem_package.sun_rise_sett as sr
import src.ephem_routines.ephem_package.zodiac_phase as zd
import src.weather_package.main_openweathermap as wt
import src.ephem_routines.ephem_package.geo_place as geo


try:
    import os
    import sys
    import datetime
    import time
    import boto3
    print("All Modules Loaded ...... ")
except Exception as e:
    print("Error {}".format(e))


class MyDb(object):

    def __init__(self, table_name='DHT'):
        self.Table_Name = table_name
        self.db = boto3.resource('dynamodb', region_name='eu-west-1')
        self.table = self.db.Table(table_name)
        self.client = boto3.client('dynamodb')

    # @property
    def get(self, _pk=1, _sr=1):
        response = self.table.get_item(
            Key={
                "CHAT": _pk,    # CHAT with suffix (#REP, #ONCE, ...)
                "UTC": _sr      # UTC  yyyy-MM-dd HH:mm:ss,Z
            }
        )
        return response

    def put(self, data_dict):
        response = self.table.put_item(
            Item={
                "CHAT": data_dict["CHAT"],
                "UTC": data_dict["UTC"],
                # Attributes
                "location": str(data_dict["location"]),
                "weather": str(data_dict["weather"]),
                "zodiac": str(data_dict["zodiac"])
            }
        )
        return response

    def delete(self, _pk=1):
        self.table.delete_item(
            Key={
                "CHAT": _pk
            }
        )

    def describe_table(self):

        from botocore.exceptions import ClientError

        # Assumes client is already initialized as DynamoDB client
        try:
            response = self.client.describe_table(TableName=self.Table_Name)
            return response
        except ClientError as err:
            # This will not result in a failed assertion
            assert err.response['Error']['Code'] == 'ResourceNotFoundException'
            return err.response['Error']['Code']

        # response = self.client.describe_table(TableName=self.Table_Name)
        # return response

    def create_table(self):
        """
        Creates a DynamoDB table.
        """
        str_info = "\nCreates a DynamoDB table."

        # if self.table is not None:
        #     str_info += "\n{self.Table_Name} ready..."
        #     return self.table, str_info

        params = {
            'TableName': self.Table_Name,
            'KeySchema': [
                {'AttributeName': 'CHAT', 'KeyType': 'HASH'},
                {'AttributeName': 'UTC', 'KeyType': 'RANGE'}
            ],
            'AttributeDefinitions': [
                {'AttributeName': 'CHAT', 'AttributeType': 'S'},
                {'AttributeName': 'UTC', 'AttributeType': 'S'}
            ],
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 12,
                'WriteCapacityUnits': 12
            }
        }
        self.table = self.db.create_table(**params)
        str_info += f"\nCreating {self.Table_Name}..."
        self.table.wait_until_exists()

        return self.table, str_info

    def table_query(self, _pk="", _between_low="", _between_high=""):

        from boto3.dynamodb.conditions import Key, Attr

        response = self.table.query(
            KeyConditionExpression=Key('CHAT').eq(_pk) & Key('UTC').between(_between_low, _between_high)
        )
        items = response['Items']
        return items

    # def table_query_by_prop(self, _pk="", _between_low="", _between_high=""):
    #
    #     from boto3.dynamodb.conditions import Key, Attr
    #
    #     response = self.table.query(
    #         KeyConditionExpression=Key('CHAT').eq(_pk) & Key('UTC').between("", "") & Key('UTC').lt(_lt)
    #     )
    #     items = response['Items']
    #     return items


def main_create_table_record():

    text = ""

    res_table = obj.describe_table()
    text += "\n" + str(res_table) + "\n"

    if res_table == "ResourceNotFoundException":
        pass
        text += "\n\n*** Create table"
        table, str_info = obj.create_table()
        text += "\n" + str_info

    data_dict = {"CHAT": "4342423425#ONCE", "UTC": "2022-12-15 12:34:22,434", "location": {}, "weather": {}, "zodiac": {}}

    resp = obj.put(data_dict)
    text += str(resp) + "\n"

    return resp, text


def main_put_record(_chat_job="12345678#REP1"):

    global observer

    text = ""
    # dts = int(dt.utcnow().timestamp())
    utc_str = dt.utcnow().strftime(geo.dt_format_rev)

    # if init_id == 0:
    #     table_dict = obj.describe_table()
    #     # init_id = int(table_dict["Table"]["ItemCount"])
    #     # init_id = int(table_dict["Table"]["TableSizeBytes"] / 2)
    #     init_id = dts - 670000000   # clear some digits
    #
    # else:
    #     init_id += 1
    # # print(init_id)

    # Partition and Sorting keys
    data_dict = {"CHAT": _chat_job, "UTC": utc_str}

    # Location and timezone
    observer.get_coords_by_name()
    observer.get_tz_by_coord()
    data_dict["location"] = {"geo": observer.geo_name,
                             "lat": round(observer.location.latitude, 2),
                             "lon": round(observer.location.longitude, 2),
                             "tz": observer.timezone_name
                             }

    # Weather data
    wth_dict, str_head = wt.main_weather_now(observer.geo_name, dt.today())
    data_dict["weather"] = wth_dict

    # Zodiac data
    data_dict["zodiac"] = {}

    resp = obj.put(data_dict)

    text += "\n" + str(resp["ResponseMetadata"]["RequestId"])[:12] + "... "
    text += "" + str(resp["ResponseMetadata"]["HTTPStatusCode"]) + "/" + str(resp["ResponseMetadata"]["RetryAttempts"])

    # text += "\n" + str(init_id) + " "

    return data_dict, text


def main_get_record(_chat_job="12345678#REP"):

    text = ""
    list_of_items = obj.table_query(_pk=_chat_job, )
    # print(res_item1["Item"])
    text += "\n" + str(list_of_items) + "\n"

    return list_of_items[0], text


def main_query_range(_chat_job="442763659#REP", _between_low="2022-12-11 21:11:17", _between_high="2022-12-11 21:13:17"):

    text = ""
    list_of_items = obj.table_query(_pk=_chat_job, _between_low=_between_low, _between_high=_between_high)

    if len(list_of_items) > 0:

        text += "\n" + str(list_of_items) + "\n"
        return list_of_items, text

    else:

        text += "\nempty list"
        return [], text


def main_query_filter(list_of_items, attr="weather", field="T"):
    value_list = []

    for item in list_of_items:
        # print(item["weather"])
        # weather_dict = json.loads(str(item["weather"]))
        weather_dict = ast.literal_eval(item[attr])
        value = weather_dict[field]
        # print(value)
        value_list.append(value)

    return value_list



obj = MyDb(table_name='main_records')
observer = geo.Observer(geo_name="Kharkiv")

if __name__ == '__main__':
    import json
    import ast
    # text = main_create_table_record()
    # print(text)


    # init_id, text = main_put_record()
    # # print(item_dict)
    # print(text)


    list_of_items, text = main_query_range("442763659#REP", "2022-12-11 21:11:17", "2022-12-11 21:12:17")
    # pprint(list_of_items)
    # print(text)
    data_list = main_query_filter(list_of_items, attr="weather", field="H")
    print(data_list)
