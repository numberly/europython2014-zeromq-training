#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import argparse
import zmq
from zmq.eventloop import ioloop, zmqstream

io_loop = ioloop.IOLoop()

context = zmq.Context()

socket = context.socket(zmq.ROUTER)

stream = zmqstream.ZMQStream(socket, io_loop=io_loop)

CLIENTS = set()


def register(stream, message):
    addr, text = message
    print text
    CLIENTS.add(text.lstrip("REGISTER").strip())
    stream.send_multipart((addr, ' '.join(CLIENTS)))


stream.on_recv_stream(register)

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--bind-address', default='tcp://0.0.0.0:5555')

args = parser.parse_args()

socket.bind(args.bind_address)
io_loop.start()
