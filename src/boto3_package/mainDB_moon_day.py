
# pip install awscli
# pip install boto3

# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html

import pandas as pd
import os

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

    def put(self, moon_zodiac_dict):
        # response = self.table.put_item(
        #     Item={
        #         self._partition_key: moon_zodiac_dict[self._partition_key],
        #         self._sort_key: moon_zodiac_dict[self._sort_key],
        #         'title': moon_zodiac_dict["title"],
        #         'symbol': moon_zodiac_dict["symbol"],
        #         'source': moon_zodiac_dict["source"],
        #         'description': moon_zodiac_dict["description"]
        #     },
        # )

        # Item = {}
        # Item.update(moon_zodiac_dict)  # !!!
        response = self.table.put_item(Item=moon_zodiac_dict)

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
                {'AttributeName': self._partition_key, 'AttributeType': 'N'},
                {'AttributeName': self._sort_key, 'AttributeType': 'N'}
            ],
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        }
        self.table = self.db.create_table(**params)
        self.table.wait_until_exists()

        return self.table

    def table_query(self, partition_key=1):

        from boto3.dynamodb.conditions import Key, Attr

        response = self.table.query(
            KeyConditionExpression=Key(self._partition_key).eq(partition_key)
        )
        items = response['Items']
        # print(items)
        return items

    def populate_from_csv(self):
        import time

        text = ""

        for i in range(0, len(self._df)):
            moon_zodiac_dict = self._df.loc[i].to_dict()

            resp = moonDay_table.put(moon_zodiac_dict)
            # print(".")
            text += str(i) + ": " + str(resp) + "\n"

            time.sleep(0.1)

        return text


file_name = "moon_day.csv"
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, file_name)
print(file_path)

moonDay_table = dynamoDB_table(path_file_csv=file_path)
print(moonDay_table)


def main_create_populate_moon_day_table():

    text = ""

    result, responce = moonDay_table.describe_table()

    if result:
        text += "\n*** Table already exists!"
        text += "\n" + str(responce)
    else:
        text += "\n--- " + str(responce)
        text += "\n*** Create table '" + moonDay_table._table_name + "' ..."
        table = moonDay_table.create_table()
        text += "\n*** Table created successfully!"
        text += "\n--- " + str(table)

    text += "\n*** Populate table from csv"
    text += "\n" + moonDay_table.populate_from_csv()

    return text


def main_get_item_moon_day(partition_key=1):

    text = ""

    list_of_items = moonDay_table.table_query(partition_key=partition_key)
    # print(list_of_items)
    text += "\nlen=" + str(len(list_of_items)) + "\n"

    return list_of_items, text


def string_between_tags(input_string='', tag_index=0):
    '''
    #MAIN
    #RELATION	Любовь и отношения
    #HOME		Домашние дела
    #HEALTH		Здоровье
    #BUSINESS	Бизнес и деньги
    #MYSTIC
    '''
    tags = ('#MAIN', '#RELATION', '#HOME', '#HEALTH', '#BUSINESS', '#MYSTIC')

    # idx_begin = input_string.find(tag_begin) + len(tag_begin)
    idx_begin = input_string.find(tags[tag_index]) + len(tags[tag_index])
    idx_end = input_string.find(tags[tag_index+1])

    res_substring = input_string[idx_begin:idx_end].strip()
    # print(idx_begin, idx_end, '\n=====\n')

    return res_substring


if __name__ == '__main__':

    # text = main_create_populate_moon_day_table()
    # print(text)

    # item_dict, text = main_get_item_moon_day(partition_key=3)
    # descr_str = item_dict[0]["description_0"]
    # # print(res_str)
    #
    # print(string_between_tags(input_string=descr_str, tag_index=0))


    item_dict, text = main_get_item_moon_day(partition_key=3)
    descr_str = item_dict[0]["description_1"]
    # print(res_str)

    print(string_between_tags(input_string=descr_str, tag_index=0))
