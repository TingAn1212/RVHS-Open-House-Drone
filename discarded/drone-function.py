import threading 
import socket
import sys
import time
# Create a UDP socket
states = ""
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

local_address1 = ("",9000) 
local_address2 = ("0.0.0.0",8890) 
target_address = ('192.168.10.1', 8889)
client.bind(local_address1)
def state(server):
    global states
    print("Listening")
    while True:
        try:
            data, source = server.recvfrom(1518)
            print(data)
            states = data
        except Exception:
            print ('\nExit . . .\n')
            break
def recv():
    count = 0
    while True: 
        try:
            data, server = client.recvfrom(1518)
            print(data)
        except Exception:
            print ('\nExit . . .\n')
            break
print ('\r\n\r\nTello Python3 Demo.\r\n')
print ('Tello: command takeoff land flip forward back left right \r\n       up down cw ccw speed speed?\r\n')
print ('end -- quit demo.\r\n')
#Thread create
recvThread = threading.Thread(target=recv)
recvThread.start()
servered = False
while True: 
    try:
        msg = input("")
        if not msg:
            break  
        if 'end' in msg:
            print ('...')
            client.close()
            break
        # Send data
        if msg == "state" :
            print(states)
        if msg == "open" and not servered:
            server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server.bind(local_address2)
            stateThread = threading.Thread(target=state, args=[server])
            stateThread.start()
            servered = True
        elif msg == "command":
            msg = msg.encode(encoding="utf-8") 
            sent = client.sendto(msg, target_address)
        else:
            msg = msg.encode(encoding="utf-8") 
            sent = client.sendto(msg, target_address)
                
    except KeyboardInterrupt:
        print ('\n . . .\n')
        client.close() 
        break