#!/usr/bin/env python
import argparse
import zmq
from zmq.eventloop import ioloop, zmqstream


io_loop = ioloop.IOLoop()

context = zmq.Context()

CITY = None


def get_ip():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('www.google.com', 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def guess(stream, message):
    print message
    city = message[1]
    reply = "CORRECT" if city.lower() == CITY.lower() else "INCORRECT"
    stream.send_multipart([message[0], reply])


parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', default='5557')
parser.add_argument('-C', '--connect-address', default='tcp://127.0.0.1:5555')
parser.add_argument('-c', '--city', default='Berlin')

args = parser.parse_args()

# First just register to the server
myip = get_ip()
sock = context.socket(zmq.DEALER)
sock.connect(args.connect_address)
command = 'REGISTER {}:{}'.format(myip, args.port)
sock.send_string(command)
print sock.recv_multipart()

# start server
CITY = args.city
sock = context.socket(zmq.ROUTER)
stream = zmqstream.ZMQStream(sock, io_loop=io_loop)
stream.on_recv_stream(guess)
sock.bind("tcp://%s:%s" % (myip, args.port))
io_loop.start()
