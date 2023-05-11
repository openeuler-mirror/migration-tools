import os
import subprocess


def run_subprocess(cmd:str):
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        shell=True
    )
    output = ""
    try:
        for line in iter(process.stdout.readline, b""):
            output += line.decode()
            print(line.decode())
    except:
        pass
    process.communicate()
    return_code = process.poll()
    return output, return_code


def check_pkg(rpm):
    _, ret = run_subprocess('rpm -q {}'.format(rpm))
    if ret:
        return
    return True


def get_disk_info(string):
    dev_name = ""
    part_num = ""
    length = len(string)
    for c in range(length - 1, -1, -1):
        if not string[c].isdigit():
            if string.find('nvme') != -1:
                dev_name = string[0:c]
                part_num = string[c + 1:length]
            else:
                dev_name = string[0:c + 1]
                part_num = string[c + 1:length]
            break
    return dev_name, part_num



def swap_release():
    tmp_dir = '/var/tmp'
    rpme_release = 'rpm -qf /etc/os-release|xargs -i rpm -e --nodeps {}'
    run_subprocess(rpme_release)
    cmd = 'yumdownloader {} --destdir {}'.format(openEuler_release, tmp_dir)
    run_subprocess(cmd)
    run_subprocess('rpm -ivh {}/*.rpm --nodeps --force'.format(tmp_dir))


def system_sync():
    rebuilddb = 'rpm --rebuilddb;dnf clean all'
    run_subprocess(rebuilddb)
    cmd = 'dnf -y distro-sync --allowerasing --skip-broken'
    _, ret = run_subprocess(cmd)
    _, ret = run_subprocess('rpm -q kernel|grep {}'.format('uel20'))
    if ret:
        return False
    return True

def main():
    openEuler_release = 'openEuler-release'
    if not self.check_pkg('rsync'):
        print('please install rsync')
        return
    if check_pkg("yum-utils"):
        print("please install yum-utils")
        return
    if not check_pkg(openEuler_release):
        swap_release()
    if system_sync():
        print("System Migration Successful")
    else:
        print("System Migration Failed")

if __name__ == '__main__':
    main()
