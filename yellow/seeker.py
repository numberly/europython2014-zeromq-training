#!/usr/bin/env python
import argparse
import zmq

context = zmq.Context()

socket = context.socket(zmq.DEALER)

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--connect-address', default='tcp://127.0.0.1:5555')

args = parser.parse_args()

socket.connect(args.connect_address)

msg = "LIST"
socket.send(msg)
print "Waiting for response..."
response = socket.recv()
ips = response.split(" ")

def ask_hider(ip):
    req_socket = context.socket(zmq.REQ)
    req_socket.connect("tcp://" + ip)
    req_socket.send(guess)
    response = req_socket.recv()
    return response=="CORRECT"
        
guess = "WARSAW"

for ip in ips:
    print "Asking {}".format(ip)
    if ask_hider(ip):
        print "The answer is {}".format(guess)
        break



