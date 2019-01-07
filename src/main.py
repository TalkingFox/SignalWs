import json

def lambda_handler(event, context):
    print('event')
    print(json.dumps(event))
    print('context')
    print(context)
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "body": "Coolio!"
    }

if __name__ == "__main__":
    lambda_handler({'event':'pooped'},{'context': 'butt'})