
########################################################################

import socket
import argparse
import sys
import time
import struct
import ipaddress
import csv
import pprint
import threading

########################################################################

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
        return (False, b'')

class Server:

    HOSTNAME = "127.0.0.1"

    PORT = 50000
    RECV_SIZE = 1024
    BACKLOG = 5
    ENCODING = 'utf-8'

    thread_list = []

    def __init__(self) -> None:
        self.create_listen_socket()
        #self.open_chatrooms()
        self.process_connections_forever()
    
    def open_chatrooms(self):
        f = open('chatrooms.csv')
        room_list = list(csv.reader(f, delimiter=','))
        f.close()
        
        for i in room_list:
            threading.Thread()

    # def create_chatroom(self, addr, port):
    #     try:
    #         my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #         ttl = struct.pack('B', 1)
    #         my_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    #         my_socket.bind((addr, port))

    def create_listen_socket(self):
        try:    
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((Server.HOSTNAME, Server.PORT))
            self.socket.listen(Server.BACKLOG)
            print("CRDS Listening on port {} ...".format(Server.PORT))
        except Exception as msg:
            print(msg)
            exit() 

    def process_connections_forever(self):
        try:
            while True:
                self.connection_handler(self.socket.accept())

        except KeyboardInterrupt:
            print()

        finally:
            self.socket.close()
    
    def connection_handler(self, client):

        connection, address = client
        print("-" * 72)
        print("Connection received from {}.".format(address))
        self.crds(connection)

    def crds(self, connection):

        while True:
            recvbytes = connection.recv(Server.RECV_SIZE)
            command = recvbytes.decode(Server.ENCODING)

            if command == 'getdir':
                print("Chatroom directory was requested. Sending now... ")
            
            elif command == 'makeroom':
                print('Client would like to make a room. Awaiting information about new chatroom... ')
                
                #awating information about new chatroom name
                status = False

                while not status:
                    status, room_name_size_bytes = recv_bytes(connection, 32)

                room_name_size = int.from_bytes(room_name_size_bytes, byteorder='big')
                status = False

                while not status:
                    status, room_name_bytes = recv_bytes(connection, room_name_size)
                
                room_name = room_name_bytes.decode(self.ENCODING)
                status = False

                #awaiting information about new chatroom ip address
                while not status:
                    status, room_addr_size_bytes = recv_bytes(connection, 32)

                room_addr_size = int.from_bytes(room_addr_size_bytes, byteorder='big')
                status = False

                while not status:
                    status, room_addr_bytes = recv_bytes(connection, room_addr_size)
                
                room_addr = room_addr_bytes.decode(self.ENCODING)
                status = False

                #awaiting information about new chatroom port number
                while not status:
                    status, room_port_size_bytes = recv_bytes(connection, 32)

                room_port_size = int.from_bytes(room_port_size_bytes, byteorder='big')
                status = False

                while not status:
                    status, room_port_bytes = recv_bytes(connection, room_port_size)
                
                room_port = room_port_bytes.decode(self.ENCODING)
                status = False

                print('Client would like to make {} with IP address {} and port number {}. Creating now.'.format(room_name, room_addr, room_port))
                    

            elif command == 'deleteroom':
                print('Client would like to delete a room. Awaiting information about room to delete... ')

                status = False

                while not status:
                    status, room_name_size_bytes = recv_bytes(connection, 32)

                room_name_size = int.from_bytes(room_name_size_bytes, byteorder='big')
                status = False

                while not status:
                    status, room_name_bytes = recv_bytes(connection, room_name_size)
                
                room_name = room_name_bytes.decode(self.ENCODING)

                print('Client would like to delete {}. Deleting now... '.format(room_name))

            elif command == 'bye':
                print('Appending changes to chatroom directory.')
                print('Closing connection... ')
                connection.close()
                break


class Client:

    username = 'Guest'
    RECV_SIZE = 1024
    HOSTNAME = socket.gethostname()
    MSG_ENCODING = "utf-8"


    def __init__(self):
        self.get_socket()
        self.init_command()

    def get_socket(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as msg:
            print(msg)
            exit()

    def connect_to_server(self):
        try:
            self.socket.connect((Server.HOSTNAME, Server.PORT))
        except Exception as msg:
            print(msg)
            exit()

    def init_command(self):
        cmd = input("Input a command (connect, name, chat): ")
        if cmd == 'connect':
            self.connect_to_server()
            self.crds_command()
  
        elif cmd == 'name':
            self.username = input("Enter your display name: ")
            print('Display name has been updated to be {}.'.format(self.username))
            self.init_command()

        elif cmd[0:4] == 'chat':
            croom = input('Which room would you like to chat in? ')
            print('Connecting to {}'.format(croom))


    def crds_command(self):
        print('You are now connected to the Chat Room Discovery Server.')

        file = open('chatrooms.csv')
        room_list = list(csv.reader(file, delimiter=','))
        file.close()
        
        while True:
            cmd = input("Input a command (getdir, makeroom, deleteroom, bye): ")

            if cmd == 'getdir':
                self.socket.sendall(cmd.encode(self.MSG_ENCODING))
                pp = pprint.PrettyPrinter(indent=4)
                pp.pprint(room_list)

            elif cmd == 'makeroom':
                self.socket.sendall(cmd.encode(self.MSG_ENCODING))

                room_name = input('What would you like to name the room? ')
                while True:
                    room_addr = input('What is the IP multicast address for this room? (239.x.x.x)')
                    #print(room_addr[:3])
                    if room_addr[:3] == '239':
                        break
                    else:
                        print('Invalid IP address.')
                room_port = input('What is the port number for this room? ')

                room_list.append([room_name, room_addr, room_port])

                name_bytes = room_name.encode(self.MSG_ENCODING)
                addr_bytes = room_addr.encode(self.MSG_ENCODING)
                port_bytes = room_port.encode(self.MSG_ENCODING)

                name_len = len(name_bytes).to_bytes(32, byteorder='big')
                addr_len = len(addr_bytes).to_bytes(32, byteorder='big')
                port_len = len(port_bytes).to_bytes(32, byteorder='big')

                pkt = name_len + name_bytes + addr_len + addr_bytes + port_len + port_bytes
                self.socket.sendall(pkt)

            elif cmd == 'deleteroom':
                self.socket.sendall(cmd.encode(self.MSG_ENCODING))

                room_name = input('What is the name of the room would you like to delete? ')
                for i in range(len(room_list)):
                    if room_list[i][0] == room_name:
                        room_list.pop(i)

                name_bytes = room_name.encode(self.MSG_ENCODING)
                name_len = len(name_bytes).to_bytes(32, byteorder='big')

                pkt = name_len + name_bytes
                self.socket.sendall(pkt)

            elif cmd == 'bye':
                self.socket.sendall(cmd.encode(self.MSG_ENCODING))

                file = open('chatrooms.csv', 'w')
                room_updater = csv.writer(file)
                for i in room_list:
                    room_updater.writerow(i)
                print('Changes have been committed to the CRDS. Exiting now...')
                self.socket.close()
                break

            else:
                print('Invalid command.')
        
            

if __name__ == '__main__':
    roles = {'client': Client,'server': Server}
    parser = argparse.ArgumentParser()

    parser.add_argument('-r', '--role',
                        choices=roles, 
                        help='server or client role',
                        required=True, type=str)

    args = parser.parse_args()
    roles[args.role]()