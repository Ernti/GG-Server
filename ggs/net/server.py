"""
Created on 13.12.2013

@author: u
"""
import json
import socket

from ggs.net.threads import AcceptConnectionThread


class Server(object):

    def __init__(self):
        self.stop_requested = False
        self.clients = []
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

    def player_action(self, message, acting_client):
        if message['type'] == 'playermoved':
            # TODO: check if in range
            for client in self.clients:
                if client != acting_client:
                    client.send(json.dumps({'type': 'spaceobjectmoved',
                                            'soid': self.clients.index(acting_client),
                                            'x': message['x'],
                                            'y': message['y']}))