#!/usr/bin/env python3.6
import xmlrpc.client
from beaconrx import BeaconRx
from tunnels import SSHtunnels
import time

# server = xmlrpc.client.ServerProxy('http://localhost:9001/RPC2')

# print('State: {}'.format(server.supervisor.getState()))
# print('State: {}'.format(server.twiddler.getAPIVersion()))

# for e in server.system.listMethods():
#     print(e)

# print(server.twiddler.getGroupNames())
# server.twiddler.addProgramToGroup("copter", "video", {'command': 'ls -lrt /'})

# server.supervisor.stopProcess('copter:video')
# server.supervisor.startProcess('copter:video')
# x = server.supervisor.readProcessStdoutLog('copter:video', 0, 2e6)
# print(len(x))
# print(x)

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


supervisor_port = '9001'
process_map = {'video': '/home/drobban/code/drone_xsystem_v1/controlstation/fake.sh',
               'arducopter':  '/home/drobban/code/drone_xsystem_v1/controlstation/fake.sh'}


beacon = BeaconRx('0.0.0.0', 9999)

drone_control = None
drone_ip = None
try:
    drone_ip = beacon.get_ip(timeout=15)
except TimeoutError:
    print('Unable to connect. Could not find beacon')

try:
    if drone_ip:
        print('IP: {}'.format(drone_ip))
        supervisor_tunnel = SSHtunnels('drobban', drone_ip, '7777', supervisor_port)
except TimeoutError as e:
    print('Tunnel creation timeout\n')

try:
    if drone_ip:
        drone_control = ControlStation('127.0.0.1', '7777')
        drone_control.add_procmap(process_map)
        drone_control.output(0, 2e4)
except ConnectionRefusedError as e:
    print('Supervisor problem?')


try:
    drone_control.close()
except:
    print('Problem?')

try:
    supervisor_tunnel.close()
except:
    print('Unable to close tunnel')
beacon.close()

