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


def init_remove_oldrepo():
    backup_comment = '#This is a yum repository file that was disabled . <Migration to UiniontechOS> \
            \n'
    path = '/etc/yum.repos.d/'
    repos = os.listdir(path)
    for repo in repos:
        path_file = path+'/'+repo
        if not os.path.isfile(path_file):
            continue
        if not re.search('repo$',repo):
            continue
        with open(path_file, 'r') as fsrc:
            content = fsrc.read()
            with open(path_file+'.disabled','w') as fdst:
                fdst.write(repo+'\n'+backup_comment+content)
                fdst.close()
            fsrc.close()
        os.remove(path_file)


#初始化repo文件
def initRepoFile(baseurl):
    reposdir = '/etc/yum.repos.d/'
    h = 0
    if re.match('file:',baseurl):
        str0, path = baseurl.split('://',1)
        path = '/' + path.strip('/') + '/'
    else:
       h = 1
    if re.fullmatch('8',version[0]):
        path_appstream = baseurl+'/AppStream'
        path_baseos = baseurl+'/BaseOS'
        path_310 = baseurl+'/kernel-3.10'
        path_418 = baseurl+'/kernel-4.18'
        path_510 = baseurl+'/kernel-5.10'

        repostr_uos = '''[UniontechOS-AppStream]\nname = UniontechOS AppStream\nbaseurl = '''+path_appstream.strip('\n')+'''\nenabled = 1\ngpgcheck = 0\n\n[UniontechOS-BaseOS]\nname = UniontechOS BaseOS\nbaseurl = '''+path_baseos.strip('\n')+'''\nenabled = 1\ngpgcheck = 0\n\n[UniontechOS-kernel-4.18.0]\nname = UniontechOS Kernel-4.18.0\nbaseurl = '''+path_418.strip('\n')+'''\nenabled = 0\ngpgcheck = 0\nskip_if_unavailable = 1\n\n[UniontechOS-kernel-5.10.0]\nname = UniontechOS Kernel-5.10.0\nbaseurl = '''+path_510.strip('\n')+'''\nenabled = 0\ngpgcheck = 0\nskip_if_unavailable = 1\n\n
'''
    else:
        path_310 = baseurl+'/kernel-3.10'
        repostr_uos = '''[UniontechOS-AppStream]\nname = UniontechOS AppStream\nbaseurl = '''+baseurl.strip('\n')+'''\nenabled = 1\ngpgcheck = 0\n\n[UniontechOS-kernel-3.10.0]\nname = UniontechOS Kernel-3.10.0\nbaseurl = '''+path_310.strip('\n')+'''\nenabled = 0\ngpgcheck = 0\nskip_if_unavailable = 1\n
        '''
    repofile = os.path.join(reposdir, 'switch-to-uos.repo')
    with open(repofile,'w') as f_repo:
        f_repo.write(repostr_uos)
        f_repo.close()


#检测repo文件创建缓存
def checkRepoMakeCache():
    os.system('yum clean all')
    os.system('yum makecache')
    os_version_ret = platform.dist()
    version = os_version_ret[1].split('.',-1)
    ret = os.path.exists('/var/cache/dnf/UniontechOS-AppStream.solv')
    if ret:
        ret = os.path.exists('/var/cache/dnf/UniontechOS-BaseOS.solv')
        if ret or re.fullmatch('7',version[0]):
            return 0
        else:
            return 1
    else:
        if re.fullmatch('7',version[0]):
            ret = os.path.exists('/var/cache/yum/x86_64/7/UniontechOS-AppStream/repomd.xml')
            if ret:
                return 0
        return 1