#!/usr/bin/env python3.6
import select
import time
import socket


class StationHandler():
    commands = {}

    def __init__(self):
        self.commands = {'CONNECT': self.connect_gcs,
                         'SHUTDOWN': self.shutdown_drone,
                         'START_VIDEO': self.start_video}

    def start_video(self, details):
        print('Starting video')
        return 1

    def connect_gcs(self, details):
        print('Connecting to gcs')
        return 1

    def shutdown_drone(self, details):
        print('Shutting down drone')
        return -1

    def handle_message(self, station, data):
        '''
        If settings needs to be sent.
        Do it as an message.
        '''
        parts = data.split('-')
        for kv in parts[1:]:
            (key, val) = kv.split(':')
            station.gcs_info[key] = val
        return 1

    def handle_command(self, station, data):
        rcommand = data.split('-')[-1]
        if rcommand in self.commands:
            return self.commands[rcommand](station.gcs_info)
        return 0

    def handle(self, station, data):
        if 'MESSAGE-' in data:
            return self.handle_message(station, data)
        elif 'COMMAND-' in data:
            return self.handle_command(station, data)
        return 0


class DroneStation():
    sock = None
    gcs_info = {}
    clients = []
    outputs = []
    handler = None

    def __init__(self, host, port, handler):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))
        self.sock.listen(2)
        if not callable(handler):
            raise NotImplementedError
        else:
            self.handler = handler()
        # Misleading I know
        self.clients.append(self.sock)

    def accept(self):
        # self.clients.append(self.sock.accept())
        conn, raddr = self.sock.accept()
        self.clients.append(conn)
        self.outputs.append(conn)
        return self.clients[-1]

    def close(self):
        self.sock.close()
        self.sock = None
        self.clients = []

    def handle(self, data):
        return self.handler.handle(self, data)

    def read_message(self, conn):
        data = ''
        data = str(conn.recv(1025), 'utf-8')
        if data:
            status = self.handle(data)
            if status == -1:
                self.confirm(conn, data)
            elif status:
                print('Sending confirmation')
                self.confirm(conn, data)
            else:
                print('Sending error')
                self.deny(conn, data)
        else:
            print('EOF on socket')
            return -1

    def confirm(self, conn, data):
        conn.sendall(bytes(data.upper(), 'utf-8'))

    def deny(self, conn, data):
        conn.sendall(bytes('error', 'utf-8'))

    def run(self):
        while 1:
            inputdata, outputdata, exceptional = select.select(self.clients, self.outputs, self.clients)
            for conn in inputdata:
                if conn == self.sock:
                    self.accept()
                    print('#Clients: {0} \t Got connection \t '.format(len(self.outputs)))
                else:
                    if self.read_message(conn) == -1:
                        self.clients.remove(conn)
                        self.outputs.remove(conn)
                        print('#Clients: {0} \t Client disconnected \t'.format(len(self.outputs)))
            for conn in exceptional:
                self.clients.remove(conn)

HOST = 'localhost'
PORT = 9999
station = DroneStation(HOST, PORT, StationHandler)

# Need to handle disconnecting clients.
# Also multiple clients might be a good idea in case of trouble?
station.run()

# print(station.gcs_info)
station.close()
