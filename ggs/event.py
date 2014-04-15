class Event(object):
    pass


class Observable(object):
    def __init__(self):
        self.callbacks = []

    def subscribe(self, callback):
        self.callbacks.append(callback)

    def fire(self, **attrs):
        event = Event()
        event.source = self
        for key, value in attrs.items():
            setattr(event, key, value)
        for fn in self.callbacks:
            fn(event)


class EventHandler(object):
    def __init__(self, server):
        self.server = server

    def handle(self, event):
        if event.type == 'move':
            self.server.broadcast({'type': 'spaceobjectmoved',
                                   'x': event.source.x,
                                   'y': event.source.y,
                                   'r': event.source.r})

        if event.type == 'connected':
            self.server.clients.append(event.source)

            self.server.broadcast({'type': 'newspaceobject',
                                   'soid': event.source.player.ship.soid})
            self.server.broadcast({'type': 'sendchatmessage',
                                   'message': 'New Player ' + str(event.source.player.id) + ' connected!'})
            event.source.send({'type': 'connected'})
            for client in self.server.clients:
                if client is not event.source:
                    client.send({'type': 'newspaceobject',
                                 'soid': client.player.ship.soid})

        if event.type == 'disconnected':
            self.server.clients.remove(event.source)
            self.server.broadcast({'type': 'removespaceobject',
                                   'soid': event.source.player.ship.soid})
            self.server.broadcast({'type': 'sendchatmessage',
                                   'message': 'Player ' + str(event.source.player.id) + ' has disconnected!'})