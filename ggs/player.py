from ggs.ship import Ship


class Player(object):
    dummy_id = 0

    def __init__(self):
        self.id = Player.dummy_id
        print("new player id " + str(self.id))
        Player.dummy_id += 1
        self.ship = Ship()