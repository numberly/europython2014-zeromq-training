#!/usr/bin/env python

import argparse
import zmq
from utils import get_local_ip

context = zmq.Context()

socket = context.socket(zmq.DEALER)

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--connect-address', default='tcp://172.16.16.188:5556')
parser.add_argument('-p', '--port', default=5555)

args = parser.parse_args()
myip = get_local_ip()

socket.connect(args.connect_address)

# First just register to the server
command = 'REGISTER {}:{}'.format(myip, args.port)
socket.send(command)
players = socket.recv_string().split()
#players = ['172.16.17.133:7777']

guesses = ['Ljubljana', 'Stockholm', 'Berlin']

print(players)
for player in players:
    player_socket = context.socket(zmq.DEALER)
    player_socket.connect('tcp://{}'.format(player))
    for guess in guesses:
        player_socket.send(guess)
        if player_socket.recv_string() == 'CORRECT':
            print('Guessed: {}'.format(guess))
            break
    else:
        print("Couldn't guess the answer")
