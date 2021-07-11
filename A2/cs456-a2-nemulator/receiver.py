from socket import *
import sys
import argparse

from packet import Packet

# integer type; 0: ACK, 1: Data, 2: EOT
# integer seqnum; Modulo 32
# integer length; Length of the String variable ‘data’
# String data; String with Max Length 500

def main(args):
    # listen to network emulator
    cur_seqnum = 0
    buffer = {}

    recv_socket = socket(AF_INET, SOCK_DGRAM)
    recv_socket.bind(("", args.recvPort))

    raw = open(args.file, "w")
    raw.close()
    
    print("Ready to receive data from emulator")
    while True:
        packet, addr = recv_socket.recvfrom(2048)
        typ, seqnum, length, data = Packet(packet).decode()

        print(seqnum, cur_seqnum)
        log(seqnum)
        
        if seqnum == cur_seqnum:
            # handle valid packet
            if typ == 2:
                print("Received eot")
                print(f"Sending eot {cur_seqnum}")
                send_eot_packet(recv_socket, cur_seqnum, args.host, args.emulatorPort)
                recv_socket.close()
                break
            else:
                # write to file
                with open(args.file, "a") as file:
                    file.write(data)
                    print("Writing to file")
                    cur_seqnum = (cur_seqnum + 1) % 32
                    # check buffer for next packets
                    print("Checking buffer")
                    while cur_seqnum in buffer:
                        file.write(buffer[cur_seqnum])
                        buffer.pop(cur_seqnum)
                        cur_seqnum = (cur_seqnum + 1) % 32
                send_ack_packet(recv_socket, cur_seqnum, args.host, args.emulatorPort)
        else:
            # check this: if the packet is within the next 10
            if 32 - (cur_seqnum + 10) > seqnum:
                buffer[seqnum] = data
            send_ack_packet(recv_socket, cur_seqnum, args.host,args.emulatorPort)


def send_ack_packet(recv_socket, cur_seqnum, host,ePort):
    print(f"Sending ACK for {cur_seqnum-1}")
    print(f"Now looking for {cur_seqnum}")
    ack = Packet(0, cur_seqnum-1, 0, "")
    recv_socket.sendto(ack.encode(), (host, ePort))


def send_eot_packet(recv_socket, cur_seqnum, host,ePort):
    eot = Packet(2, cur_seqnum, 0, "")
    recv_socket.sendto(eot.encode(), (host, ePort))


def log(seqnum):
    with open("arrival.log", "w") as file:
        file.write(f"{seqnum}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="hostname for the network emulator", type=str)
    parser.add_argument("emulatorPort", help="UDP port number used by the emulator to receive ACKs from the receiver", type=int)
    parser.add_argument("recvPort", help="port number for receiver to receive data from the emulator", type=int)
    parser.add_argument("file", help="filename to write to", type=str)

    args = parser.parse_args()
    main(args)