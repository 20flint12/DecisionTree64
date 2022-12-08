# pip install awscli
# pip install boto3

# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html

import pandas as pd

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
                'zod_id': pk,
                'element_id': sr
            }
        )
        return response

    def put(self, moon_zodiac_dict):
        response = self.table.put_item(
            Item={
                'zod_id': moon_zodiac_dict["zod_id"],
                'element_id': moon_zodiac_dict["element_id"],
                'title': moon_zodiac_dict["title"],
                'symbol': moon_zodiac_dict["symbol"],
                'source': moon_zodiac_dict["source"],
                'description': moon_zodiac_dict["description"]
            }
        )
        return response

    def delete(self, sensor_id=''):
        self.table.delete_item(
            Key={
                'zod_id': sensor_id
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
                {'AttributeName': 'zod_id', 'KeyType': 'HASH'},
                {'AttributeName': 'element_id', 'KeyType': 'RANGE'}
            ],
            'AttributeDefinitions': [
                {'AttributeName': 'zod_id', 'AttributeType': 'N'},
                {'AttributeName': 'element_id', 'AttributeType': 'N'}
            ],
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 12,
                'WriteCapacityUnits': 12
            }
        }
        self.table = self.db.create_table(**params)
        # print(f"Creating {self.Table_Name}...")
        str_info += f"\nCreating {self.Table_Name}..."
        self.table.wait_until_exists()

        return self.table, str_info

    def table_query(self, zod_id=1):

        from boto3.dynamodb.conditions import Key, Attr

        response = self.table.query(
            KeyConditionExpression=Key('zod_id').eq(zod_id)
        )
        items = response['Items']
        # print(items)
        return items


def main_create_populate_moon_zodiac():

    out_str = ""

    res_table = obj.describe_table()
    out_str += "\n" + str(res_table) + "\n"

    if res_table == "ResourceNotFoundException":
        pass
        out_str += "\n\n*** Create table"
        table, str_info = obj.create_table()
        out_str += "\n" + str_info

    # *** Populate table from csv
    df = pd.read_csv('moon_zodiac.csv')
    # print(df.info())

    for i in range(0, len(df)):
        moon_zodiac_dict = df.loc[i].to_dict()
        # print(moon_zodiac_dict)

        resp = obj.put(moon_zodiac_dict)
        out_str += str(resp) + "\n"

    return out_str


def main_get_item_moon_zodiac(zod_id=1):

    out_str = ""

    # res_item = obj.get(2, 2)
    list_of_items = obj.table_query(zod_id=zod_id)
    # print(res_item1["Item"])
    out_str += "\n" + str(list_of_items) + "\n"

    return list_of_items[0], out_str


obj = MyDb(table_name='moon_zodiac')


if __name__ == '__main__':

    # res = main_create_populate_moon_zodiac()
    item_dict, res_str = main_get_item_moon_zodiac(3)
    print(item_dict)
    # print(res_str)
