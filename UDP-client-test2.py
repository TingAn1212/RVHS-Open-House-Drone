import socket
target = ("127.0.0.1", 20001)
bufferSize = 1024
# Create a UDP socket at client side
server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Send to server using created UDP socket
while (True):
    print("Please send a message: ")
    server.sendto(str.encode(input()),target)
    message,address = server.recvfrom(bufferSize)
    print(message.decode())