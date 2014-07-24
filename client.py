#!/usr/bin/env python
import zmq
import sys
import getopt

context = zmq.Context()

socket = context.socket(zmq.DEALER)

SHORT_OPTIONS = 's:'

LONG_OPTIONS = [ 'server=' ]

opts, args = getopt.getopt(sys.argv[1:], SHORT_OPTIONS, LONG_OPTIONS)
options = { 'server' : 'tcp://127.0.0.1:5555' }

for o, a in opts:
    if o in ('-s', '--server',):
        options['server']  = a
    else:
        print 'ERR: option %s not supported' % (o)

server = options['server']
print 'Connecting to server %s ...' % (server)
socket.connect(server)

for i in range(10):
    socket.send(str(i))
    print socket.recv()
