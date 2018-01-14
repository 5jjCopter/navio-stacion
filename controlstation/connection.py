#!/usr/bin/env python3.6
import time
import socket
import sys


class Reporter():
    def __init__(self):
        pass


class ControlConnection():
    sock = None
    gcs_info = None

    def __init__(self, host, port, gcs_info):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.gcs_info = gcs_info

    def send(self, message):
        self.sock.sendall(bytes(message, 'utf-8'))
        response = self.read()
        return message.upper() == response

    def read(self):
        return str(self.sock.recv(1025), 'utf-8')

    def send_info(self):
        '''
        Transmit information about GCS
        Expects a map
        '''
        # message = 'MESSAGE-ip:{0}-port:{1}'.format(self.gcs_info['ip'],
        #                                            self.gcs_info['port'])
        message = 'MESSAGE'
        for k, v in self.gcs_info.items():
            message += '-{0}:{1}'.format(k, v)
        return self.send(message)

    def command_connection(self):
        message = 'COMMAND-CONNECT'
        return self.send(message)

    def command_shutdown(self):
        message = 'COMMAND-SHUTDOWN'
        return self.send(message)

    def start_video(self):
        message = 'COMMAND-START_VIDEO'
        return self.send(message)

    def start_killswitch(self):
        message = 'COMMAND-START_KILLSWITCH'
        return self.send(message)

    def close(self):
        self.sock.close()
        self.sock = None


details = {'ip': '127.0.0.1', 'port': 14550,
           'video_bitrate': 500000, 'video_fps': 15}

drone_connection = ControlConnection('localhost', 9999, details)

if drone_connection.send_info():
    print('message sent and confirmed')
else:
    print('error')

if drone_connection.command_connection():
    print('Command successful')
else:
    print('error')

if drone_connection.start_video():
    print('Command successful')
else:
    print('error')

if drone_connection.start_killswitch():
    print('Command successful')
else:
    print('error')


if drone_connection.command_shutdown():
    print('Command successful')
else:
    print('error')

drone_connection.close()
