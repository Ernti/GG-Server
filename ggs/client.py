import json
import socket
import re
from threading import Thread


class ReceiveThread(Thread):

    def __init__(self, client):
        Thread.__init__(self)
        self.client = client

    def run(self):
        while self.client.alive:
            try:
                data = self.client.conn.recv(1024)
                for match_group in re.finditer("\{([^{}]+)\}", data.decode()):

                    data_json = json.loads('{' + match_group.group(1) + '}')
                    if data:
                        self.client.handle(data_json)
                    else:
                        self.client.handle({'type': 'removespaceobject'})
                        self.client.alive = False

            except socket.error:
                self.client.handle({'type': 'removespaceobject'})
                self.client.alive = False


class Client(object):

    def __init__(self, server, conn, addr):
        self.server = server
        self.conn = conn
        self.addr = addr
        self.alive = True
        self.receive_thread = ReceiveThread(self)
        self.receive_thread.start()

        self.server.player_action({'type': 'sendchatmessage', 'message': 'New Player connected!'}, self)

    def send(self, message):
        try:
            self.conn.send(message.encode())
        except socket.error:
            self.alive = False

    def handle(self, message):
        if message['type'] == 'playermoved':
            self.server.player_action(message, self)
        if message['type'] == 'removespaceobject':
            self.server.player_action(message, self)
        if message['type'] == 'sendchatmessage':
            self.server.player_action(message, self)
        #print(message)