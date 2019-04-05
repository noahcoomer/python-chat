## Noah Coomer & Casey Satran
## server.py

import socket
import random
import ssl
from threading import Thread

class Server(object):
    sock = None
    room_count = 0
    clients = {}
    clients_to_rooms = {}
    rooms_to_clients = {}
    

    def __init__(self, addr='localhost', port=1234):
        '''
        Start the server node
        '''
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = addr
        self.port = port
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        print("Server initialized successfully. (host: ", self.host, ") (port: ", self.port, ")")
        
        while True:
            client_sock, addr = self.sock.accept()
            print(addr[0], " just connected.")
            thr = Thread(target=self.client_thread, args=(client_sock, addr,))
            thr.start()
        

    def assign_uid(self, client_sock, addr):
        '''
        Assign a UID to the client of the form: UID = name + random_number
        '''
        print("Assigning a uid to: ", addr)
        while True:
            try:
                client_sock.send("Enter a username: ".encode())
                name = client_sock.recv(2048)
                if name == bytes('.exit', 'utf-8'):
                    break
                num = str(random.randint(1000, 9999))
                uid = name.decode() + num
                self.clients[uid] = client_sock
                client_sock.send(bytes("Your uid is: " + uid + "\n", 'utf-8'))
                print("Successfully added ", uid, " to the server.")
                return uid
            except IOError as e:
                client_sock.send(bytes("Invalid input. Please try again.\n", 'utf-8'))
                print("Invalid input from client. Trying again.")
                continue
            except Exception as e:
                print(e)
                client_sock.send(bytes("Fatal error.\n", 'utf-8'))
                print("Fatal error occurred. Exiting.")
                self.sock.close()
                break


    def echo_clients(self, client_sock, addr, uid):
        '''
        Echo the currently connected clients to a newly connected client
        '''
        print("Echoing connections to: ", uid, addr)
        client_sock.send(bytes("Clients currently online:\n ", 'utf-8'))
        clients_str = ''
        for client in self.clients.keys():
            clients_str += client + "\n"
        client_sock.send(clients_str.encode())
        if len(self.clients) == 1:
            return
        
        while True:
            client_sock.send("Enter the uid of the client you would like to chat with.".encode())
            partner = client_sock.recv(2048).decode()
            # Make sure the partner uid is connected and user did not enter own uid
            if partner not in self.clients or partner == uid:
                client_sock.send("Invalid uid. Try again.".encode())
                continue
            # find the partner's room and add the new client to it
            if partner in self.clients_to_rooms:
                room = self.clients_to_rooms[partner]
                self.clients_to_rooms[uid] = room
                self.rooms_to_clients[room].append(uid)
                msg = uid + " has entered the chat room."
                self.broadcast_message(uid, msg)
                return
            else:
                # if no rooms, then make a new one
                self.clients_to_rooms[uid] = self.room_count
                self.clients_to_rooms[partner] = self.room_count
                self.rooms_to_clients[self.room_count] = [uid, partner]
                self.room_count += 1
                self.broadcast_message(uid, "Started a chat room with you.")
                return


    def broadcast_message(self, uid, message):
        '''
        Broadcast a message from a client identified by uid to the room they are in
        '''
        room = self.clients_to_rooms[uid]
        clients = self.rooms_to_clients[room]

        for client in clients:
            sock = self.clients[client]
            sock.sendall(bytes("<" + uid + "> " + message, "utf-8"))


    def client_thread(self, client_sock, addr):
        '''
        Start a new thread for each client
        '''
        client_sock.send("Welcome to Python Chat!\n".encode())
        #client_sock.send("Enter 'help' for a list of available commands.\n".encode())

        # Try to assign the user a uid and echo them the clients
        try:
            uid = self.assign_uid(client_sock, addr)
            self.echo_clients(client_sock, addr, uid)
        except Exception as e:
            print(e)
            return 0

        while True:
            command = client_sock.recv(4096)
            if command != bytes('.exit', 'utf-8'):
                print("Received message from: ", addr, '\n')
                message = command.decode()
                self.broadcast_message(uid, message) 
            else:
                print("Removing connection with: ", addr)
                self.clients[uid].close()
                del self.clients[uid]
                return 1


if __name__ == '__main__':
    addr = input("Enter your IP (leave blank for localhost): ")
    if addr == '':
        addr = 'localhost'

    try:
        port = int(input("Enter a port number (leave blank for 1234): "))
    except ValueError:
        port = 1234

    try:
        Server(addr=addr, port=port)
    except OSError:
        print("Port already in use. Randomly trying another.")
        port = random.randint(10000, 99999)
        Server(addr=addr, port=port)
    
