#!/usr/bin/env python3
import os
import re
import subprocess


class DestroyAgent(object):
    def __init__(self):
        self.program_file = '/usr/lib/uos-sysmig-agent'
        self.cache_file = '/var/tmp/uos-migration'
        self.pid = []

    def kill_pid(self):
        for n in range(len(self.pid)):
            if str(os.getpid()) == self.pid[n]:
                continue
            print(self.pid[n])
            subprocess.run('kill -9 {}'.format(self.pid[n]), shell=True)
            # del self.pid[n]

    def destroy_self(self):
        cmd = 'yum remove uos-sysmig-agent -y'
        subprocess.run(cmd, shell=True)
        if os.path.exists(self.program_file):
            os.removedirs(self.program_file)
        if os.path.exists(self.cache_file):
            os.removedirs(self.cache_file)
        # print(os.path.join(os.getcwd() + os.path.basename(__file__)))
        # os.remove(os.path.join(os.getcwd() + '/' + os.path.basename(__file__)))
        os.remove(os.path.join('/tmp' + '/' + os.path.basename(__file__)))

    def check_pid(self, pids):
        for i in range(len(self.pid)):
            if pids == self.pid[i]:
                return False
            if pids == os.getpid():
                return False
        return True

    def get_running_pid(self, path):
        cmd = "lsof -Pn +D {} "
        if not os.path.exists(path):
            return
        # ret = subprocess.check_output("lsof -Pn +D /usr/lib/uos-sysmig-agent", shell=True)
        # ret = str(ret, 'utf-8').split('\n')
        ret = os.popen(cmd.format(path)).readlines()
        for i in range(len(ret)):
            if 'PID' in ret[i]:
                continue
            pids = ret[i].split(' ', -1)
            for n in range(len(pids)):
                if not pids[n]:
                    continue
                if re.match('bash', pids[n]):
                    break
                if re.match(r'[0-9]', pids[n]):
                    if self.check_pid(pids[n]):
                        self.pid.append(pids[n])
                    break

    def run(self):
        self.get_running_pid(self.program_file)
        self.get_running_pid(self.cache_file)
        self.kill_pid()
        self.destroy_self()


if __name__ == "__main__":
    destroy_agent = DestroyAgent()
    destroy_agent.run()

