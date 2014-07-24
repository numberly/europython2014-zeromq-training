#!/usr/bin/env python2
import argparse
import zmq
import json
from zmq.eventloop import ioloop, zmqstream


io_loop = ioloop.IOLoop()

context = zmq.Context()

socket = context.socket(zmq.ROUTER)


stream = zmqstream.ZMQStream(socket, io_loop=io_loop)


def hider(secret):
    def reply(stream, message):
        print "recv:", message
        ans = "INCORRECT"
        if message[1] == secret:
            ans = "CORRECT"
        stream.send([message[0], ans])
        print "sent:", ans
    return reply

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--bind-address', default='tcp://127.0.0.1:5555')
parser.add_argument('-s', '--secret', default=None)

args = parser.parse_args()

if args.secret is None:
    raise Exception("Need to define secret")

socket.bind(args.bind_address)
stream.on_recv_stream(hider(args.secret))
io_loop.start()
