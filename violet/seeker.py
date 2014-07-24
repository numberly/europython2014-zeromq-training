
#!/usr/bin/env python
import argparse
import zmq
import socket

PORT = 54321


def get_local_ip():
    """
    Retrieve the clients local ip address and return it as a string

    :returns IpAddress as String
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((args.connect_address, 0))
    ip = s.getsockname()[0]
    s.close()
    return ip


context = zmq.Context()

mysocket = context.socket(zmq.DEALER)

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--connect-address', default='tcp://%s:%s' % ('172.16.16.188', 5556))
parser.add_argument('-l', '--local-address', default=None)

args = parser.parse_args()

mysocket.connect(args.connect_address)
if args.local_address is None:
  ip = get_local_ip()
else:
  ip = args.local_address


def get_hider_ips(ip, port):
    mysocket.send("%s:%s" % (ip, port))
    ips =  set(mysocket.recv().split(' '))
    print ips
    return ips


def guess_hider(sock, guess):
    sock.send(guess.lower())
    ans = sock.recv()
    return ans == 'CORRECT'


def is_valid_host(ip_port):
    if '127.0.0.1' in ip_port:
        return False
    if ':' not in ip_port:
        return False
    return True


if __name__ == '__main__':
    guesses = ['london', 'tel-aviv', 'berlin', 'sydney']
    for ip_port in get_hider_ips(ip, PORT):
        try:
            if not is_valid_host(ip_port):
                raise Exception('no valid ip %s' % ip_port)
            context = zmq.Context()
            hidersock = context.socket(zmq.DEALER)
            hidersock.connect('tcp://%s' % (ip_port))
        except Exception as e:
            print 'failed with %s %s' % (ip_port, e)
            continue
        print 'guessing on %s' % ip_port
        for guess in guesses:
            if guess_hider(hidersock, guess):
                print 'FOUND: %s on %s' % (guess, ip_port)
            else:
                print '.',

