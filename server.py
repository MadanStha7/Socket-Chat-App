from socket import *
import threading
import sys
from playsound import playsound

FLAG = False


def recv_from_client(conn):
    global FLAG
    try:
        while True:
            if FLAG == True:
                break
            message = conn.recv(1024).decode()

            if message == 'q':
                conn.send('q'.encode())
                print('CLosing Connection')
                conn.close()
                FLAG == True
                break
            print('Client: ' + message)
            playsound('alert.wav')
    except:
        conn.close


def send_to_client(conn):
    global FLAG
    try:
        while True:
            if FLAG == True:
                break
            send_msg = input('')

            if send_msg == 'q':
                conn.send('q'.encode())
                print('Closing connection')
                conn.close()
                FLAG = True
                break
            conn.send(send_msg.encode())
    except:
        conn.close()


def main():
    threads = []
    global FLAG

    HOST = '192.168.1.97'
    serverPort = 6789
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((HOST, serverPort))
    serverSocket.listen(1)

    print('THe chat server is ready to connect to a chat client')

    connectionSocket, addr = serverSocket.accept()
    print('Server is connected with chat clent \n')
    t_rcv = threading.Thread(target=recv_from_client, args=(connectionSocket,))
    t_send = threading.Thread(target=send_to_client, args=(connectionSocket,))

    threads.append(t_rcv)
    threads.append(t_send)
    t_rcv.start()
    t_send.start()

    t_rcv.join()
    t_send.join()

    print('EXITING')
    serverSocket.close()
    sys.exit()


if __name__ == '__main__':
    main()
