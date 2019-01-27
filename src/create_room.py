import random
import json
import boto3
from config import Config
from datetime import datetime
from room_response import RoomCreated

def lambda_handler(event, context):
    host_id = event["requestContext"]["connectionId"]
    dynamodb = boto3.resource('dynamodb', region_name=Config.AWS_REGION)
    table = dynamodb.Table(Config.ROOM_TABLE)
    room = get_open_room(table)
    response = table.put_item(
        Item={
            'roomName': room,
            'created': datetime.now().isoformat(),
            'host': host_id
        }
    )
    return RoomCreated(room).__dict__

def get_words():
    with open('words.txt') as f:
        content = f.readlines()
        content = [x.strip() for x in content]
        return content

def get_open_room(table):
    words = get_words()
    closed_rooms = get_closed_rooms()
    available = list(set(words) - set(closed_rooms))
    return random.choice(available)

def get_closed_rooms():
    dynamodb = boto3.resource('dynamodb', region_name=Config.AWS_REGION)
    table = dynamodb.Table(Config.WORDS_TABLE)
    response = table.get_item(
        Key={
            'state': 'state'
        }
    )
    data = response['Item']
    return data['value']['wordsInUse']
    