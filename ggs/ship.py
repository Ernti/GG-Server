from ggs.event import Observable


class Ship(Observable):
    dummy_id = 0

    def __init__(self):
        self.soid = Ship.dummy_id
        ++Ship.dummy_id
        self.x = 0
        self.y = 0
        self.r = 0
        Observable.__init__(self)

    def move(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.fire(type='move')