
import pandas as pd
from datetime import datetime
from pprint import pprint
import os
import json

import src.ephem_routines.ephem_package.geo_place as geo
import src.ephem_routines.ephem_package.moon_day as md
import src.ephem_routines.ephem_package.sun_rise_sett as sr
import src.ephem_routines.ephem_package.zodiac_phase as zd
import src.weather_package.main_openweathermap as wt
import src.mathplot_package._plot_recordWeather as pw


try:
    import os
    import sys
    import datetime
    import time
    import boto3
    print("All Modules Loaded ...... ")
except Exception as e:
    print("Error {}".format(e))


class dynamoDB_table(object):

    _table_name = "table_name"
    _partition_key = 'part_key'
    _sort_key = 'sort_key'

    _df = None

    def __init__(self, path_file_csv=''):

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

    @property
    def sort_key(self):

        return self._sort_key

    # @property
    def get(self, pk=1, sr=1):
        response = self.table.get_item(
            Key={
                self._partition_key: pk,
                self._sort_key: sr
            }
        )
        return response

    def put(self, job_name='', data_dict=None):     # at a current time

        from decimal import Decimal
        import json

        utc_str = datetime.datetime.utcnow().strftime(geo.dt_format_rev)

        # Partition and Sorting keys
        rec_items_dict = {
                self._partition_key: job_name,
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

    def table_query(self, _pk="", _between_low="", _between_high=""):

        from boto3.dynamodb.conditions import Key, Attr

        # response = self.table.query(
        #     KeyConditionExpression=Key(self._partition_key).eq(_pk) & Key(self._sort_key).between(_between_low, _between_high)
        # )

        fe = Attr(self._sort_key).between(_between_low, _between_high)
        response = self.table.scan(
            FilterExpression=fe
        )

        items = response['Items']
        return items

    def populate_from_csv(self):
        text = ""

        for i in range(0, len(self._df)):
            weather_dict = self._df.loc[i].to_dict()
            # print(weather_dict)

            resp = self.put(job_name="chat_job_id", data_dict=weather_dict)
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


def main_put_record(observer=None, job_name="12345678#REP1"):

    text = ""

    data_dict = {}

    # Location and timezone
    observer.get_coords_by_name()
    observer.get_tz_by_coord()

    # Observer data
    observer_dict = {"geo": observer.get_geo_name, "tz": observer.timezone_name}
    data_dict["location"] = json.dumps(observer_dict)

    # Weather data
    wth_dict, str_head = wt.main_weather_now(observer)
    data_dict["weather"] = json.dumps(wth_dict)

    resp = recordWeather_table.put(job_name=job_name, data_dict=data_dict)

    text += "\n" + str(resp["ResponseMetadata"]["RequestId"])[:12] + "... "
    text += "" + str(resp["ResponseMetadata"]["HTTPStatusCode"]) + "/" + str(resp["ResponseMetadata"]["RetryAttempts"])

    return data_dict, text


def main_query_filter(lists_of_items, geo_name="", attr="weather", field="T"):
    '''
    :param lists_of_items:
    :param geo_name:
    :param attr:
    :param field:
    :return:

    'location': {"geo":{"S":"KREMENCHUK"},"tz":{"S":"Europe/Kyiv"}}
    '''

    value_list = []
    value_dict = {}

    # print(">", geo_name)

    for item in lists_of_items:

        sort_key_val = item[recordWeather_table.sort_key]

        location_dict = json.loads(item['location'])
        attr_dict = json.loads(item[attr])

        # city = location_dict['geo'].decode("utf-8")
        city = location_dict['geo']

        # ToDo do not use invalid dict!
        if field in attr_dict:
            value = attr_dict[field]
        else:
            value = 0
        # print(">", sort_key_val, city, item[attr], value)

        # Filter by city
        if geo_name.upper() == city:

            value_dict[sort_key_val] = float(value)
            value_list.append(float(value))

    average = 0
    if len(value_list) > 0:
        average = sum(value_list) / len(value_list)

    return value_dict, average


if __name__ == '__main__':

    # text = main_create_populate_record_weather()
    # print(text)


    # geo_name = 'Mragowo'
    # geo_name = 'ASTANA'
    geo_name = 'Kremenchuk'
    local_unaware_datetime = datetime.datetime.now()
    observer_obj = geo.Observer(geo_name=geo_name, unaware_datetime=local_unaware_datetime)
    text = ""
    text += str(observer_obj)
    # ###########################################################################

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



    list_of_items = recordWeather_table.table_query(_pk="5354533983#345369460#REP",
                                                    _between_low="2021-01-21 14:41:49",
                                                    _between_high="2024-01-21 12:37:00")

    # pprint(list_of_items)
    # print(text)
    data_dict, avg = main_query_filter(list_of_items, geo_name=geo_name, attr="weather", field="P")
    print(geo_name)
    pprint(data_dict)

    # pw.plot_weather(data_list=data_list, file_name="user_photo2.jpg")
