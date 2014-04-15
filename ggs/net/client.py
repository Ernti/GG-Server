import json
import socket
import re
from threading import Thread
from ggs.event import Observable


class ReceiveThread(Thread):

    def __init__(self, client):
        Thread.__init__(self)
        self.client = client

    def run(self):
        while self.client.alive:
            try:
                data = self.client.conn.recv(1024)
                #print(data)
                for match_group in re.finditer("\(([^()]+)\)", data.decode()):

                    data_json = json.loads(match_group.group(1))
                    if data:
                        self.client.handle(data_json)
                    else:
                        self.client.fire(type='disconnected')

            except socket.error:
                self.client.fire(type='disconnected')


class Client(Observable):

    def __init__(self, server, conn, addr):
        self.server = server
        self.conn = conn
        self.addr = addr
        self.receive_thread = ReceiveThread(self)
        self.receive_thread.start()
        Observable.__init__(self)

    def send(self, message):
        try:
            self.conn.send(('(' + json.dumps(message) + ')').encode())
        except socket.error:
            self.fire(type='disconnected')

    def handle(self, message):
        self.server.handle(message, self)