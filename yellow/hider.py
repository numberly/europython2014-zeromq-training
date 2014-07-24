#!/usr/bin/env python
import argparse
import zmq
from zmq.eventloop import ioloop, zmqstream
import json
from utils import get_local_ip

HIDER_IP = '0.0.0.0'
HIDER_PORT = '5557'

def register_ip(broker_ip):
    socket = context.socket(zmq.DEALER)

    socket.connect(broker_ip)
    ip = get_local_ip()

    msg = "REGISTER {}:{}".format(ip, HIDER_PORT)
    socket.send(msg)
    response = socket.recv()

io_loop = ioloop.IOLoop()

context = zmq.Context()

socket = context.socket(zmq.REP)

CITIES = {'Warsaw'.lower()}

stream = zmqstream.ZMQStream(socket, io_loop=io_loop)

def check_city_guess(stream, message):
    print "Got connection"
    city = message[0]
    reply = 'CORRECT' if city.lower() in CITIES else 'INCORRECT'

    stream.send(reply)

stream.on_recv_stream(check_city_guess)

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--bind-address', default='tcp://{}:{}'.format(HIDER_IP, HIDER_PORT))
parser.add_argument('--broker-address', default='tcp://127.0.0.1:5555')

args = parser.parse_args()

register_ip(args.broker_address)

socket.bind(args.bind_address)
io_loop.start()
