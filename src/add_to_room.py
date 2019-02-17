import json
from config import Config
from room_request import AddToRoomRequest, AddToRoomRequestToClient
from room_response import RoomError, RequestAccepted

import botocore
import boto3

def lambda_handler(event, context):
    body = json.loads(event['body'])
    request = AddToRoomRequest(**body)
    send_offer(event['requestContext'], request)
    response = RequestAccepted()
    return response.__dict__

def send_offer(request_context, request):
    endpoint = 'https://'+ request_context['domainName'] + '/' + request_context['stage']
    client = boto3.client('apigatewaymanagementapi', endpoint_url=endpoint)
    request_to_client = AddToRoomRequestToClient(request.answer)
    request_to_client_as_string = json.dumps(request_to_client.__dict__)
    client.post_to_connection(ConnectionId=request.client, Data=bytearray(request_to_client_as_string, 'utf-8'))