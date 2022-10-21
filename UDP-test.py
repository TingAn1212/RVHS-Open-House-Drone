import socket
# Setting
local_address = ("127.0.0.1",20001)
bufferSize  = 1024
# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Bind to address and ip
UDPServerSocket.bind(local_address)
print("UDP server up and listening")
# Listen for incoming datagrams
while(True):
    message,address = UDPServerSocket.recvfrom(bufferSize)
    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)
    print(clientMsg)
    print(clientIP)
    # Sending a reply to client
    UDPServerSocket.sendto(str.encode("Received: " + message.decode()), address)