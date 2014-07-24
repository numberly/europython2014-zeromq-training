#!/usr/bin/env python

import argparse
import time
import zmq

context = zmq.Context()

socket = context.socket(zmq.DEALER)

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--connect-address', default='tcp://127.0.0.1:5555')
parser.add_argument('-p', '--port', default='5556')

args = parser.parse_args()


def get_ip():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('www.google.com', 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

myip = get_ip()

socket.connect(args.connect_address)

command = 'LIST'
socket.send_string(command)
peers = socket.recv_multipart()[0].split(' ')

cities = """Berlin
London
Paris
Dublin
""".splitlines()

def get_cities():
    for c in cities:
        if c:
            yield c


seeker = context.socket(zmq.DEALER)
print peers
for peer in peers:
    seeker.connect('tcp://{}'.format(peer))
poller = zmq.Poller()
poller.register(seeker, zmq.POLLIN|zmq.POLLOUT)
gen = get_cities()
while True:
    print 'poll'
    socks = dict(poller.poll(timeout=1))
    print socks
    if seeker in socks and socks[seeker] == zmq.POLLOUT:
        try:
            city = next(gen)
        except StopIteration:
            break
        print city
        seeker.send(city)
    if seeker in socks and socks[seeker] == zmq.POLLIN:
        response = seeker.recv()
        if response == 'CORRECT':
            print 'Won', city
    time.sleep(.01)
