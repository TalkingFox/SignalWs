import random
import json
import boto3
from config import Config
from datetime import datetime
from room_response import RoomCreated

def lambda_handler(event, context):
    host_id = event["requestContext"]["connectionId"]
    room = get_open_room()
    create_room(room, host_id)
    reserve_word(room)
    register_host(host_id, room)
    return RoomCreated(room).__dict__

def get_words():
    with open('words.txt') as f:
        content = f.readlines()
        content = [x.strip() for x in content]
        return content

def get_open_room():
    words = get_words()
    closed_rooms = get_closed_rooms()
    available = list(set(words) - set(closed_rooms))
    return random.choice(available)

def get_closed_rooms():
    dynamodb = boto3.resource('dynamodb', region_name=Config.AWS_REGION)
    table = dynamodb.Table(Config.WORDS_TABLE)
    response = table.get_item(
        Key={
            'wordsProperty': 'wordsInUse'
        }
    )
    data = response['Item']
    return list(data['propertyValue'].keys())
    
def create_room(room, host):
    dynamodb = boto3.resource('dynamodb', region_name=Config.AWS_REGION)
    table = dynamodb.Table(Config.ROOM_TABLE)
    response = table.put_item(
        Item={
            'roomName': room,
            'created': datetime.now().isoformat(),
            'host': host
        }
    )

def register_host(host, room):
    dynamodb = boto3.resource('dynamodb', region_name=Config.AWS_REGION)
    table = dynamodb.Table(Config.HOST_TABLE)
    table.put_item(
        Item={
            'roomName': room,
            'created': datetime.now().isoformat(),
            'host': host
        }
    )

def reserve_word(word):
    dynamodb = boto3.resource('dynamodb', region_name=Config.AWS_REGION)
    table = dynamodb.Table(Config.WORDS_TABLE)
    table.update_item(
        Key={
            'wordsProperty': 'wordsInUse'
        },
        UpdateExpression='SET propertyValue.#i = :i',
        ExpressionAttributeValues={
            ':i': word,
        },
        ExpressionAttributeNames={
            '#i': word
        }
    )