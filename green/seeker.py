#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import zmq

context = zmq.Context()

sock = context.socket(zmq.DEALER)

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--connect-address', default='tcp://127.0.0.1:5555')
parser.add_argument('city_list')

args = parser.parse_args()

sock.connect(args.connect_address)

sock.send('LIST')
response = sock.recv_string()
peers = response.split()

with open(args.city_list) as fd:
    cities = [line.strip() for line in fd]

print 'Searching for {} cities on {} peers..'.format(len(cities), len(peers))
print peers

logging.basicConfig(level=logging.DEBUG)

for peer in peers:
    print 'Trying', peer
    try:
        peer_socket = context.socket(zmq.DEALER)
        peer_socket.setsockopt(zmq.RCVTIMEO, 1000)
        peer_socket.connect('tcp://{}'.format(peer))
        for city in cities:
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

