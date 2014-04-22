"""
Created on 13.12.2013

@author: udakak
"""

import socket
from ggs.event import EventHandler

from ggs.net.threads import AcceptConnectionThread


class Server(object):
    def __init__(self):
        self.stop_requested = False
        self.event_handler = EventHandler(self)
        self.clients = []
        self.player = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.socket.bind(('', 4455))
        self.socket.listen(5)
        accept_connection_thread = AcceptConnectionThread(self)
        accept_connection_thread.daemon = True
        accept_connection_thread.start()

    def stop(self):
        self.stop_requested = True
        for client in self.clients:
            client.send("shutdown")
        self.socket.close()

    def broadcast(self, message, filter = None):
        for client in self.clients:
            if client is not filter:
                client.send(message)

    def handle(self, message, client):
        if message['type'] == 'playermoved':
            client.player.ship.move(message['x'], message['y'], message['r'])

        if message['type'] == 'sendchatmessage':
            self.broadcast({'type': 'sendchatmessage',
                            'sender': client.player.id,
                            'message': str(client.player.id) + ": " + message['message']})