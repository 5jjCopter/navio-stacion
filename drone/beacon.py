#!/usr/bin/env python3
import select
import time
import socket
import sys
from urllib import request


class Beacon():
    sock = None

    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((host, port))

    def send(self, message):
        self.sock.sendall(bytes(message, 'utf-8'))

    def read(self):
        return str(self.sock.recv(1024), 'utf-8')

    def ping(self):
        message = request.urlopen('http://ipinfo.io/ip').read().decode('utf-8')
        # message = 'HELLO'
        return self.send(message)

    def close(self):
        self.sock.close()
        self.sock = None

if __name__ == '__main__':
    GCS_IP = '94.245.62.12'
    GCS_PORT = 9999

    while 1:
        time.sleep(10)
        beacon_station = Beacon(GCS_IP, GCS_PORT)
        beacon_station.ping()
        beacon_station.close()
