class RoomRequest:
    def __init__(self, type, **kwargs):
        self.type = type
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def action(self):
        return self.action

class JoinRoomRequest(RoomRequest):
    def __init__(self, **kwargs):
        super().__init__('join_room', **kwargs)
    
    def room(self):
        return self.room

    def offer(self):
        return self.offer

class JoinRoomRequestToHost(RoomRequest):
    def __init__(self, offer, connection_id):
        super().__init__('guest_request')
        self.offer = offer
        self.client = connection_id

class AddToRoomRequest(RoomRequest):
    def __init__(self, **kwargs):
        super().__init__('add_to_room', **kwargs)

    def client(self):
        return self.client
    
    def answer(self):
        return self.answer

class AddToRoomRequestToClient(RoomRequest):
    def __init__(self, answer):
        super().__init__('room_joined')
        self.answer = answer