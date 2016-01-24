# Test to have a first idea on how good asyncio works
# This test asumes that there are N network connection where the system is listening
# Pick a random available connection and send a stimulus (ON,OFF), wait a random time
# and start again

# If we want to stress the system more, we should create a thread per connection and send
# stimulus

import socket
import random
import time

messages = [b"ON", b"OFF"]
sockets = []
sleep_times = [0.5, 0.3, 0.2, 0, 0.1]


def create_clients(number, start_port):

    for i in range(1, number + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        server_address = ('localhost', start_port + i)
        sock.connect(server_address)
        print("client in {}".format(sock.getsockname()))
        print("client connecting to {}".format(sock.getpeername()))
        time.sleep(1)
        sockets.append(sock)

    while True:
        message = random.choice(messages)
        client = random.choice(sockets)
        st = random.choice(sleep_times)
        client.sendall(message)
        print('{} --> {}: {!r} -- sleeping {}'.format(client.getsockname(),client.getpeername(), message, st))
        time.sleep(st)


def create_client(start_port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        server_address = ('localhost', start_port)
        sock.connect(server_address)
        print("Client starting at {}".format(sock.getsockname()))
        print("client connecting to {}".format(server_address))
        message = random.choice(messages)
        print("Sending: message {}".format(message))
        sock.sendall(message)
        time.sleep(random.choice(sleep_times))
        message = random.choice(messages)
        print("Sending: message {}".format(message))
        sock.sendall(message)
        time.sleep(random.choice(sleep_times))

        print("BYE")

if __name__ == '__main__':
    create_clients(3, 8887)
