import os
import json
from settings import *

def list_to_json(keylist, valuelist):
    res = dict(zip(keylist, valuelist))
    res = json.dumps(res)
    return json.dumps(res)

def check_storage(data):
    agent_ip = '127.0.0.1'
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
    agent_ip = '127.0.0.1'
    os_version_ret = platform.dist()
    version = os_version_ret[1].split('.',-1)
    local_os_version = os_version_ret[0]+version[0]
    state = 0
    agent_os = local_os_version

    if re.match('.entos8',local_os_version):
        data = '当前操作系统为CentOS 8'
        return list_to_json(['ip', 'ret', 'data'],[agent_ip, state, data])
    elif re.match('.entos7',local_os_version):
        data = '当前操作系统为CentOS 7'
        return list_to_json(['ip', 'ret', 'data'],[agent_ip, state, data])
    else:
        state = 1
        data = '无法检测到当前系统，请检查/etc/os-release文件，确认后重试.'
        return list_to_json(['ip', 'ret', 'data'],[agent_ip, state, data])