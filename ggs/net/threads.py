'''
Created on 13.12.2013

@author: udakak
'''
import json
import socket
from threading import Thread


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
            if data['username'] == "testname" \
                        and data['password'] == "iminspace":

                client = {'conn': self.conn, 'addr': self.addr}
                self.server.clients.append(client)
                client_id = self.server.clients.index(client)
                self.conn.send("connected".encode())
                receive_thread = ReceiveThread(self.server,
                                               self.conn,
                                               self.addr,
                                               client_id)
                receive_thread.start()
            else:
                self.conn.send("loginerror".encode())


class ReceiveThread(Thread):

    def __init__(self, server, conn, addr, client_id):
        Thread.__init__(self)
        self.server = server
        self.conn = conn
        self.addr = addr
        self.client_id = client_id

    def run(self):
        while True:
            try:
                data = self.conn.recv(1024)
                if not data:
                    self.server.clients.pop(self.client_id)
                    break
                print(data)

            except socket.error:
                self._stop()
