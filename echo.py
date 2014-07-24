#!/usr/bin/env python
import zmq
from zmq.eventloop import ioloop, zmqstream


io_loop = ioloop.IOLoop()

context = zmq.Context()

socket = context.socket(zmq.ROUTER)


stream = zmqstream.ZMQStream(socket, io_loop=io_loop)


def echo(stream, message):
    stream.send_multipart(message)

stream.on_recv_stream(echo)

socket.bind('tcp://0.0.0.0:5555')
io_loop.start()
