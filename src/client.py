## Noah Coomer & Casey Satran
## client.py

import socket
import threading

class Client:
    sock = None
    host = 'localhost'
    port = 6969
    
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

        send_thread = threading.Thread(target=self.send_thread)
        receive_thread = threading.Thread(target=self.receive_thread)
        send_thread.start()
        receive_thread.start()
        

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

    
Client()
