"""
Created on 13.12.2013

@author: udakak
"""

import json
from threading import Thread
import re

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
        data = self.conn.recv(1024)
        for match_group in re.finditer("\(([^()]+)\)", data.decode()):

            data_json = json.loads(match_group.group(1))

            if data_json['password'] == "iminspace":
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

