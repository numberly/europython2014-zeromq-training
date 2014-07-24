import socket


def get_local_ip(destination):
    """
    Retrieve the clients local ip address and return it as a string

    :returns IpAddress as String
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((destination, 5556))
    ip = s.getsockname()[0]
    s.close()
    return ip
