#!/usr/bin/env python
import argparse
import zmq

context = zmq.Context()

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--connect-address', default='tcp://127.0.0.1:5555')

args = parser.parse_args()

def list_ips(broker_ip):
    socket = context.socket(zmq.DEALER)

    socket.connect(broker_ip)

    msg = "LIST"
    socket.send(msg)
    print "Waiting for response..."
    response = socket.recv()
    ips = response.split(" ")
    return ips

def ask_hider(ip):
    req_socket = context.socket(zmq.REQ)
    req_socket.connect("tcp://" + ip)
    req_socket.send(guess)
    response = req_socket.recv()
    return response=="CORRECT"
        
guess = "WARSAW"

ips = list_ips(args.connect_address)

for ip in ips:
    print "Asking {}".format(ip)
    if ask_hider(ip):
        print "The answer is {}".format(guess)
        break



