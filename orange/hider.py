#!/usr/bin/env python
import argparse
import zmq
from zmq.eventloop import ioloop, zmqstream
import json


io_loop = ioloop.IOLoop()
context = zmq.Context()
socket = context.socket(zmq.ROUTER)

stream = zmqstream.ZMQStream(socket, io_loop=io_loop)

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--bind-address', default='tcp://0.0.0.0:7777')
parser.add_argument('-c', '--city', default='Berlin')

args = parser.parse_args()

def guess(stream, message):
    addr, text = message
    print text
    stream.send_multipart((addr, 'CORRECT' if text == args.city else 'INCORRECT'))

stream.on_recv_stream(guess)

socket.bind(args.bind_address)
io_loop.start()
