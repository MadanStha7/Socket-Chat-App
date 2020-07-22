import threading
import sys
from playsound import playsound
from socket import *

FLAG = False


def send_to_server(clsock):
    global FLAG
    while True:
        if FLAG == True:
            break
        send_msg = input('')
        clsock.sendall(send_msg.encode())


def recv_from_server(clsock):
    global FLAG
    while True:
        data = clsock.recv(1024).decode()
        if data == 'q':
            print('CLosing connection')
            FLAG = True
            break
        print('Server: ' + data)
        playsound('alert.wav')


def main():
    threads = []

    HOST = '192.168.1.97'
    PORT = 6789
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((HOST, PORT))

    print('client is connected with chat server \n')
    t_rcv = threading.Thread(target=send_to_server, args=(clientSocket,))
    t_send = threading.Thread(target=recv_from_server, args=(clientSocket,))

    threads.append(t_send)
    threads.append(t_rcv)

    t_send.start()
    t_rcv.start()

    t_send.join()
    t_rcv.join()

    print('EXITING')

    sys.exit()


if __name__ == '__main__':
    main()
