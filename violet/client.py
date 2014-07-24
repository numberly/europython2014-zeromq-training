#!/usr/bin/env python2
import argparse
import zmq


PORT = 54321
DEFUALT_SERVER = '172.16.16.228'


def get_local_ip():
    """
    Retrieve the clients local ip address and return it as a string

    :returns IpAddress as String
    """
    import socket
    ip = socket.gethostbyname(socket.gethostname())
    return ip


def hello(connect_address):
    context = zmq.Context()
    zmsocket = context.socket(zmq.DEALER)
    zmsocket.connect()
    msg = "{} {}".format(get_local_ip(), PORT)
    zmsocket.send(msg)
    known_clients = set(zmsocket.recv().split(" "))
    return known_clients


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--connect-address', default='tcp://%s:5555' % DEFUALT_SERVER)
    args = parser.parse_args()
    print hello(args.connect_address)


if __name__ == '__main__':
    main()
