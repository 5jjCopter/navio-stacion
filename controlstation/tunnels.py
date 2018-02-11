#!/usr/bin/env python3.6
import time
import subprocess
import psutil
import shlex

class SSHtunnels():
    def __init__(self, user, host, local_port, remote_port, timeout=5):
        '''
        timeout=5 as default.
        '''
        ssh_command = 'ssh -tt -L {local}:127.0.0.1:{remote} {username}@{host}'.format(username=user,
                                                                                   host=host,
                                                                                   local=local_port,
                                                                                   remote=remote_port)
        sub_string = shlex.split(ssh_command)
        self.tunnel = subprocess.Popen(sub_string,
                                       stdout=subprocess.DEVNULL,
                                       stderr=subprocess.DEVNULL,
                                       stdin=subprocess.DEVNULL)

        #block until established status.
        not_done = True
        timer = 0
        while not_done:
            try:
                status = {conn.laddr[1]: conn.status for conn in psutil.Process(self.tunnel.pid).connections()}
            except:
                status = {}

            if int(local_port) in status:
                not_done = not ('LISTEN' == status[int(local_port)])
            time.sleep(1)
            timer += 1
            if timer > timeout:
                self.tunnel.terminate()
                raise TimeoutError

    def close(self):
        self.tunnel.terminate()



if __name__ == '__main__':
    tunnel = SSHtunnels('drobban', '192.168.100.147', '7777', '9001')
    tunnel.close()

