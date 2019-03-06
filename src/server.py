## Noah Coomer & Casey Satran
## server.py

import socket
import random
from thread import *

class Server:
    sock = None
    host = ''
    port = 6969
    clients = {}
    

    def start():
        '''
        Start the server node
        '''
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        sock.bind((host, port))
        sock.listen(10)

        while True:
            client_sock, addr = sock.accept()
            print(addr[0], " just connected.")
            start_new_thread(client_thread, (client_sock, addr))
        

    def assign_uid(client_sock, addr):
        '''
        Assign a UID to the client of the form: UID = name + random_number
        '''
        client_sock.send("Enter a username: ")

        while True:
            try:
                name = client_sock.recv(2048)
                if name:
                    num = str(randint(1000, 9999))
                    clients[name + num] = addr
                else:
                    remove(client_sock)
            except:
                continue


    def echo_clients(client_sock):
        '''
        Echo the currently connected clients to a newly connected client
        '''
        client_sock.send("Clients currently online: ")
        clients_str = ''
        for client in clients.keys():
            clients_str += client + "/n"
        client_sock.send(clients_str)


    def client_thread(client_sock, addr):
        client_sock.send("Welcome to Python Chat!")
        client_sock.send("Enter 'help' for a list of available commands.")
            
        assign_uid(client_sock, addr)
        echo_clients(client_sock)

        while True:
            command = client_sock.recv(4096)

            if command:
                print()
            else:
                remove(client_sock)


server = Server()
server.start()
