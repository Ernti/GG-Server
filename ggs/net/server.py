'''
Created on 13.12.2013

@author: u
'''
import socket

from ggs.net.threads import AcceptConnectionThread


class Server(object):

    def __init__(self):
        self.stop_requested = False
        self.clients = []

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', 4455))
        self.socket.listen(5)
        self.accept_connection_thread = AcceptConnectionThread(self)
        self.accept_connection_thread.daemon = True
        self.accept_connection_thread.start()

    def stop(self):
        self.stop_requested = True
        for client in self.clients:
            client['conn'].send("shutdown".encode())
        self.socket.close()
