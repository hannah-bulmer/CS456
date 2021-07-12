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

    # setup UDP socket
    recv_socket = socket(AF_INET, SOCK_DGRAM)
    recv_socket.bind(("", args.recvPort))

    reset_files()
    
    print("Ready to receive data from sender")
    while True:
        packet, addr = recv_socket.recvfrom(2048)
        typ, seqnum, length, data = Packet(packet).decode()

        log(seqnum)
        
        if seqnum == cur_seqnum:    # handle valid packet
            if typ == 2:    # handle EOT
                print("EOT received. File transfer complete, closing connection.")
                send_eot_packet(recv_socket, cur_seqnum, args.host, args.emulatorPort)
                recv_socket.close()
                break

            else:   # otherwise its a data packet, write to file
                with open(args.file, "a") as file:
                    file.write(data)
                    cur_seqnum = (cur_seqnum + 1) % 32

                    # check buffer for next packets
                    while cur_seqnum in buffer:
                        file.write(buffer[cur_seqnum])
                        buffer.pop(cur_seqnum)
                        cur_seqnum = (cur_seqnum + 1) % 32

                # ack the good packet    
                send_ack_packet(recv_socket, cur_seqnum, args.host, args.emulatorPort)

        else:   # handle packets that are out of order
            # check if packet is within the next 10, if so add to buffer
            if seqnum > cur_seqnum and seqnum <= (cur_seqnum - 10) % 32:
                buffer[seqnum] = data
            if seqnum - 1 in buffer:    # clear old stuff out of buffer
                buffer.pop(seqnum-1)
            assert(len(buffer) <= 10)

            # ack expected packet
            send_ack_packet(recv_socket, cur_seqnum, args.host,args.emulatorPort)


def send_ack_packet(recv_socket, cur_seqnum, host,ePort):
    ack = Packet(0, (cur_seqnum-1)%32, 0, "")
    recv_socket.sendto(ack.encode(), (host, ePort))


def send_eot_packet(recv_socket, cur_seqnum, host,ePort):
    eot = Packet(2, cur_seqnum, 0, "")
    recv_socket.sendto(eot.encode(), (host, ePort))


def log(seqnum):
    with open("arrival.log", "a") as file:
        file.write(f"{seqnum}\n")


def reset_files():
    """Empties output and log files before receiver starts"""

    raw = open(args.file, "w")
    raw.close()
    raw = open("arrival.log", "w")
    raw.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="hostname for the network emulator", type=str)
    parser.add_argument("emulatorPort", help="UDP port number used by the emulator to receive ACKs from the receiver", type=int)
    parser.add_argument("recvPort", help="port number for receiver to receive data from the emulator", type=int)
    parser.add_argument("file", help="filename to write to", type=str)

    args = parser.parse_args()
    main(args)