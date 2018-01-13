#!/usr/bin/env python3.6

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

    def send(self):
        self.sock.sendall(bytes('hello', 'utf-8'))

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
        print(message)

        self.sock.sendall(bytes(message, 'utf-8'))

        response = self.read()
        return message.upper() == response

    def command_connection(self):
        message = 'COMMAND-CONNECT'
        self.sock.sendall(bytes(message, 'utf-8'))

        response = self.read()
        return message.upper() == response

    def command_shutdown(self):
        message = 'COMMAND-SHUTDOWN'
        self.sock.sendall(bytes(message, 'utf-8'))

        response = self.read()
        return message.upper() == response

    def start_video(self):
        message = 'COMMAND-START_VIDEO'
        self.sock.sendall(bytes(message, 'utf-8'))

        response = self.read()
        return message.upper() == response

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

# if drone_connection.command_shutdown():
#     print('Command successful')
# else:
#     print('error')


drone_connection.close()
