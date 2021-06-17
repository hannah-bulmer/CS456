from socket import *
import sys

def main(argv):
    # make sure correct command line args received
    if (len(argv) < 4):
        print("Missing command line arguments.")
        print("usage: ./client.sh <server_address> <n_port> <req_code> <msg>")
        exit(0)
    elif (len(argv) > 4):
        print("Too many command line arguments")
        print("usage: ./client.sh <server_address> <n_port> <req_code> <msg>")
        exit(0)

    server_addr = argv[0]
    n_port = int(argv[1])
    req_code = argv[2]
    msg = argv[3]

    # client creates TCP connections with <n_port>
    # client sends their request code
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((server_addr,n_port))
    clientSocket.send(req_code.encode())
    
    # client receives back the r_port
    r_port = clientSocket.recv(1024).decode()
    clientSocket.close()

    # if they sent the wrong req code, nothing will be sent back so r_port will be ""
    # client exits gracefully
    if (r_port is None or r_port == ""):
        print("Error: wrong req code sent")
        exit(0)

    print("From Server: ", r_port)

    # Client opens UDP port to send their message to the listening server
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.sendto(msg.encode(),(server_addr, int(r_port)))

    # client receives back modified message, prints, and closes
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print(modifiedMessage.decode())
    clientSocket.close()

if __name__ == "__main__":
    main(sys.argv[1:])