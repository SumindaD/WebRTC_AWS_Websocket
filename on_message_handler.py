import json
import boto3
import os

dynamodb = boto3.client('dynamodb')


def handle(event, context):
    messageType = json.loads(event['body'])['type']
    messageData = json.loads(event['body'])['data']
    messageId = json.loads(event['body'])['id']
    
    paginator = dynamodb.get_paginator('scan')
    
    connectionIds = []

    apigatewaymanagementapi = boto3.client('apigatewaymanagementapi', 
    endpoint_url = "https://" + event["requestContext"]["domainName"] + "/" + event["requestContext"]["stage"])

    # Retrieve all connectionIds from the database
    for page in paginator.paginate(TableName=os.environ['SOCKET_CONNECTIONS_TABLE_NAME']):
        connectionIds.extend(page['Items'])

    # Emit the recieved message to all the connected devices
    for connectionId in connectionIds:
        apigatewaymanagementapi.post_to_connection(
            Data=json.dumps({"type": messageType, "data": messageData, "id": messageId}),
            ConnectionId=connectionId['connectionId']['S']
        )

    return {}