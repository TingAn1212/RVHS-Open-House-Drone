import socket
target = ("192.168.10.1", 8889)
bufferSize = 1024
server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

def command(cmd):
    server.sendto(str.encode(cmd),target)
    message,address = server.recvfrom(bufferSize)
    return message.decode()