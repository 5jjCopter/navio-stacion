#!/usr/bin/env python3
import time
import socket
from urllib import request


class Beacon():
    sock = None

    def __init__(self, host, port, spec_ip=None):
        self.given_ip = spec_ip
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((host, port))

    def send(self, message):
        self.sock.sendall(bytes(message, 'utf-8'))

    def read(self):
        return str(self.sock.recv(1024), 'utf-8')

    def ping(self):
        message = request.urlopen('http://ipinfo.io/ip').read().decode('utf-8')[:-1]
        if self.given_ip:
            return self.send(self.given_ip)
        else:
            return self.send(message)

    def close(self):
        self.sock.close()
        self.sock = None

if __name__ == '__main__':
    GCS_IP = '94.245.62.12'
    GCS_PORT = 9999

    while 1:
        time.sleep(10)
        beacon_station = Beacon(GCS_IP, GCS_PORT, '192.168.100.147')
        beacon_station.ping()
        beacon_station.close()
