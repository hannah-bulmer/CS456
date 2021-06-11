from socket import *
import sys

def main(argv):
    if (len(argv) < 4):
        print("Missing command line arguments.")
        print("Run program as ./client <server_address>, <n_port>, <req_code>, <msg>")
        exit(0)
    elif (len(argv) > 4):
        print("Too many command line arguments")
        exit(0)

    server_addr = argv[0]
    n_port = int(argv[1])
    req_code = argv[2]
    msg = argv[3]

    print(server_addr)
    print(n_port)
    print(req_code)
    print(msg)

    # 1 Client creates TCP connections with <n_port>

    # client sends request code to server
    # if correct request code, server will send back a random port number where it will be listening for the actual request
    # once this is received, client closes TCP connection with server

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((server_addr,n_port))
    clientSocket.send(req_code.encode())
    r_port = clientSocket.recv(1024).decode()
    print("From Server: ", r_port)
    clientSocket.close()

    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.sendto(msg.encode(),(server_addr, int(r_port)))
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print(modifiedMessage.decode())
    clientSocket.close()

if __name__ == "__main__":
    main(sys.argv[1:])