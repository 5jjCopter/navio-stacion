#!/usr/bin/env python3.6
import multiprocessing as mp
import select
import time
import socket
import sys


class BeaconRx():
    '''
    When initialized latest known IP is fetched from
    get_ip()
    '''
    server_sock = None
    handler = None

    def __init__(self, host, port):
        self.sockets = []
        self.outputs = []

        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind((host, port))
        # self.server_sock.listen(2)
        self.sockets.append(self.server_sock)
        self.drone_ip = ''

        # Setup for async IO. Expose latest IP via get_ip()
        self.manager = mp.Manager()
        self.s = self.manager.dict({'ip': None})
        self.p = mp.Process(target=self._run, args=(self.s, ))
        self.p.start()

    def close(self):
        self.server_sock.close()
        self.server_sock = None
        self.sockets = []
        self.p.terminate()

    def get_ip(self, timeout=None):
        '''
        Blocks until IP is available
        If timeout given it will raise TimeoutError
        '''
        timer = 0
        while self.s['ip'] == None:
            time.sleep(1)
            timer += 1
            if timeout == None:
                return self.s['ip']
            elif timer >= timeout:
                raise TimeoutError

        return self.s['ip']

    def read_message(self, conn):
        data, addr = conn.recvfrom(1024)
        data = str(data, 'utf-8')
        if data:
            self.drone_ip = data
            self.s['ip'] = self.drone_ip
        else:
            # print('{0} \t disconnected'.format(conn.getpeername()[0]))
            return -1

    def net_event(self, input_obj):
        self.read_message(input_obj)

    def _run(self, x=None):
        sys.stdout = open('/dev/null', 'w')
        while 1:
            # io_inputs = self.sockets
            io_inputs = self.sockets
            inputdata, outputdata, exceptional = select.select(io_inputs, self.outputs, io_inputs, 10)
            try:
                self.s['ip'] = None
            except BrokenPipeError:
                pass

            for input_obj in inputdata:
                if input_obj in self.sockets:
                    self.net_event(input_obj)
            for conn in exceptional:
                self.sockets.remove(conn)
            # print('Drone got IP: {0}'.format(self.drone_ip))


if __name__ == '__main__':
    LISTEN_IP = '0.0.0.0'
    LISTEN_PORT = 9999
    receiver_station = BeaconRx(LISTEN_IP, LISTEN_PORT)
    # receiver_station._run()
    for x in range(30000):
        time.sleep(0.1)
        print('Fetched from beacon {0}'.format(receiver_station.get_ip()))
    # receiver_station._run()
    receiver_station.close()
