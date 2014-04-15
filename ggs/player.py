from ggs.ship import Ship


class Player(object):
    dummy_id = 0

    def __init__(self):
        self.id = Player.dummy_id
        ++Player.dummy_id
        self.ship = Ship()