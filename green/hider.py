#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import argparse
import zmq
from zmq.eventloop import ioloop, zmqstream

io_loop = ioloop.IOLoop()

context = zmq.Context()

socket = context.socket(zmq.ROUTER)

stream = zmqstream.ZMQStream(socket, io_loop=io_loop)


def check_guess(stream, message):
    addr, guess = message
    response = ('CORRECT' if guess in CITIES else 'INCORRECT')
    stream.send_multipart((addr, response))


stream.on_recv_stream(check_guess)

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--bind-address', default='tcp://0.0.0.0:5556')
parser.add_argument('-c', '--cities', default='Berlin')

args = parser.parse_args()

CITIES = set(args.cities.split(','))

socket.bind(args.bind_address)
io_loop.start()
