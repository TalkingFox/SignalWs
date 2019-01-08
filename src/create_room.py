import random
import json
import boto3
from config import Config
from datetime import datetime

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
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "body": room
    }

def get_words():
    with open('words.txt') as f:
        content = f.readlines()
        content = [x.strip() for x in content]
        return content

def get_open_room(table):
    words = get_words()
    closed_rooms = get_closed_rooms(table)
    available = list(set(words) - set(closed_rooms))
    return random.choice(available)

def get_closed_rooms(table):
    response = table.scan(
        ProjectionExpression="roomName"
    )
    data = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table.scan(
            ExclusiveStartKey=response['LastEvaluatedKey'],
            ProjectionExpression="roomName"
        )
        data.extend(response['Items'])
    return list(map(lambda x: x['roomName'], data))

if __name__ == "__main__":
    lambda_handler({'event':'pooped'},{'context': 'butt'})