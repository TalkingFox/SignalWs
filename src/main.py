import json

def lambda_handler(event, context):
    print('event')
    print(json.dumps(event))
    print('context')
    print(json.dumps(context))
    return {
        'message': 'ok'
    }

if __name__ == "__main__":
    lambda_handler({'event':'pooped'},{'context': 'butt'})