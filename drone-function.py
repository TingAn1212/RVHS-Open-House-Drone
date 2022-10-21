import socket
from time import sleep
from multiprocessing import Process
#Address setting
target = ("192.168.10.1", 8889)
self_address = ("0.0.0.0", 8890)
bufferSize = 1024
#client and global state
client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
stating = False
state = ""

def get_state(): # A async function to constantly update the state
    global stating
    global state
    stating = True
    while (stating):
        sleep(10)
        message,address = server.recvfrom(bufferSize)
        state = message.decode()

def command(cmd): # Send command to drone
    client.sendto(str.encode(cmd),target)
    message,address = client.recvfrom(bufferSize)
    return message.decode()


if __name__ == '__main__':
    # Init the drone
    command("Command")
    # Server object for state
    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(self_address)
    # Start listening for state
    listen_state = Process(target=get_state, args=())
    listen_state.start()

    #Insert more code here



    # listen_state.kill()
