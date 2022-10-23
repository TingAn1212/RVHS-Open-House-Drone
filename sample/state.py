import socket
from time import sleep
INTERVAL = 0.2

if __name__ == "__main__":

    local_ip = ''
    local_port = 8890
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket for sending cmd

    l = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    l.bind((local_ip, local_port))
    tello_ip = '192.168.10.1'
    tello_port = 8889
    tello_adderss = (tello_ip, tello_port)

    s.sendto('command'.encode('utf-8'), tello_adderss)
    l.sendto('command'.encode('utf-8'), tello_adderss)

    try:
        index = 0
        while True:
            index += 1
            response, ip = l.recvfrom(1024)
            if response == 'ok':
                continue
            out = response
            print(out)
            sleep(INTERVAL)
    except KeyboardInterrupt:
        socket.close()