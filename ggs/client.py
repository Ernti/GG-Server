import json
import socket
from threading import Thread


class ReceiveThread(Thread):

    def __init__(self, client):
        Thread.__init__(self)
        self.client = client

    def run(self):
        while self.client.alive:
            try:
                data = self.client.conn.recv(1024)
                if data:
                    self.client.handle(json.loads(data.decode()))

            except socket.error:
                self.client.alive = False


class SendThread(Thread):

    def __init__(self, client):
        Thread.__init__(self)
        self.client = client

    def run(self):
        while self.client.alive:
            for message in self.client.message_queue:
                try:
                    self.client.conn.send(message.encode())
                except socket.error:
                    self.client.alive = False


class Client(object):

    def __init__(self, server, conn, addr):
        self.server = server
        self.conn = conn
        self.addr = addr
        self.alive = True
        self.message_queue = []
        self.receive_thread = ReceiveThread(self)
        self.receive_thread.start()
        self.send_thread = SendThread(self)
        self.send_thread.start()

    def send(self, message):
        self.message_queue.append(message)

    def handle(self, message):
        if message['type'] == 'playermoved':
            self.server.player_action(message, self)
        print(message)