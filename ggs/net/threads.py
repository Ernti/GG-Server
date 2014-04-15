"""
Created on 13.12.2013

@author: udakak
"""

import json
from threading import Thread

from ggs.net.client import Client
from ggs.player import Player


class AcceptConnectionThread(Thread):

    def __init__(self, server):
        Thread.__init__(self)
        self.server = server

    def run(self):
        while not self.server.stop_requested:
            conn, addr = self.server.socket.accept()
            login_thread = LoginThread(self.server, conn, addr)
            login_thread.start()


class LoginThread(Thread):

    def __init__(self, server, conn, addr):
        Thread.__init__(self)
        self.server = server
        self.conn = conn
        self.addr = addr

    def run(self):
        data_json = self.conn.recv(1024)
        if data_json:
            data = json.loads(data_json.decode())
            if data['password'] == "iminspace":
                client = Client(self.server, self.conn, self.addr)
                client.subscribe(self.server.event_handler.handle)
                player = Player()
                player.ship.subscribe(self.server.event_handler.handle)
                client.player = player

                # Player will already exist at this point
                self.server.player.append(player)

                client.fire(type='connected')
            else:
                self.conn.send(('(' + json.dumps({'type': 'loginerror'}) + ')').encode())

