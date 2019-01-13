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