import boto3
from boto3.dynamodb.conditions import Attr
from config import Config
from room_response import BasicResponse


def lambda_handler(event, context):
    connection_id = event['requestContext']['connectionId']
    room = get_hosts_room(connection_id)
    if room is None:
        return
    delete_room(room)
    return BasicResponse(body={})


# returns a roomName if the connectionId corresponds to a host
# returns None if not
def get_hosts_room(connection_id):
    dynamo = boto3.resource('dynamodb', region_name=Config.AWS_REGION)
    table = dynamo.Table(Config.ROOM_TABLE)
    response = table.scan(
        FilterExpression=Attr('host').eq(connection_id)
    )
    rooms = list(response['Items'])
    return next(iter(rooms), None)


def delete_room(room):
    dynamo = boto3.resource('dynamodb', region_name=Config.AWS_REGION)
    table = dynamo.Table(Config.ROOM_TABLE)
    table.delete_item(
        Key={
            'roomName': room['roomName']
        }
    )
    