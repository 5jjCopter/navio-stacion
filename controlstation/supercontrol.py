#!/usr/bin/env python3.6
import xmlrpc.client
from beaconrx import BeaconRx
from tunnels import SSHtunnels


class ControlStation():

    def __init__(self, host, port):
        self.proc_map = {}

        host_string = 'http://{0}:{1}/RPC2'.format(host, port)
        self.rpc_server = xmlrpc.client.ServerProxy(host_string)

    def add_procmap(self, process_map):
        self.proc_map = process_map

        for process_id, command in process_map.items():
            try:
                self.rpc_server.twiddler.addProgramToGroup('copter', process_id, {'command': command})
            except:
                print('process_id occupied - passing {}'.format(process_id))

    def close(self):
        '''
        Remove all processes added to group
        This to clean up supervisor after we are done
        '''
        for process_id, command in self.proc_map.items():
            try:
                self.rpc_server.supervisor.stopProcess('copter:{}'.format(process_id))
            except xmlrpc.client.Fault as e:
                print('Not running, ok. - {}'.format(e))

            try:
                self.rpc_server.twiddler.removeProcessFromGroup('copter', process_id)
            except xmlrpc.client.Fault as e:
                print('Process is probably not found. - {}'.format(e))

    def output(self, offset, length):
        '''
        Just for debugging.
        '''
        proc_info = self.rpc_server.supervisor.getAllProcessInfo()
        # print(self.proc_map)
        for info in proc_info:
            pass
            print('Name: {0} \t State: {1}\n'.format(info['name'], info['statename']))
            print(self.rpc_server.supervisor.readProcessStdoutLog('copter:{}'.format(info['name']), offset, length))


