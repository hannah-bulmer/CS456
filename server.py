from socket import *
import sys
import random

def main(argv):
    if len(argv) != 1:
        print("Error: please provide req_code param")
    
    req_code = argv[0]
    n_port = 52500

    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(("",n_port))
    serverSocket.listen(1)

    msg_socket = socket(AF_INET, SOCK_DGRAM)

    print(f"SERVER_PORT={n_port}")
    while True:

        connectionSocket, addr = serverSocket.accept()
        msg = connectionSocket.recv(1024).decode()

        if msg == req_code:
            r_port = str(random.randint(2048, 25000))
            connectionSocket.send(r_port.encode())
            connectionSocket.close()
            print(f"Listening on {r_port}")
            msg_socket.bind(("",int(r_port)))

        # UDP stuff
        message, clientAddress = msg_socket.recvfrom(2048)
        modifiedMessage = message.decode()[::-1]
        msg_socket.sendto(modifiedMessage.encode(),clientAddress)
        msg_socket = socket(AF_INET, SOCK_DGRAM)

if __name__ == "__main__":
    main(sys.argv[1:])