#!/usr/bin/env python

import argparse
import zmq

context = zmq.Context()

socket = context.socket(zmq.DEALER)

parser = argparse.ArgumentParser()
#parser.add_argument('-c', '--connect-address', default='tcp://127.0.0.1:5555')
parser.add_argument('-c', '--connect-address', default='tcp://172.16.17.133:5555')
parser.add_argument('-p', '--port', default=5556)

args = parser.parse_args()

import socket as socket2
myip = socket2.gethostbyname(socket2.gethostname())

socket.connect(args.connect_address)

# First just register to the server
command = '{}:{}'.format(myip, args.port)
socket.send(command)
players = socket.recv_string().split()

guesses = ['Ljubljana', 'Stockholm']

for player in players:
    player_socket = context.socket(zmq.DEALER)
    player_socket.connect('tcp://{}'.format(player))
    for guess in guesses:
        player_socket.send(guess)
        if socket.recv_string() == 'yes':
            print('Guessed: {}'.format(guess))
            break
    else:
        print("Couldn't guess the answer")
