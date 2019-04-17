## Noah Coomer & Casey Satran
## client.py

import socket
import random
import ssl
from threading import Thread

class Client(object):
    sock = None
    
    def __init__(self, addr='localhost', port=1234):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = addr
        self.port = port
        self.sock.connect((self.host, self.port))
        print("Successfully connected to server.")

        send = Thread(target=self.send_thread)
        receive = Thread(target=self.receive_thread)
        send.start()
        receive.start()
        

    def send_thread(self):
        while True:
            message = input()
            if message == '.exit':
                self.sock.sendall(message.encode())
                self.sock.close()
                return 0
            else:
                self.sock.sendall(message.encode())
        

    def receive_thread(self):
        while True:
            message = self.sock.recv(2048)
            if message:
                print(message.decode())


    def exit(self):
        pass

if __name__ == '__main__':
    addr = input("Enter your IP (leave blank for localhost): ")
    if addr == '':
        addr = 'localhost'
    
    try:
        port = int(input("Enter the port (Leave blank for 1234): "))
    except ValueError:
        port = 1234
    
    try:
        Client(addr=addr, port=port)
    except OSError:
        print("Port already in use. Randomly trying another.")
        port = random.randint(10000, 99999)
        Client(addr=addr, port=port)
