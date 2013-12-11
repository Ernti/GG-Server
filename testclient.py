'''
Created on 11.12.2013

@author: udakak
'''

import socket
from threading import Thread

stop_requested = False

class TestThread(Thread):
    
    def run(self):
        while not stop_requested:
            data = sock.recv(1024)
            if data == "shutdown":
                sock.close()
            print(data)
        
        

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 4455))
    sock.send("Test".encode())
    testthread = TestThread()
    testthread.start()
except KeyboardInterrupt:
    stop_requested = True