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
    id, tcp = message
    CLIENTS.add(tcp)
    print CLIENTS
    reply = list(CLIENTS)
    stream.send_multipart([id, json.dumps(reply)])

stream.on_recv_stream(hello)

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--bind-address', default='tcp://0.0.0.0:5555')

args = parser.parse_args()

socket.bind(args.bind_address)
io_loop.start()
