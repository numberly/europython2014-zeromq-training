#!/usr/bin/env python

import argparse
import functools
import time
import threading

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


def worker(peer):
    seeker = context.socket(zmq.DEALER)
    seeker.connect('tcp://{}'.format(peer))
    poller = zmq.Poller()
    poller.register(seeker, zmq.POLLIN|zmq.POLLOUT)
    gen = get_cities()
    while True:
        socks = dict(poller.poll(timeout=5000))
        if seeker in socks and socks[seeker] == zmq.POLLOUT:
            try:
                city = next(gen)
            except StopIteration:
                break
            seeker.send(city)
        elif seeker in socks and socks[seeker] == zmq.POLLIN:
            response = seeker.recv()
            if response == 'CORRECT':
                print 'Won', city
                break
        elif seeker in socks and socks[seeker] == zmq.POLLIN|zmq.POLLOUT:
            response = seeker.recv()
            if response == 'CORRECT':
                print 'Won', city
                break
            try:
                city = next(gen)
            except StopIteration:
                break
            seeker.send(city)
        else:
            print 'timeout'
            break
        time.sleep(.1)


for peer in peers:
    thread = threading.Thread(target=functools.partial(worker, peer))
    thread.daemon = True
    thread.start()
    thread.join()
