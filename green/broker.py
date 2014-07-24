#!/usr/bin/env python
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
    CLIENTS.add(message[1])
    stream.send_multipart((addr, ' '.join(CLIENTS)))

stream.on_recv_stream(register)

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--bind-address', default='tcp://0.0.0.0:5555')

args = parser.parse_args()

socket.bind(args.bind_address)
io_loop.start()
