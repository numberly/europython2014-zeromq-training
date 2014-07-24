#!/usr/bin/env python
import argparse
import zmq
from zmq.eventloop import ioloop, zmqstream
import json


io_loop = ioloop.IOLoop()

context = zmq.Context()

socket = context.socket(zmq.ROUTER)


stream = zmqstream.ZMQStream(socket, io_loop=io_loop)

CLIENTS = set()


def hello(stream, message):
    print message
    parts = message[1].split()
    if parts[0] == "REGISTER":
        CLIENTS.add(parts[1])
    elif parts[0] == "LIST":
        pass
    reply = [message[0], " ".join(list(CLIENTS))]
    stream.send_multipart(reply)

stream.on_recv_stream(hello)

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--bind-address', default='tcp://0.0.0.0:5555')

args = parser.parse_args()

socket.bind(args.bind_address)
io_loop.start()
