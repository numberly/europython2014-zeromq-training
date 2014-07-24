import zmq
from zmq.eventloop import ioloop, zmqstream


io_loop = ioloop.IOLoop()
context = zmq.Context()
socket = context.socket(zmq.ROUTER)
stream = zmqstream.ZMQStream(socket, io_loop=io_loop)

hosts = set()

def register(stream, message):
    hosts.update(message)
    stream.send_multipart(list(message))

stream.on_recv_stream(register)

socket.bind('tcp://0.0.0.0:5555')
io_loop.start()
