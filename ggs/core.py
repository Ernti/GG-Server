"""
Created on 13.12.2013

@author: udakak
"""

import time

from ggs.net.server import Server
import socket


class Core(object):

    def __init__(self):
        self.stop_requested = False
        self.server = Server()

    def _start_server(self):
        self.server.start()

    def _stop_server(self):
        self.server.stop()

    def _tick(self):
        for client in self.server.clients:
            try:
                client['conn'].send("testy".encode())

            except socket.error:
                self.server.clients.remove(client)

    def _tick_loop(self):
        while not self.stop_requested:
            print("tick")
            self._tick()
            time.sleep(10)

    def run(self):
        self._start_server()
        self._tick_loop()

    def stop(self):
        self.stop_requested = True
        self._stop_server()
