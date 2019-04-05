# python-chat

A reliable chat application written in Python3.

## Features

This application supports chatting between multiple clients. When connecting to the server,
a client asked to enter a username which will become a unique identifier for the client while connected.
A list of all connected clients is then echo'd back to the newly connected client. The newly connected
client may then enter a unique identifier and will be placed inside a chatroom with the other client.
These chatrooms can support any amount of connections.

## Running the Application

1. Ensure that Python 3 is installed on your machine.

2. Cd into the `python-chat` folder.

3. Start the server by running:

```
> python3 src/server.py
```

4. Start any amount of clients (at least 2) to begin chatting:

```
> python3 src/client.py
```

