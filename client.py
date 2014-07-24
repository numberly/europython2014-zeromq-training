#!/usr/bin/env python
import zmq
from optparse import OptionParser


class ZMQClient(object):
    def __init__(self):
        self.context = zmq.Context()

    def connect(self, addr):
        self.addr = addr
        self.socket = self.context.socket(zmq.DEALER)
        self.socket.connect(self.addr)

    def send(self, msg):
        self.socket.send_multipart([str(i)])
        return self.socket.recv()

if __name__ == '__main__':
    parser = OptionParser()

    parser.add_option(
        "-c",
        "--connect-address",
        dest="address",
        default='tcp://127.0.0.1:5555'
    )
    (options, args) = parser.parse_args()
    client = ZMQClient()
    client.connect(options.address)

    for i in range(10):
        msg = "Hi server this is my message {}".format(i)
        print client.send(msg)
