#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import argparse
import logging
import zmq
import socket

context = zmq.Context()

sock = context.socket(zmq.DEALER)

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--connect-address', default='tcp://127.0.0.1:5555')
parser.add_argument('city')

args = parser.parse_args()

sock.connect(args.connect_address)

sock.send('LIST')
response = sock.recv_string()
peers = response.split()

city = args.city

print 'Searching for {} on {} peers..'.format(city, len(peers))
print peers

logging.basicConfig(level=logging.DEBUG)

for peer in peers:
    print 'Trying', peer
    try:
        peer_socket = context.socket(zmq.DEALER)
        peer_socket.setsockopt(zmq.RCVTIMEO, 1000)
        peer_socket.connect('tcp://{}'.format(peer))
        peer_socket.send(city)
        result = peer_socket.recv_string()
        if result == 'CORRECT':
            print 'Found', city
        elif result == 'INCORRECT':
            print 'Incorrect guess'
        else:
            print 'invalid response:', result
    except Exception, e:
        logging.exception('Failed to connect to %s', peer)

