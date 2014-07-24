#!/usr/bin/env python2
import argparse
import zmq
import json
from zmq.eventloop import ioloop, zmqstream


known = set()

io_loop = ioloop.IOLoop()

context = zmq.Context()

socket = context.socket(zmq.ROUTER)


stream = zmqstream.ZMQStream(socket, io_loop=io_loop)


def reply(stream, message):
    print message
    msg = message[1].split()
    if msg[0] == "HELLO":
      known.add((msg[1], msg[2]))
    res = [a + ":" + b for a,b in known]
    print res
    stream.send_multipart(" ".join(res))

stream.on_recv_stream(reply)

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--bind-address', default='tcp://127.0.0.1:5555')

args = parser.parse_args()

socket.bind(args.bind_address)
io_loop.start()
