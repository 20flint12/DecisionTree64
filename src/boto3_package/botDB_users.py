
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
        self._last_time_key = self._df.columns[2]       # to capture time moment !

        self.db = boto3.resource('dynamodb', region_name='eu-west-1')
        self.table = self.db.Table(self._table_name)
        self.client = boto3.client('dynamodb')

    @property
    def partition_key(self):

        return self._partition_key

    @property
    def sort_key(self):

        return self._sort_key

    @property
    def table_name(self):

        return self._table_name

    def get(self, pk="", sr=1):
        response = self.table.get_item(
            Key={
                self._partition_key: pk,
                # self._sort_key: sr
            }
        )
        return response

    def put(self, user_data_dict=None):     # at a current UTC time

        from decimal import Decimal
        import json

        # print("user_data_dict=", user_data_dict)

        # # Partition and Sorting keys
        # rec_items_dict = {
        #         self._partition_key: chat_id,
        #         self._sort_key: utc_str
        # }
        rec_items_dict = {}

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

    def table_scan(self):

        from boto3.dynamodb.conditions import Key, Attr

        response = self.table.scan()
        # response = self.table.query(
        #     KeyConditionExpression=Key(self._partition_key).eq(_pk) & Key(self._sort_key).between(_between_low, _between_high)
        # )
        items = response['Items']
        return items

    def table_query(self, _pk=""):

        from boto3.dynamodb.conditions import Key, Attr

        response = self.table.query(
            KeyConditionExpression=Key(self._partition_key).eq(_pk)
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


file_name = "bot_users.csv"
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


def _test_update_user_record(chat_id="", user_name="Noname", user_db_data=None, ):
    text = ""

    user_data_dict = {
        'pk_chat_id': str(chat_id),     # "4774374724",
        'sk_user_name': user_name,      # 'Serhii Surmylo',
        # 'last_time': '2022-12-11 21:11:17'
        }

    upd_data_dict = {}

    if "reminder_time" in user_db_data and user_db_data["reminder_time"]:
        upd_data_dict['reminder_time'] = user_db_data["reminder_time"]

    if "context_user_data" in user_db_data and user_db_data["context_user_data"]:
        upd_data_dict['context_user_data'] = user_db_data["context_user_data"]

    if "payment" in user_db_data and user_db_data["payment"]:
        upd_data_dict['payment'] = user_db_data["payment"]

    if "activity" in user_db_data and user_db_data["activity"]:
        upd_data_dict['activity'] = user_db_data["activity"]

    # upd_data_dict['context_data_dict'] = context_data_dict

    user_data_dict.update(upd_data_dict)

    resp = botUsers_table.put(user_data_dict=user_data_dict)

    text += "\n" + str(resp["ResponseMetadata"]["RequestId"])[:12] + "... "
    text += "" + str(resp["ResponseMetadata"]["HTTPStatusCode"]) + "/" + str(resp["ResponseMetadata"]["RetryAttempts"])

    return user_data_dict, text


def update_user_record(update=None, context=None, user_db_data=None):      # !!! user_db_data store in context_chat_data
    '''
    # User(first_name='Serhii', id=442763659, is_bot=False, language_code='en', last_name='Surmylo', username='Serhii_Surmylo')
    '''
    text = ""

    user = update.effective_user
    username = str(user.first_name) + " " + str(user.last_name) + " - " + str(user.username)

    user_data_dict = {'pk_chat_id': str(user.id), 'sk_user_name': username}

    upd_data_dict = {}

    if opc.key_Reminder in context.user_data and context.user_data[opc.key_Reminder]:
        upd_data_dict['reminder_time'] = context.user_data[opc.key_Reminder]

    if context.user_data is not None:
        upd_data_dict['context_user_data'] = context.user_data

    # print(user_db_data)
    '''
    # user_db_data = {
    #     'pk_chat_id': '333344452',
    #     'sk_user_name': 'Vasiya',
    #     'reminder_time': '0333',
    #     'activity': {'attempts': 2, 'state': True},
    #     'payment': {},
    #     'context_user_data': {
    #         f'{opc.key_Geolocation}': 'WARSfAW444',
    #         f'{opc.key_Interval}': '3.212',
    #         f'{opc.key_Reminder}': '1134'
    #         }
    #     }
    '''
    if "payment" in user_db_data:
        if user_db_data["payment"] or user_db_data["payment"] is not None:
            upd_data_dict['payment'] = user_db_data["payment"]
        else:
            upd_data_dict['payment'] = {}
    else:
        upd_data_dict['payment'] = {}

    if "activity" in user_db_data:
        if user_db_data["activity"]:
            upd_data_dict['activity'] = user_db_data["activity"]
        else:
            upd_data_dict['activity'] = {'attempts': 1, 'state': True}
    else:
        upd_data_dict['activity'] = {'attempts': 2, 'state': True}


    user_data_dict.update(upd_data_dict)

    resp = botUsers_table.put(user_data_dict=user_data_dict)

    text += "\n" + str(resp["ResponseMetadata"]["RequestId"])[:12] + "... "
    text += "" + str(resp["ResponseMetadata"]["HTTPStatusCode"]) + "/" + str(resp["ResponseMetadata"]["RetryAttempts"])

    return user_data_dict, text


def user_scan_filter(attr="weather"):

    list_of_items = botUsers_table.table_scan()

    count = len(list_of_items)

    return list_of_items, count


def get_user_db_data(pk=""):     # store this content in context.chat_data

    list_of_items = botUsers_table.table_query(_pk=pk)

    context_chat_data = list_of_items[0]

    return context_chat_data


if __name__ == '__main__':

    # text = main_create_populate_bot_users()
    # print(text)
    # # ###########################################################################



    # list_of_items = botUsers_table.table_query(_pk="442763659")
    # print(len(list_of_items), list_of_items[0])




    user_db_data = get_user_db_data(pk="33334445267")
    pprint(user_db_data)
    '''
    {'activity': {'attempts': Decimal('0'), 'state': True},
     'last_time': '2023-01-28 22:09:31',
     'payment': {},
     'pk_chat_id': '33334445267',
     'reminder_time': '0333',
     'sk_user_name': 'Vasiya-fake',
     'context_user_data': {'��������': '3.212',
                      '����������': 'WARSfAW444',
                      '�����������': '1134'}}
     '''




    # context_data_dict = {
    #     # 'pk_chat_id': '333344452',
    #     # 'sk_user_name': 'Vasiya',
    #     'reminder_time': '0333',
    #     'activity': {'attempts': 2, 'state': True},
    #     'payment': {},
    #     'context_user_data': {
    #         f'{opc.key_Geolocation}': 'WARSfAW444',
    #         f'{opc.key_Interval}': '3.212',
    #         f'{opc.key_Reminder}': '1134'
    #         }
    #     }
    att = int(user_db_data["activity"]["attempts"])    # !!! when wrong request !!!
    user_db_data["activity"]["attempts"] = att + 1
    if att >= 3:
        user_db_data["activity"]["state"] = False      # !!! check this state to know how work with user !!!
    else:
        user_db_data["activity"]["state"] = True
    data_dict, text = _test_update_user_record(chat_id="33334445267", user_name="Vasiya-fake",
                                               user_db_data=user_db_data,
                                               # context_data_dict=None,
                                               )
    pprint(data_dict)
    print(text)




    user_db_data = get_user_db_data(pk="33334445267")
    pprint(user_db_data)
    '''
    {'activity': {'attempts': Decimal('0'), 'state': True},
     'last_time': '2023-01-28 22:09:31',
     'payment': {},
     'pk_chat_id': '33334445267',
     'reminder_time': '0333',
     'sk_user_name': 'Vasiya-fake',
     'context_user_data': {'��������': '3.212',
                      '����������': 'WARSfAW444',
                      '�����������': '1134'}}
     '''

