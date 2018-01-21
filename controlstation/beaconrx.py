#!/usr/bin/env python3.6
import select
import time
import socket
import sys


class BeaconRx():
    server_sock = None
    sockets = []
    outputs = []
    handler = None

    def __init__(self, host, port):
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind((host, port))
        # self.server_sock.listen(2)
        self.sockets.append(self.server_sock)
        self.drone_ip = ''


    def close(self):
        self.server_sock.close()
        self.server_sock = None
        self.sockets = []

    def read_message(self, conn):
        data, addr = conn.recvfrom(1024)
        data = str(data, 'utf-8')
        if data:
            print('Addr data: {0}'.format(addr))
            self.drone_ip = data[:-1]
        else:
            print('{0} \t disconnected'.format(conn.getpeername()[0]))
            return -1

    def net_event(self, input_obj):
        self.read_message(input_obj)

    def run(self):
        while 1:
            io_inputs = self.sockets
            inputdata, outputdata, exceptional = select.select(io_inputs, self.outputs, io_inputs)
            for input_obj in inputdata:
                if input_obj in self.sockets:
                    self.net_event(input_obj)
            for conn in exceptional:
                self.sockets.remove(conn)
            print('Drone got IP: {0}'.format(self.drone_ip))


if __name__ == '__main__':
    LISTEN_IP = '0.0.0.0'
    LISTEN_PORT = 9999
    receiver_station = BeaconRx(LISTEN_IP, LISTEN_PORT)
    receiver_station.run()
