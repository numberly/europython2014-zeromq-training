import zmq

context = zmq.Context()

socket = context.socket(zmq.DEALER)

socket.connect('tcp://172.16.16.228:5555')
while True:
    socket.send_multipart([str(1)])
