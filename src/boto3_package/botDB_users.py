
import pandas as pd
from datetime import datetime
from pprint import pprint
import os

import src.ephem_routines.ephem_package.geo_place as geo
import src.ephem_routines.ephem_package.moon_day as md
import src.ephem_routines.ephem_package.sun_rise_sett as sr
import src.ephem_routines.ephem_package.zodiac_phase as zd
import src.weather_package.main_openweathermap as wt
import src.PTB._ptb_observer_persist_conversation as opc


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
    _last_time_key = '_last_time_key'

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
        self._last_time_key = self._df.columns[2]

        self.db = boto3.resource('dynamodb', region_name='eu-west-1')
        self.table = self.db.Table(self._table_name)
        self.client = boto3.client('dynamodb')

    @property
    def sort_key(self):

        return self._sort_key

    @property
    def table_name(self):

        return self._table_name

    # @property
    def get(self, pk=1, sr=1):
        response = self.table.get_item(
            Key={
                self._partition_key: pk,
                self._sort_key: sr
            }
        )
        return response

    def put(self, user_data_dict=None):     # at a current UTC time

        from decimal import Decimal
        import json

        # # Partition and Sorting keys
        # rec_items_dict = {
        #         self._partition_key: chat_id,
        #         self._sort_key: utc_str
        # }
        rec_items_dict = {}

        # print("data_csv_dict=", user_data_dict)

        if user_data_dict is not None:
            ddb_data = json.loads(json.dumps(user_data_dict), parse_float=Decimal)  # get rid of float
            rec_items_dict.update(ddb_data)  # !!!

            # Update last_time_key current UTC now
            utc_str = datetime.datetime.utcnow().strftime(geo.dt_format_rev)
            rec_items_dict[self._last_time_key] = utc_str

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

        response = self.table.query(
            KeyConditionExpression=Key(self._partition_key).eq(_pk) & Key(self._sort_key).between(_between_low, _between_high)
        )
        items = response['Items']
        return items

    def populate_from_csv(self):
        text = ""

        for i in range(0, len(self._df)):
            data_csv_dict = self._df.loc[i].to_dict()
            # print("> ", data_csv_dict)
            # {'chat_pk': 4774374724, 'name_sk': '2022-12-11 21:11:17', 'last_action': '2022-12-11 21:11:17', 'setting': '{'Геолокація': 'WARSAW', 'Інтервал': '1.111', 'Нагадування': '2331'}'}

            resp = self.put(user_data_dict=data_csv_dict)

            text += str(resp) + "\n"

        return text


file_name = "bot_Users.csv"
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, file_name)
print(file_path)

botUsers_table = dynamoDB_table(path_file_csv=file_path)
print(botUsers_table)


def main_create_populate_bot_users():

    text = ""

    result, response = botUsers_table.describe_table()

    if result:
        text += "\n*** Table already exists!"
        text += "\n" + str(response)
    else:
        text += "\n--- " + str(response)
        text += "\n*** Create table '" + botUsers_table.table_name + "' ..."
        table = botUsers_table.create_table()
        text += "\n*** Table created successfully!"
        text += "\n--- " + str(table)

    text += "\n*** Populate table from csv"
    text += "\n" + botUsers_table.populate_from_csv()

    return text


def update_user_record(chat_id="", user_name="Noname", sett_dict=None, payment_dict=None):

    text = ""

    user_data_dict = {
        'pk_chat_id': chat_id,      # "4774374724",
        'sk_user_name': user_name,  # 'Serhii Surmylo',
        # 'last_time': '2022-12-11 21:11:17'
        }

    upd_data_dict = {}

    # User settings for chat
    # upd_data_dict['user_setting'] = {
    #     f'{opc.key_Geolocation}': 'WARSAW4',
    #     f'{opc.key_Interval}': '3.21',
    #     f'{opc.key_Reminder}': '0034'
    # }
    upd_data_dict['user_setting'] = sett_dict

    # User permition and payments
    # upd_data_dict['permition'] = {
    #     'payment': 32.37
    # }
    upd_data_dict['permition'] = payment_dict

    user_data_dict.update(upd_data_dict)

    resp = botUsers_table.put(user_data_dict=user_data_dict)

    text += "\n" + str(resp["ResponseMetadata"]["RequestId"])[:12] + "... "
    text += "" + str(resp["ResponseMetadata"]["HTTPStatusCode"]) + "/" + str(resp["ResponseMetadata"]["RetryAttempts"])

    return user_data_dict, text


def user_query_filter(lists_of_items, geo_name="", attr="weather", field="T"):
    '''
    :param lists_of_items:
    :param geo_name:
    :param attr:
    :param field:
    :return:
    '''

    value_list = []
    value_dict = {}

    for item in lists_of_items:

        print(">",  item)
        sort_key = item[botUsers_table.sort_key]
        city = item['location']['geo']
        value = item[attr][field]
        # print(">", sort_key, city, item[attr], value)

        # Filter by city
        if geo_name.upper() == city:

            # value_dict[res_sun_str] = mdates.date2num(observer.get_unaware)
            value_dict[sort_key] = float(value)

            value_list.append(float(value))

    average = 0
    if len(value_list) > 0:
        average = sum(value_list) / len(value_list)

    return value_dict, average


if __name__ == '__main__':

    # text = main_create_populate_bot_users()
    # print(text)
    # # ###########################################################################


    # setting_dict = {
    #     f'{opc.key_Geolocation}': 'WARSsdfAW4',
    #     f'{opc.key_Interval}': '3.212',
    #     f'{opc.key_Reminder}': '1134'
    # }
    #
    # data_dict, text = update_user_record(chat_id="333344452", user_name="Vasiya", sett_dict=setting_dict, payment_dict=None)
    # print(data_dict)
    # print(text)



    list_of_items = botUsers_table.table_query(_pk="442763659#REP",
                                               _between_low="2021-01-21 14:41:49",
                                               _between_high="2024-01-21 12:37:00")

    # pprint(list_of_items)
    # # # print(text)
    # data_dict, avg = main_query_filter(list_of_items, geo_name=geo_name, attr="weather", field="P")
    # pprint(data_dict)
