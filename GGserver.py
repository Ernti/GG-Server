'''
Created on 09.12.2013

@author: udakak
'''
import socket, time
from threading import Thread

clients = []
stop_requested = False

class AcceptConnectionThread(Thread):
    
    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', 4455))
        sock.listen(5)
        while not stop_requested:
            conn, addr = sock.accept()
            client = {'conn': conn, 'addr': addr}
            clients.append(client)
            client_id = clients.index(client)
            receive_thread = ReceiveTread(conn, addr, client_id)
            receive_thread.start()
            
class ReceiveTread(Thread):
    
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
