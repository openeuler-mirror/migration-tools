import os
import json
import platform
import re
import time
import paramiko

from settings import *
from func.utils import list_to_json
from func.share import *

def check_storage(data):
    uos_sysmig_conf = json.loads(getSysMigConf())
    agent_ip = json.loads(uos_sysmig_conf).get('agentip').strip()[1:-1]
    path = '/var/cache'
    stat = os.statvfs(path)
    CACHE_SPACE = 10.0
    state = 1
    if stat:
        ava_cache = format(stat.f_bavail * stat.f_frsize / 1024 // 1024 /1024, '.1f')
        with open(PRE_MIG,'a+') as pf:
            pf.write('/var/cache可用空间为'+ava_cache+'GB')
            pf.close()
        if float(ava_cache) >= CACHE_SPACE:
            state = 0
            keylist = ['ip', 'ret', 'data']
            data = '可用空间为'+ava_cache+'GB'
            valuelist = [agent_ip, state, data]
            return list_to_json(keylist, valuelist)
        else:
            keylist = ['ip', 'ret', 'error']
            data = '可用空间为' + ava_cache + 'GB,请清理/var/cache的空间后重试。'
            valuelist = [agent_ip, state, data]
            return list_to_json(keylist, valuelist)
    else:
        keylist = ['ip', 'ret', 'error']
        data = '可用空间为'+ava_cache+'GB,请清理/var/cache的空间后重试。'
        valuelist = [agent_ip, state, data]
        return list_to_json(keylist, valuelist)


def check_os(data):
    uos_sysmig_conf = json.loads(getSysMigConf())
    agent_ip = json.loads(uos_sysmig_conf).get('agentip').strip()[1:-1]
    os_version_ret = platform.dist()
    version = os_version_ret[1].split('.',-1)
    local_os_version = os_version_ret[0]+version[0]
    state = 0

    if re.match('.entos8',local_os_version):
        data = '当前操作系统为CentOS 8'
        return list_to_json(['ip', 'ret', 'data'],[agent_ip, state, data])
    elif re.match('.entos7',local_os_version):
        data = '当前操作系统为CentOS 7'
        return list_to_json(['ip', 'ret', 'data'],[agent_ip, state, data])
    else:
        state = 1
        error = '无法检测到当前系统，请检查/etc/os-release文件，确认后重试.'
        return list_to_json(['ip', 'ret', 'error'],[agent_ip, state, error])

def check_SSHClent(user, passwd, ip, port):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    t = 0
    for _ in range(10):
        t += 1
        time.sleep(1)
        try:
            ssh.connect(ip, username=user, password=passwd, port=port)
            if user != "root":
                stdin, stdout, stderr = ssh.exec_command('sudo -v')
                flag = True
                ret = stderr.read().decode()
                ret = ret.split('\n')[:-1]
                for i in range(len(ret)):
                    if re.match('sudo',ret[i].strip()[0:4]):
                        flag = False
                    strsudo = ret[i].strip()
                if flag:
                    if ret != 'sudo':
                        data = list_to_json(['res', 'error'], ['1', '此用户没有root权限'])
                        return data

            ssh.close()
            data = list_to_json(['res', 'data'], ['0', '验证完成成功'])
            return data
        except:
            print("error:" + ip + user + passwd + str(port))
    data = list_to_json(['res', 'error'], ['1', '此用户没有root权限'])
    return data


def check_user(data):
    """
    检测用户密码
    :param data:
    :return:
    """
    log_info = "post check_user:" + str(data)
    print(log_info)
    json_data = json.loads(data)
    with open('/usr/lib/uos-sysmig-agent/.passwd.txt','w',encoding='utf-8') as f:
        text = json_data['passwd']
        f.write(text)
    uos_sysmig_conf = json.loads(getSysMigConf())
    agent_ip = json.loads(uos_sysmig_conf).get('agentip').strip()[1:-1]
    re_data = check_SSHClent(json_data['user'], json_data['passwd'], agent_ip, 22)
    return re_data

