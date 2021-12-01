import socket
import struct



def ip2long(ip):
    """
    Convert an ip string to long
    """
    packed_ip = socket.inet_aton(ip)
    return struct.unpack("!L", packed_ip)[0]


def long2ip(ip):
    """
    Convert long to ip string
    """
    return socket.inet_ntoa(struct.pack('!L', ip))
