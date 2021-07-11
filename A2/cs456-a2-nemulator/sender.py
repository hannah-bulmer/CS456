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

    send_socket = socket(AF_INET, SOCK_DGRAM)
    send_socket.bind(("", args.recvPort))
    send_socket.settimeout(0)
    
    with open(args.file, 'rb') as file:
        while True:
            if data == None:
                # try sending packet
                data = file.read(500)
                length = len(data)
            if data == b'':
                print(f"Waiting for {num_unacked} acks still")
                if num_unacked == 0: # check this
                    print(f"Sending eot with seqnum {seqnum}")
                    timestamp += 1
                    log_seqnum(timestamp, seqnum)

                    send_eot_packet(send_socket, seqnum,args.host,args.emulatorPort)
                    break
            elif num_unacked < N and data != None:
                # send packet

                packet = Packet(1, seqnum, length, data.decode())
                print(f"Sending {data.decode()[0:30]}")
                send_socket.sendto(packet.encode(), (args.host,args.emulatorPort))

                timestamp += 1
                log_seqnum(timestamp, seqnum)

                # packet sent, we can move on to sending next piece of data
                packets[seqnum] = packet
                data = None

                seqnum = (seqnum + 1) % 32
                num_unacked += 1
                if timer == None:
                    timer = datetime.now()
            
            if timer and (datetime.now() - timer).microseconds > args.timeout * 1000:
                timestamp += 1
                N = 1
                log_n(timestamp,N)

                print("Timeout, resending packet")

                # retransmit problem packet
                problem_seq = (seqnum - num_unacked) % 32
                unacked_packet = packets[problem_seq]
                a,b,c, bad_data = unacked_packet.decode()
                print(f"Sending {bad_data[0:30]}")
                send_socket.sendto(unacked_packet.encode(), (args.host,args.emulatorPort))

                timer = datetime.now()
            
            timestamp += 1
            ack = None
            try:
                ack, addr = send_socket.recvfrom(2048)
            except BlockingIOError:
                pass
            if ack == None:
                continue
            typ, ack_seqnum, l, ack_data = Packet(ack).decode()
            # check incoming ack
            if (typ == 0):
                print(f"ACK received for {ack_seqnum}")
                print(f"Num unacked: {num_unacked}")
                print(f"Seqnum var: {seqnum}")
                print(f"Current seqnum: {(seqnum - num_unacked) % 32}")
                print(f"New ack? {is_between(ack_seqnum, seqnum - num_unacked, seqnum)}")
                log_ack(timestamp, ack_seqnum)

                # check if it's a new ACK
                if is_between(ack_seqnum, seqnum - num_unacked, seqnum):
                    packets_acked = 1 + ack_seqnum - (seqnum - num_unacked) % 32
                    print(packets_acked, num_unacked)
                    assert(packets_acked <= num_unacked)
                    num_unacked -= packets_acked

                    prev_n = N
                    N = 10 if N == 10 else N + 1
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
    print(f"t={time} N={N}")
    with open("N.log", "a") as file:
        file.write(f"t={time} {N}\n")


def log_seqnum(time, seqnum):
    # print(f"t={time} seqnum={seqnum}")
    with open("seqnum.log", "a") as file:
        file.write(f"t={time} {seqnum}\n")


def log_ack(time, seqnum):
    # print(f"t={time} ack={seqnum}")
    with open("ack.log", "a") as file:
        file.write(f"t={time} {seqnum}\n")


def send_eot_packet(send_socket, seqnum,host,ePort):
    eot = Packet(2, seqnum, 0, "")
    send_socket.sendto(eot.encode(), (host, ePort))


def reset_files():
    raw = open("N.log", "w")
    raw.close()
    raw = open("ack.log", "w")
    raw.close()
    raw = open("seqnum.log", "w")
    raw.close()


# if a is between b and c
def is_between(a,b,c):
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