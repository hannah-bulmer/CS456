from socket import *
import sys
import argparse
from datetime import datetime

from packet import Packet

def main(args):
    N = 1
    num_unacked = 0
    seqnum = 0
    packets = {}
    timer = None
    timestamp = 0
    data = None

    reset_files()

    log_n(timestamp,N)

    # setup UDP socket
    send_socket = socket(AF_INET, SOCK_DGRAM)
    send_socket.bind(("", args.recvPort))
    send_socket.settimeout(0)
    
    with open(args.file, 'rb') as file:
        while True:
            if data == None:    # read some new data to send if last chunk has been sent
                data = file.read(500)
                length = len(data)

            if data == b'':     # if EOF, send EOT
                if num_unacked == 0: # only send if we've received all the ACKS tho! Otherwise we just have to wait and keep looping
                    print("File transfer complete. Sending EOT and closing connection")
                    
                    timestamp += 1
                    log_seqnum(timestamp, seqnum)

                    send_eot_packet(send_socket, seqnum,args.host,args.emulatorPort)
                    break

            elif num_unacked < N and data != None: # if we have space left in the window, send the packet

                packet = Packet(1, seqnum, length, data.decode())
                send_socket.sendto(packet.encode(), (args.host,args.emulatorPort))

                timestamp += 1
                log_seqnum(timestamp, seqnum)

                # packet sent, we can move on to sending next piece of data. Store small num of packets in case we need to retransmit
                packets[seqnum] = packet
                data = None

                seqnum = (seqnum + 1) % 32
                num_unacked += 1
                if timer == None:   # set timer if not set yet
                    timer = datetime.now()
            
            # if timeout has occurred
            if timer and (datetime.now() - timer).microseconds > args.timeout * 1000:
                
                timestamp += 1
                N = 1   # reset N to 1
                log_n(timestamp,N)

                # retransmit problem packet
                problem_seq = (seqnum - num_unacked) % 32
                unacked_packet = packets[problem_seq]
                send_socket.sendto(unacked_packet.encode(), (args.host,args.emulatorPort))

                timer = datetime.now()  # and reset timer
            
            timestamp += 1
            ack = None

            # grab the ACK if one exists - but this is nonblocking, if there is no ACK to get, we just continue and try again on next loop. This way we can keep sending packets and watch for timeout without getting blocked here.

            try:    
                ack, addr = send_socket.recvfrom(2048)
            except BlockingIOError:
                pass
            if ack == None:
                continue
                
            typ, ack_seqnum, l, ack_data = Packet(ack).decode()
            # check incoming ack
            assert(typ == 0)
            log_ack(timestamp, ack_seqnum)

            # check if it's a new ACK
            if is_between(ack_seqnum, seqnum - num_unacked, seqnum):
                packets_acked = 1 + ack_seqnum - (seqnum - num_unacked) % 32 # count num packets we can consider ACKed now
                assert(packets_acked <= num_unacked)
                num_unacked -= packets_acked

                prev_n = N
                N = 10 if N == 10 else N + 1 # add 1 to N up to a max of 10
                if N != prev_n:
                    log_n(timestamp,N)

                if num_unacked > 0:
                    timer = datetime.now()
                else:
                    timer = None
    
    send_socket.settimeout(None)
    timestamp += 1
    # wait for EOT
    eot, addr = send_socket.recvfrom(2048)
    log_ack(timestamp, ack_seqnum)
    send_socket.close()


def log_n(time, N):
    with open("N.log", "a") as file:
        file.write(f"t={time} {N}\n")


def log_seqnum(time, seqnum):
    with open("seqnum.log", "a") as file:
        file.write(f"t={time} {seqnum}\n")


def log_ack(time, seqnum):
    with open("ack.log", "a") as file:
        file.write(f"t={time} {seqnum}\n")


def send_eot_packet(send_socket, seqnum,host,ePort):
    eot = Packet(2, seqnum, 0, "")
    send_socket.sendto(eot.encode(), (host, ePort))


def reset_files():
    """Empties output and log files before sender starts"""

    raw = open("N.log", "w")
    raw.close()
    raw = open("ack.log", "w")
    raw.close()
    raw = open("seqnum.log", "w")
    raw.close()


def is_between(a,b,c):
    """returns true if a is within (b,c] modulo 32, else false"""

    a = a % 32
    b = b % 32
    c = c % 32
    if a < b:
        if a <= c and c < b: return True
        return False
    else:
        if b < c and c <= a: return False
        return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="host address of the network emulator", type=str)
    parser.add_argument("emulatorPort", help="UDP port number used by the emulator to receive data from the sender", type=int)
    parser.add_argument("recvPort", help="port number used by the sender to receive ACKs from the emulator", type=int)
    parser.add_argument("timeout", help="timeout interval in units of millisecond", type=int)
    parser.add_argument("file", help="filename to write to", type=str)

    args = parser.parse_args()
    main(args)