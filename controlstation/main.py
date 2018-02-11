#!/usr/bin/env python3.6
from beaconrx import BeaconRx
from tunnels import SSHtunnels
from supercontrol import ControlStation
import time


if __name__ == '__main__':
    user = 'drobban'
    supervisor_port_binding = ['7777', '9001']
    joystick_port_binding = ['8888', '777']
    process_map = {'video': '/home/drobban/code/drone_xsystem_v1/controlstation/fake.sh',
                   'arducopter':  '/home/drobban/code/drone_xsystem_v1/controlstation/fake.sh'}

    tunnels = {}
    beacon = BeaconRx('0.0.0.0', 9999)

    try:
        drone_ip = beacon.get_ip(timeout=10)
        print('Got connection from {}'.format(drone_ip))
        if drone_ip:
            tunnels['supervisor'] = SSHtunnels(user, drone_ip,
                                               supervisor_port_binding[0],
                                               supervisor_port_binding[1])

            tunnels['joystick'] = SSHtunnels(user, drone_ip,
                                             joystick_port_binding[0],
                                             joystick_port_binding[1])
            print('Tunnels connected')

            drone_control = ControlStation('127.0.0.1', supervisor_port_binding[0])
            drone_control.add_procmap(process_map)
    except TimeoutError as e:
        print('Timeout {}'.format(e))
    except ConnectionRefusedError as e:
        print('Supervisor problem?')



    try:
        drone_control.close()
    except:
        print('Problem?')

    try:
        for name, tunnel in tunnels.items():
            print('closing {}'.format(name))
            tunnel.close()
    except Exception as e:
        print('{} Unable to close tunnels'.format(e))

    beacon.close()
    print('Beacon receiver closed')

