from socket import *
import sys

def main(argv):
    if len(argv) != 1:
        print("Error: please provide req_code param")
    
    req_code = argv[0]

    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(("",0))
    n_port = serverSocket.getsockname()[1]
    serverSocket.listen(1)

    msg_socket = socket(AF_INET, SOCK_DGRAM)
    connected = False

    print(f"SERVER_PORT={n_port}")
    while True:

        connectionSocket, addr = serverSocket.accept()
        msg = connectionSocket.recv(1024).decode()

        print("Received code " ,msg)
        if msg == req_code:
            msg_socket.bind(("",0))
            r_port = str(msg_socket.getsockname()[1])
            print("Sending port")
            connectionSocket.send(r_port.encode())
            connectionSocket.close()
            print(f"Listening on {r_port}")
            connected = True
        else:
            print("Wrong code, closing socket")
            connectionSocket.close()
        # UDP stuff
        if connected:
            print("Listening for new messages")
            message, clientAddress = msg_socket.recvfrom(2048)
            print("Message received", message)
            modifiedMessage = message.decode()[::-1]
            msg_socket.sendto(modifiedMessage.encode(),clientAddress)
            msg_socket = socket(AF_INET, SOCK_DGRAM)
            print("Returning to watching for connections")
            connected = False

if __name__ == "__main__":
    main(sys.argv[1:])