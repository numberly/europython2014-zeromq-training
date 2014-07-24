#!/usr/bin/env python
import argparse
import zmq
from zmq.eventloop import ioloop, zmqstream
import json


io_loop = ioloop.IOLoop()

context = zmq.Context()

socket = context.socket(zmq.ROUTER)


stream = zmqstream.ZMQStream(socket, io_loop=io_loop)

CITY = None


def guess(stream, message):
    print message
    city = message[1]
    reply = "YES" if city == CITY else "NO"
    stream.send_multipart([message[0], reply])

stream.on_recv_stream(guess)

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--bind-address', default='tcp://0.0.0.0:5555')
parser.add_argument('-c', '--city', default='Berlin')

args = parser.parse_args()

CITY = args.city
socket.bind(args.bind_address)
io_loop.start()
