# ！/usr/bin/env python3
import re
import subprocess, os


class DestroyAgent(object):
    def __init__(self):
        self.program_file = '/usr/lib/uos-sysmig-agent'
        self.cache_file = '/var/tmp/uos-migration'
        self.pid = []

    def kill_pid(self):
        for n in range(len(self.pid)):
            subprocess.run('kill -9 {}'.format(self.pid[n]))
            del self.pid[n]

    def check_pid(self, pids):
        for i in range(len(self.pid)):
            if pids == self.pid[i]:
                return False
        return True

    def get_running_pid(self, path):
        cmd = "lsof -Pn +D {} "
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
                if re.match(r'[0-9]', pids[n]):
                    if self.check_pid(pids[n]):
                        self.pid.append(pids[n])
                    break

    def run(self):
        self.get_running_pid(self.program_file)
        self.get_running_pid(self.cache_file)
        print(self.pid)


destroy_agent = DestroyAgent()
destroy_agent.run()
destroy_agent.kill_pid()
