import boto3
import os
import sys
import pandas as pd
import datetime
import matplotlib.pyplot as plt
# %matplotlib inline


d = datetime.datetime.now()
Current_Date = "{}{}{}".format(d.month, d.day, d.year)
print(Current_Date)

client = boto3.client('s3')
response = client.create_bucket(ACL='private',
                                Bucket='serhiiimages{}'.format(Current_Date),
                                CreateBucketConfiguration={
                                    'LocationConstraint': 'eu-west-1'
                                }
                               )
print(response)


