import json

class BasicResponse():
    def __init__(self, body):
        self.body = json.dumps(body)
        self.isBase64Encoded = False
        self.statusCode = 200

    def body(self):
        return self.body


class RoomError(BasicResponse):
    def __init__(self, error):
        super().__init__({'error': error, 'type': 'room_error'})
        self.statusCode = 500

class RoomCreated(BasicResponse):
    def __init__(self, room, host_id):
        super().__init__({'room': room, 'host_id': host_id, 'type': 'room_created'})

class RequestAccepted(BasicResponse):
    def __init__(self):
        super().__init__({'message': 'Request Accepted', 'type': 'request_accepted'})