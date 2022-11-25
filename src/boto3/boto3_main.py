# eu - west - 1     Ireland
# AKIARXWKMEAH2CRR6ND3
# QqKSoaps4vq1tw+RciF9/CtyTf5qBLYuxGR+uZXU

# pip install awscli
# pip install boto3


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

    @property
    def get(self):
        response = self.table.get_item(
            Key={
                'Sensor_Id': "1"
            }
        )
        return response

    def put(self, sensor_id='', temperature='', humidity=''):
        response = self.table.put_item(
            Item={
                'Sensor_Id': sensor_id,
                'Temperature': temperature,
                'Humidity': humidity
            }
        )
        return response

    def delete(self, sensor_id=''):
        self.table.delete_item(
            Key={
                'Sensor_Id': sensor_id
            }
        )

    def describe_table(self):
        response = self.client.describe_table(
            TableName='DHT'
        )
        return response


obj = MyDb()
print(obj.describe_table())
data = obj.get
resp = obj.put(sensor_id='2', temperature='99', humidity='99')


# db = boto3.resource('dynamodb')
# table = db.Table('employees')
#
# table.put_item(
#     Item={
#         'emp_id': "3",
#         'name': "Erfvb",
#         'age': 24
#     }
# )

