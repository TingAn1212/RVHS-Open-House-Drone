#Import 
import threading 
import socket
#Global Variables
states = ""
local_address1 = ("",9000) 
local_address2 = ("0.0.0.0",8890) 
target_address = ('192.168.10.1', 8889)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(local_address1)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(local_address2)
#Async
def state():
    global states
    print("Listening")
    while True:
        try:
            data, source = server.recvfrom(1518)
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
#Init
client.sendto(str.encode("command"), target_address)
recvThread = threading.Thread(target=recv)
recvThread.start()

server.sendto(str.encode("command"), target_address)
stateThread = threading.Thread(target=state)
stateThread.start()
#Main
while (True):
    try:
        msg = input("")
        if not msg:
            break  
        if 'end' in msg:
            print ('...')
            client.close()
            server.close()
            break
        # Send data
        if msg == "state" :
            print(states)
        else:
            msg = msg.encode(encoding="utf-8") 
            sent = client.sendto(msg, target_address)
    except KeyboardInterrupt:
        print ('\n . . .\n')
        client.close() 
        server.close()
        break
