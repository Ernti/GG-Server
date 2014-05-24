from ggs.event import Observable


class Ship(Observable):
    dummy_id = 0

    def __init__(self):
        self.soid = Ship.dummy_id
        Ship.dummy_id += 1
        self.target = (0, 0)
        self.x = 0
        self.y = 0
        self.r = 0
        Observable.__init__(self)

    def move(self, target):

        self.target = target

        self.fire(type='move')