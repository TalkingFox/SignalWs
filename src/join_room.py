import json
from config import Config
from room_request import JoinRoomRequest, RoomRequest
from room_response import RoomError, RequestAccepted

import botocore
import boto3

def lambda_handler(event, context):
    connection_id = event['requestContext']['connectionId']
    body = json.loads(event['body'])
    request = JoinRoomRequest(**body)
    host = get_host(request.room)
    if host is None:
        return RoomError('Could not find room').__dict__
    send_offer(event['requestContext'], host, request.offer)
    return RequestAccepted().__dict__


def get_host(room):
    dynamo = boto3.resource('dynamodb', region_name=Config.AWS_REGION)
    table = dynamo.Table(Config.ROOM_TABLE)
    response = table.get_item(
        Key={
            'roomName': room
        }
    )
    if 'Item' not in response:
        return None
    found_room = response['Item']['host']
    return found_room


def send_offer(request_context, host, offer):
    endpoint = 'https://'+ request_context['domainName'] + '/' + request_context['stage']
    client = boto3.client('apigatewaymanagementapi', endpoint_url=endpoint)
    client.post_to_connection(ConnectionId=host, Data=bytearray(offer, 'utf-8'))
