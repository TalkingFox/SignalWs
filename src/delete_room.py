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
    free_word(room)
    deregister_host(connection_id)
    return BasicResponse(body={}).__dict__


# returns a roomName if the connectionId corresponds to a host
# returns None if not
def get_hosts_room(connection_id):
    dynamo = boto3.resource('dynamodb', region_name=Config.AWS_REGION)
    table = dynamo.Table(Config.HOST_TABLE)
    response = table.get_item(
        Key={
            'host': connection_id
        }
    )
    if 'Item' in response:
        return response['Item']['roomName']

    return None


def delete_room(room):
    dynamo = boto3.resource('dynamodb', region_name=Config.AWS_REGION)
    table = dynamo.Table(Config.ROOM_TABLE)
    table.delete_item(
        Key={
            'roomName': room
        }
    )


def free_word(word):
    dynamo = boto3.resource('dynamodb', region_name=Config.AWS_REGION)
    table = dynamo.Table(Config.WORDS_TABLE)
    table.update_item(
        Key={
            'wordsProperty': 'wordsInUse'
        },
        UpdateExpression='REMOVE propertyValue.#i',
        ExpressionAttributeNames={
            '#i': word
        }
    )


def deregister_host(host):
    dynamodb = boto3.resource('dynamodb', region_name=Config.AWS_REGION)
    table = dynamodb.Table(Config.HOST_TABLE)
    table.delete_item(
        Key={
            'host': host
        }
    )
