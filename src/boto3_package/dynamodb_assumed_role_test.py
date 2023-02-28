# -*- coding: utf-8 -*-

import json
import os

from src.scikit_mathplot import main_binance_plot as dfdfd
import boto3


def get_credentials(service="", account=""):

    script_dir = os.path.dirname(os.path.abspath(__file__))
    # print(script_dir)
    script_dir_up = os.path.dirname(script_dir)
    # print(script_dir_up)
    script_dir_up_up = os.path.dirname(script_dir_up)
    # print(script_dir_up_up)
    file_name = "credentials.json"
    file_path = os.path.join(script_dir_up_up, file_name)
    # print(file_path)

    with open(file_path, 'r') as f:
        print(f)
        config = json.load(f)

    data_dict = config[service][account]

    return data_dict



if __name__ == '__main__':

    aws_credentials = get_credentials("AWS", "flint2")
    print(aws_credentials)



    # Create an Amazon DynamoDB client object
    dynamodb_client = boto3.client('dynamodb',
                                   region_name=aws_credentials["region_name"],
                                   aws_access_key_id=aws_credentials["access_key_id"],
                                   aws_secret_access_key=aws_credentials["secret_access_key"]
                                   )
    response = dynamodb_client.list_tables()
    print("dynamodb=", dynamodb_client, response)

    # Create a session object
    session = boto3.Session(aws_access_key_id=aws_credentials["access_key_id"],
                            aws_secret_access_key=aws_credentials["secret_access_key"],
                            # aws_session_token='your-temporary-session-token',
                            region_name=aws_credentials["region_name"],
                            # profile_name='flint2-profile',
                            # botocore_session=boto3.session.Session()
                            )
    print("session=", session)

    # Assume a role in the account that owns the table
    sts = session.client('sts')
    my_token = sts.get_session_token()
    print("sts=", sts, my_token)

    #
    # assumed_role_object = sts.assume_role(
    #     RoleArn=aws_credentials["RoleArn"],
    #     RoleSessionName=aws_credentials["RoleSessionName"]
    # )
    # print("assumed_role_object=", assumed_role_object)
    #
    #
    # credentials = assumed_role_object['Credentials']
    # print("credentials=", credentials)
