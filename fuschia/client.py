import zmq
from utils import get_local_ip
from optparse import OptionParser


class ZMQClient(object):
    def __init__(self):
        self.context = zmq.Context()

    def connect(self, addr):
        self.addr = addr
        self.socket = self.context.socket(zmq.DEALER)
        self.socket.connect(self.addr)

    def send(self, msg):
        self.socket.send_multipart([msg])
        return self.socket.recv()

if __name__ == '__main__':
    parser = OptionParser()

    parser.add_option(
        "-a",
        "--address",
        dest="address",
        default='tcp://127.0.0.1:5555'
    )
    (options, args) = parser.parse_args()
    client = ZMQClient()
    client.connect(options.address)

    msg = '{0}:{1}'.format(
        get_local_ip(),
        options.address.split(':')[-1]
    )
    print client.send(msg)
