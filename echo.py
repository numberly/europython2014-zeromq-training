#!/usr/bin/env python2
import argparse
import zmq
from zmq.eventloop import ioloop, zmqstream


io_loop = ioloop.IOLoop()

context = zmq.Context()

socket = context.socket(zmq.ROUTER)


stream = zmqstream.ZMQStream(socket, io_loop=io_loop)


def echo(stream, message):
    stream.send_multipart(message)

stream.on_recv_stream(echo)

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--bind-address', default='tcp://0.0.0.0:5555')

args = parser.parse_args()

socket.bind(args.bind_address)
io_loop.start()
