#!/usr/bin/env python
#coding=utf-8

import numpy as np
import matplotlib.pyplot as plt

def get_local_ip():
    """
    Retrieve the clients local ip address and return it as a string

    :returns IpAddress as String
    """
    import socket
    return socket.gethostbyname(socket.gethostname())

