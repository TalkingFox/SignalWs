class RoomRequest:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def action(self):
        return self.action    

class JoinRoomRequest(RoomRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def room(self):
        return self.room

    def offer(self):
        return self.offer

class JoinRoomRequestToHost(RoomRequest):
    def __init__(self, offer, connection_id):
        super()
        self.offer = offer
        self.client = connection_id

class AddToRoomRequest(RoomRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def client(self):
        return self.client
    
    def answer(self):
        return self.answer

class AddToRoomRequestToClient(RoomRequest):
    def __init__(self, answer):
        super()
        self.answer = answer