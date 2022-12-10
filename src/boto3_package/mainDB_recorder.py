
import pandas as pd
from datetime import datetime as dt
import src.ephem_routines.ephem_package.moon_day as md
import src.ephem_routines.ephem_package.sun_rise_sett as sr
import src.ephem_routines.ephem_package.zodiac_phase as zd
import src.weather_package.main_openweathermap as wt



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
        self.db = boto3.resource('dynamodb')
        self.table = self.db.Table(table_name)
        self.client = boto3.client('dynamodb')

    # @property
    def get(self, pk=1, sr=1):
        response = self.table.get_item(
            Key={
                'rec_id': pk,
                'time_sr': sr
            }
        )
        return response

    def put(self, data_dict):
        response = self.table.put_item(
            Item={
                'rec_id': data_dict["rec_id"],
                'time_sr': data_dict["time_sr"],
                # *** Weather data
                'temperature': int(data_dict["temperature"]),
                'pressure': int(data_dict["pressure"]),
                'humidity': int(data_dict["humidity"])
            }
        )
        return response

    def delete(self, pk=1):
        self.table.delete_item(
            Key={
                'rec_id': pk
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
                {'AttributeName': 'rec_id', 'KeyType': 'HASH'},
                {'AttributeName': 'time_sr', 'KeyType': 'RANGE'}
                # {'AttributeName': 'temperature', 'KeyType': 'RANGE'}
            ],
            'AttributeDefinitions': [
                {'AttributeName': 'rec_id', 'AttributeType': 'N'},
                {'AttributeName': 'time_sr', 'AttributeType': 'N'}
                # {'AttributeName': 'temperature', 'AttributeType': 'N'}
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

    def table_query(self, rec_id=1):

        from boto3.dynamodb.conditions import Key, Attr

        response = self.table.query(
            KeyConditionExpression=Key('rec_id').eq(rec_id)
        )
        items = response['Items']
        return items


def main_create_record():

    out_str = ""

    res_table = obj.describe_table()
    out_str += "\n" + str(res_table) + "\n"

    if res_table == "ResourceNotFoundException":
        pass
        out_str += "\n\n*** Create table"
        table, str_info = obj.create_table()
        out_str += "\n" + str_info

    # *** Populate table from csv
    # df = pd.read_csv('moon_zodiac.csv')
    # print(df.info())

    # for i in range(0, len(df)):
    #     moon_zodiac_dict = df.loc[i].to_dict()
    #     # print(moon_zodiac_dict)
    #
    #     resp = obj.put(moon_zodiac_dict)
    #     out_str += str(resp) + "\n"

    data_dict = {"rec_id": 1, "time_sr": 1}
    resp = obj.put(data_dict)
    out_str += str(resp) + "\n"

    return out_str


def main_put_record():
    global init_id

    out_str = ""
    dts = int(dt.now().timestamp())

    if init_id == 0:
        table_dict = obj.describe_table()
        # init_id = int(table_dict["Table"]["ItemCount"])
        # init_id = int(table_dict["Table"]["TableSizeBytes"] / 2)
        init_id = dts - 670000000   # clear some digits

    else:
        init_id += 1
    # print(init_id)

    data_dict = {"rec_id": init_id, "time_sr": dts}

    # Weather data
    wth_dict, str_head = wt.main_weather_now("Mragowo", dt.today())
    data_dict["temperature"] = wth_dict["temperature"]
    data_dict["pressure"] = wth_dict["pressure"]
    data_dict["humidity"] = wth_dict["humidity"]

    resp = obj.put(data_dict)

    out_str += "\n" + str(resp["ResponseMetadata"]["RequestId"])[:12] + "... "
    out_str += "" + str(resp["ResponseMetadata"]["HTTPStatusCode"]) + "/" + str(resp["ResponseMetadata"]["RetryAttempts"])

    out_str += "\n" + str(init_id) + " "

    return init_id, out_str


def main_get_record(rec_id=1):

    out_str = ""

    # res_item = obj.get(2, 2)
    list_of_items = obj.table_query(rec_id=rec_id)
    # print(res_item1["Item"])
    out_str += "\n" + str(list_of_items) + "\n"

    return list_of_items[0], out_str


obj = MyDb(table_name='main_records')
init_id = 0

if __name__ == '__main__':

    # res_str = main_create_record()
    # item_dict, res_str = main_get_item_moon_zodiac(3)
    init_id, out_str = main_put_record()
    # print(item_dict)
    print(out_str)

    init_id, out_str = main_put_record()
    # print(item_dict)
    print(out_str)

    init_id, out_str = main_put_record()
    # print(item_dict)
    print(out_str)

    init_id, out_str = main_put_record()
    # print(item_dict)
    print(out_str)
