#!/usr/bin/env python
import sys
import argparse
import zmq
from zmq.eventloop import ioloop, zmqstream

io_loop = ioloop.IOLoop()

context = zmq.Context()

socket = context.socket(zmq.ROUTER)


stream = zmqstream.ZMQStream(socket, io_loop=io_loop)

CLIENTS = set()


def hello(stream, message):
    command, separator, argument = message[1].partition(' ')
    if command == 'REGISTER':
      CLIENTS.add(argument)
    reply = [message[0]] + [" ".join(CLIENTS)]
    print reply
    stream.send_multipart(reply)

stream.on_recv_stream(hello)

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--bind-address', default='tcp://0.0.0.0:5555')

args = parser.parse_args()

socket.bind(args.bind_address)
io_loop.start()
