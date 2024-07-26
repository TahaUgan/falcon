import socket
from requests import get


def get_ip():
    
    hostname = socket.gethostname()
    hostname = str(hostname)
    IP = socket.gethostbyname(hostname)

    return IP
