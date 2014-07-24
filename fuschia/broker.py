#!/usr/bin/env python
import zmq
from optparse import OptionParser
from zmq.eventloop import ioloop, zmqstream


class ZMQBroker(object):

    def __init__(self):
        self.io_loop = ioloop.IOLoop()
        self.context = zmq.Context()
        self.clients = set()

    def connect(self, bind_address):
        self.socket = self.context.socket(zmq.ROUTER)
        self.stream = zmqstream.ZMQStream(
            self.socket,
            io_loop=self.io_loop
        )
        self.socket.bind(bind_address)

    def start(self):
        self.stream.on_recv_stream(self.response)
        self.io_loop.start()

    def response(self, stream, msg):
        addr, txt = msg
        self.clients.add(txt)
        stream.send_multipart((addr, ' '.join(self.clients)))


if __name__ == '__main__':
    parser = OptionParser()

    parser.add_option(
        "-b",
        "--bind",
        dest="bind",
        default='tcp://127.0.0.1:5555'
    )
    (options, args) = parser.parse_args()

    server = ZMQBroker()
    server.connect(options.bind)
    server.start()
