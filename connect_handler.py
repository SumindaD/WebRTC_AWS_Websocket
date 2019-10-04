import json
import boto3
import os

dynamodb = boto3.client('dynamodb')

def handle(event, context):
    connectionId = event['requestContext']['connectionId']

    # Insert the connectionId of the connected device to the database
    dynamodb.put_item(TableName=os.environ['SOCKET_CONNECTIONS_TABLE_NAME'], Item={'connectionId': {'S': connectionId}})

    return {}