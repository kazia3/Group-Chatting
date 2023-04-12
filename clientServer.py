#!/usr/bin/env python3

########################################################################

import socket
import argparse
import sys
import time
import struct
import ipaddress
import csv
import pprint
########################################################################
pp = pprint.PrettyPrinter(indent=4)

SOCKET_TIMEOUT = 4

########################################################################
# recv_bytes frontend to recv
########################################################################

# Call recv to read bytecount_target bytes from the socket. Return a
# status (True or False) and the received butes (in the former case).

def recv_bytes(sock, bytecount_target):
    # Be sure to timeout the socket if we are given the wrong
    # information.
    sock.settimeout(SOCKET_TIMEOUT)
    try:
        byte_recv_count = 0 # total received bytes
        recv_bytes = b''    # complete received message
        while byte_recv_count < bytecount_target:
            # Ask the socket for the remaining byte count.
            new_bytes = sock.recv(bytecount_target-byte_recv_count)
            # If ever the other end closes on us before we are done,
            # give up and return a False status with zero bytes.
            if not new_bytes:
                return(False, b'')
            byte_recv_count += len(new_bytes)
            recv_bytes += new_bytes
        # Turn off the socket timeout if we finish correctly.
        sock.settimeout(None)            
        return (True, recv_bytes)
    # If the socket times out, something went wrong. Return a False
    # status.
    except socket.timeout:
        sock.settimeout(None)        
        print("recv_bytes: Recv socket timeout!")
        return (False, b'')



class client:
    def __init__(self) -> None:
        print('initializing')

    def init_command(self):
        cmd = input("Input a command (connect, name, chat): ")
        if cmd == 'connect':
            self.crds_command()
        elif cmd == 'bye':
            print('Closing connection... ')
            #self.socket.close()
        elif cmd == 'name':
            name = input("Enter your display name: ")
        elif cmd[0:4] == 'chat':
            croom = input('Which room would you like to chat in? ')
            print('Connecting to {}', croom)


    def crds_command(self):
        print('You are now connected to the Chat Room Discovery Server.')
        file = open('chatroom.csv', 'rw')
        room_list = list(csv.reader(file, delimiter=','))
        cmd = input("Input a command (getdir, makeroom, deleteroom, bye): ")
        if cmd == 'getdir':
            pp.pprint(room_list)
        elif cmd == 'makeroom':
            room_name = input('What would you like to name the room? ')
            room_addr = input('What is the IP multicast address for this room? ')
            room_port = input('What is the port number for this room? ')
            room_list.append([room_name, room_addr, room_port])
        elif cmd == 'deleteroom':
            room_name = input('What is the name of the room would you like to delete? ')
            for i in range(len(room_list)):
                if room_list[i][0] == room_name:
                    room_list.pop(i)
        elif cmd == 'bye':
            file.truncate()
            room_updater = csv.writer(file)
            for i in room_list:
                room_updater.writerow(i)
            print('Changes have been committed to the CRDS. Exiting now...')
            self.init_command()
        else:
            print('Invalid command.')
            self.crds_command()



     








