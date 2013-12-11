'''
Created on 09.12.2013

@author: udakak
'''
import json
import socket
from threading import Thread
import time


clients = []
stop_requested = False

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 4455))
sock.listen(5)

class AcceptConnectionThread(Thread):
    
    def run(self):
        while not stop_requested:
            conn, addr = sock.accept()
            login_thread = LoginThread(conn, addr)
            login_thread.start()
      
class LoginThread(Thread):
    
    def __init__(self, conn, addr):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        
    
    def run(self):
        data_json = self.conn.recv(1024)
        if data_json:
            data = json.loads(data_json.decode())
            if data['username'] == "testname" and data['password'] == "iminspace":
                client = {'conn': self.conn, 'addr': self.addr}
                clients.append(client)
                client_id = clients.index(client)
                receive_thread = ReceiveThread(self.conn, self.addr, client_id)
                receive_thread.start()
            else:
                self.conn.send("loginerror".encode())
        
      
class ReceiveThread(Thread):
    
    def __init__(self, conn, addr, client_id):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.client_id = client_id
    
    def run(self):
        while not stop_requested:
            data = self.conn.recv(1024)
            if not data:
                clients.pop(self.client_id)
                break
            print(data)
            

def tick():
    for client in clients:
        client['conn'].send("testy".encode())

def shutdown():
    for client in clients:
        client['conn'].send("shutdown".encode())
    sock.shutdown

try:
    accept_connection_thread = AcceptConnectionThread();
    accept_connection_thread.start()
    
    while not stop_requested:
        print("tick")
        tick()
        time.sleep(10)
except KeyboardInterrupt:
    print("stopping...")
    stop_requested = True
    shutdown()
