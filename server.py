from socket import *
import sys

def main(argv):
    # check for correct parameters
    if len(argv) != 1:
        print("Missing command line arguments")
        print("usage: ./server.sh <req_code>")
    
    req_code = argv[0]

    # initialize server socket, bind to an available port
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(("",0))
    n_port = serverSocket.getsockname()[1]
    serverSocket.listen(1)

    # create reusable UDP socket to use to transfer messages, don't bind port yet
    msg_socket = socket(AF_INET, SOCK_DGRAM)
    connected = False

    print(f"SERVER_PORT={n_port}")
    while True:
        
        # wait for new connection
        connectionSocket, addr = serverSocket.accept()
        msg = connectionSocket.recv(1024).decode()

        # check correct request code was sent
        if msg == req_code:
            # bind new port to the UDP socket, send port num back to client
            msg_socket.bind(("",0))
            r_port = str(msg_socket.getsockname()[1])
            # print("Sending port")
            connectionSocket.send(r_port.encode())
            connectionSocket.close()
            print(f"Listening on {r_port}")
            connected = True
        else:
            # wrong request code, close socket and wait for new one
            connectionSocket.close()
        
        # if client had req code, we wait to receive a message
        if connected:
            message, clientAddress = msg_socket.recvfrom(2048)
            print("Message received", message)

            # reverse message and send back
            modifiedMessage = message.decode()[::-1]
            msg_socket.sendto(modifiedMessage.encode(),clientAddress)

            # re-initialze msg_socket so we can set it to a new port
            msg_socket = socket(AF_INET, SOCK_DGRAM)
            print("Returning to watching for connections")
            connected = False

if __name__ == "__main__":
    main(sys.argv[1:])