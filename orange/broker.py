#!/usr/bin/env python
import argparse
import zmq
from zmq.eventloop import ioloop, zmqstream

io_loop = ioloop.IOLoop()
context = zmq.Context()
socket = context.socket(zmq.ROUTER)
stream = zmqstream.ZMQStream(socket, io_loop=io_loop)
CLIENTS = set()


def hello(stream, message):
    addr, command = message
    command = command.split(' ')
    if command[0] == 'REGISTER':
        CLIENTS.add(command[1])
        print "ClientIP added {}".format(clientip)
    reply = " ".join(list(CLIENTS))
    stream.send_multipart((addr, reply))

stream.on_recv_stream(hello)

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--bind-address', default='tcp://127.0.0.1:5555')
args = parser.parse_args()

socket.bind(args.bind_address)
io_loop.start()
