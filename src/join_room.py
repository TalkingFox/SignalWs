import boto3, json
from config import Config
from room_request import JoinRoomRequest, RoomRequest
from room_response import RoomError

def lambda_handler(event, context):
    connection_id = event['requestContext']['connectionId']
    request = JoinRoomRequest(**event['body'])
    host = get_host(request.room)
    if host is None:
        return RoomError('Could not find room')
    send_offer(host, request.offer)
    
def get_host(room):
    dynamo = boto3.resource('dynamodb', region_name=Config.AWS_REGION)
    table = dynamo.Table(Config.ROOM_TABLE)
    response = table.get_item(
        Key={
            'roomName': room
        }
    )
    if 'item' not in response:
        return None    
    found_room = response['Item']
    return found_room

def send_offer(host, offer):
    client = boto3.client('apigatewaymanagementapi')
    client.post_to_connection(ConnectionId=host, Data=offer)