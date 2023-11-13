# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier:   MulanPubL-2.0-or-later

import os
import json
import platform
import re
import time
import paramiko
import subprocess
from multiprocessing import Process


from settings import *
from sysmig_agent.utils import *
from sysmig_agent.share import *
from sysmig_agent.Abitxt2xls import *

os.chdir('/usr/lib/migration-tools-agent')


def init_dir():
    if not os.path.isdir(PRE_MIG_DIR):
        os.makedirs(PRE_MIG_DIR)
    
    if not os.path.isdir(MIGRATION_DIR):
        os.makedirs(MIGRATION_DIR)

    if not os.path.isdir(MIGRATION_KERNEL):
        os.makedirs(MIGRATION_KERNEL)
    
    if not os.path.isdir(MIGRATION_DATA_RPMS_DIR):
        os.makedirs(MIGRATION_DATA_RPMS_DIR)
    
    if not os.path.exists(PRE_MIG):
        with open(PRE_MIG,'w+') as fp:
            fp.write(' ')
            fp.close()
    
    if not os.path.exists(PROGRESS):
        with open(PROGRESS,'w+') as fp:
            fp.write(' ')
            fp.close()

    if not os.path.exists(MIGRATION_DATA_RPMS_3_INFO):
        with open(MIGRATION_DATA_RPMS_3_INFO,'w+') as fp:
            fp.write(' ')
            fp.close()

    with open(pstate,'w+') as fp:
        fp.write('0')
        fp.close()
    # 迁移进度
    migInit_porgress()


def check_os_type():
    return platform.system()

def check_os_arch():
    return platform.machine()

def check_os_kernel_release():
    return platform.release()

def preSystemCheck():
    with open(PRE_MIG,'w+') as pf:
        os_version_ret = platform.dist()
        pf.write('原系统   :'+os_version_ret[0]+'\n')
        pf.write('系统类型 :'+check_os_type()+'\n')
        pf.write('系统内核 :'+check_os_kernel_release()+'\n')
        pf.write('系统架构 : '+check_os_arch()+'\n')
        pf.close()


def check_storage(data):
    uos_sysmig_conf = json.loads(getSysMigConf())
    agent_ip = json.loads(uos_sysmig_conf).get('agentip').strip()[1:-1]
    path = '/var/cache'
    stat = os.statvfs(path)
    CACHE_SPACE = 10.0
    state = 1
    # 避免centos7系统检测失败
    time.sleep(5)
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
    init_dir()
    preSystemCheck()
    messageProgress('0')
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
    with open('/usr/lib/migration-tools-agent/.passwd.txt','w',encoding='utf-8') as f:
        text = json_data['passwd']
        f.write(text)
    uos_sysmig_conf = json.loads(getSysMigConf())
    agent_ip = json.loads(uos_sysmig_conf).get('agentip').strip()[1:-1]
    re_data = check_SSHClent(json_data['user'], json_data['passwd'], agent_ip, 22)
    return re_data



def check_os_kernel(data):
    uos_sysmig_conf = json.loads(getSysMigConf())
    AGENT_IP = json.loads(uos_sysmig_conf).get('agentip').strip()[1:-1]
    platformInfo = platform.platform()
    systemKernelVersion = platformInfo.split('-',-1)
    kernel_version = systemKernelVersion[1]
    return list_to_json(['ip','data'],[AGENT_IP,kernel_version])


def check_repo_kernel(data):
    uos_sysmig_conf = json.loads(getSysMigConf())
    AGENT_IP = json.loads(uos_sysmig_conf).get('agentip').strip()[1:-1]
    version_list = []
    os_version_ret = platform.dist()
    version = os_version_ret[1].split('.', -1)
    if re.fullmatch('8', version[0]):
        ret = os.popen('yum repoquery --nvr kernel --enablerepo UniontechOS-kernel-4.19.0')
        for r in ret.readlines():
            if re.match('kernel', r):
                kernel_version = re.sub('kernel-', '', r)
                kernel_version = re.sub('-.*$', '', kernel_version)
                version_list.append(kernel_version.strip())
    elif re.fullmatch('7', version[0]):
        cmd_310 = 'yum list --enablerepo UniontechOS-kernel-3.10.0 --disablerepo UniontechOS-AppStream  kernel'
        ret = os.popen(cmd_310)
        for r in ret.readlines():
            if re.match('kernel', r) and re.search('uelc', r):
                kernel_version = re.sub('kernel-', '', r)
                kernel_version = re.sub('-.*$', '', kernel_version)
                kernel_version=kernel_version.split(' ',-1)
                kernel = kernel_version[len(kernel_version)-1]
                version_list.append(kernel.strip())
        cmd_419 = 'yum list kernel'
        ret = os.popen(cmd_419)
        for r in ret.readlines():
            if re.match('kernel', r) and re.search('uelc', r):
                kernel_version = re.sub('kernel-', '', r)
                kernel_version = re.sub('-.*$', '', kernel_version)
                kernel_version=kernel_version.split(' ',-1)
                kernel = kernel_version[len(kernel_version)-1]
                version_list.append(kernel.strip())
    else:
        version_list = ''
    keylist = ['ip', 'data']
    print(version_list)
    valuelist = [AGENT_IP, version_list]
    return list_to_json(keylist, valuelist)


def export_reports(data):
    """
    导出接口
    :param data:
    :return:
    """
    json_data = json.loads(data)
    hostname = socket.gethostname()
    uos_sysmig_conf = json.loads(getSysMigConf())
    ip = json.loads(uos_sysmig_conf).get('agentip').strip()
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    compression = "tar zcvf /var/tmp/uos-migration/%s" % json_data.get("name") + "_%s" % ip +\
                  "_%s" % hostname + "_%s" % now + ".tar.gz" + " /var/tmp/uos-migration/%s" % json_data.get("export")
    print(compression)
    try:
        os.system(compression)
    except:
        print("export reports error: %s" % compression)

    data = {}
    scp_info = hostname + "," + ip
    data[scp_info] = scp_info
    return data


def systemCheckRequires(conflist):
    os.system('rpm --rebuilddb')
    cmd = 'rpm -qa|xargs -i rpm -V --nordev --nomode  --nomtime  --nogroup --nouser  --nosize --nofiledigest --nolinkto --noscripts --nofiles --nodigest {} >>' + PRE_MIG
    rets = os.popen(cmd)
    if rets:
        for ret in rets.readlines():
            conflist.append(ret)
        if len(conflist) > 1:
            return conflist


def fork_sh(cmd):
    try:
        fderr = open("/var/tmp/uos-migration/UOS_migration_log/err_log",'a')
        subprocess.run(cmd, stderr=fderr , shell=True)
        messageState('2')
        fderr.close()
    except:
        return 0


def env():
    cmd = 'sh sysmig_agent/Abisystmcompchk.sh'
    t = Process(target=fork_sh, args=(cmd,))
    t.start()

##系统环境检查
def check_environment(data_j):
    uos_sysmig_conf = json.loads(getSysMigConf())
    AGENT_IP = json.loads(uos_sysmig_conf).get('agentip').strip()[1:-1]
    state = None
    #abi check
    with open(pstate,'r+') as fp:
        state = fp.readlines()
        fp.close()
        state = state[0]
    if re.match('0',state):
        messageState('1')
        if systemCheckRequires([]):
            data = '1'
        env()
    if re.match('1',state):
        data = '1'
        keylist = ['ip','res','data']
        valuelist = [AGENT_IP,'2',data]
        return list_to_json(keylist,valuelist)
    elif re.match('2',state):
        abi_txt2xls()
        messageState('3')
    elif re.match('3',state) or re.match('9',state):
        data = '1'
        res = 0
        keylist = ['ip','res','data']
        valuelist = [AGENT_IP,res,data]
        messageState('9')
        return list_to_json(keylist,valuelist)
    data = '1'
    keylist = ['ip','res','data']
    valuelist = [AGENT_IP,'2',data]
    return list_to_json(keylist,valuelist)

# 检测进度
def analysisProgress():
    path = '/var/tmp/uos-migration/data/uos/rpms'
    if os.path.exists(path):
        file_list = os.listdir(path)
    else:
        return None
    h=noan=oked=1

    for file in file_list:
        path = re.sub('/$',"",path)
        cur_path = os.path.join(path, file)
        if os.path.isdir(cur_path):
            continue
        else:
            ret = file.split('.',-1)
            fret = ret[len(ret)-1]
            if re.fullmatch('rpm',fret):
                noan = noan + 1
            elif re.fullmatch('oked',fret):
                oked = oked + 1
    data = (oked/(noan+oked))*98
    data = format(data, '.1f')
    messageProgress(str(data))
    return data


def check_progress(data):
    uos_sysmig_conf = json.loads(getSysMigConf())
    AGENT_IP = json.loads(uos_sysmig_conf).get('agentip').strip()[1:-1]

    with open(pstate,'r+') as fp:
        state = fp.readlines()
        fp.close()
        state = state[0]
    if  re.fullmatch('1',state):
        if not analysisProgress():
            messageProgress('0')
        with open(progresslogdir,'r+') as fpro:
            data = fpro.readlines()
            fpro.close()
    elif re.fullmatch('0',state):
        data = '0'
    elif re.fullmatch('2',state):
        data = '99'
    elif re.fullmatch('3',state):
        data = '100'
    else:
        data = '0'
    keylist = ['ip','progress']
    valuelist = [AGENT_IP,data]
    return list_to_json(keylist,valuelist)


def ifnot_mig_kernel(kernel_version):
    with open('/etc/yum.conf', 'r') as f:
        content = f.read()
        f.close()
    if re.search(r'^distroverpkg=', content, re.MULTILINE):
        content = re.sub(r"\n(distroverpkg=)", r"\n#\1", content)
    if re.search(r'bugtracker_url=', content, re.MULTILINE):
        content = re.sub(r"\n(bugtracker_url=)", r"\n#\1", content)
    with open('/etc/yum.conf', 'w') as f:
        f.write(content)
        f.close()
    if kernel_version == '0':
        kernel_patterns = 'exclude= kernel* kernel-tools python3-perf kernel-headers kernel-devel bpftool perf kernel-core kmod-kvdo kpatch glibc-headers \n'
        with open('/etc/yum.conf', 'a+') as f:
            f.write(kernel_patterns)
            f.close()


def mig_kernel(kernel_version):
    cwd = '/var/tmp/uos-migration/kernel/'
    ret = os.listdir(cwd)
    for i in ret:
        os.unlink(cwd+i)
    cmd = ' rpm -qa | grep "kernel\|bpftool\|perf" |xargs -i rpm -q --qf "%{NAME}\\n" {}'
    ret = os.popen(cmd).readlines()
    if kernel_version == '0':
        return 0
    else:
        repo = ''
        if re.fullmatch('4.18.0',kernel_version):
            repo = 'UniontechOS-kernel-'+kernel_version.strip()
        elif re.fullmatch('5.10.0',kernel_version):
            repo = 'UniontechOS-kernel-'+kernel_version.strip()
        else:
            return 1
        down_cmd = 'yumdownloader  --destdir "/var/tmp/uos-migration/kernel" --enablerepo '+repo
        ret = os.popen(cmd).readlines()
        for i in ret:
            downpackage = down_cmd+' '+i.strip()+'-'+kernel_version.strip()
            os.system(downpackage)

        cwd = '/var/tmp/uos-migration/kernel/'
        if  os.listdir(cwd):
            os.system('rpm -Uvh "/var/tmp/uos-migration/kernel/*" --nodeps --oldpackage')
        else:
            ifnot_mig_kernel()
            return 1


def migration_details(data_j):
    uos_sysmig_conf = json.loads(getSysMigConf())
    AGENT_IP = json.loads(uos_sysmig_conf).get('agentip').strip()[1:-1]
    path = '/var/tmp/uos-migration/UOS_migration_log/mig_log.txt'
    if os.path.exists(path):
        with open(path,'r') as lf:
           data = lf.read()
        lf.close()
    else:
        data = 'Init... ...'
    keylist = ['ip','data']
    valuelist = [AGENT_IP,data]
    return list_to_json(keylist,valuelist)


##迁移进度
def rpmsProgress():
    percent = 99
    uelc_rpm = os.popen('rpm -qa|grep uelc20|wc -l').readlines()
    all_rpms = os.popen('rpm -qa|wc -l').readlines()
    rpms_progress  = percent * ( int(uelc_rpm[0].strip()) /  int(all_rpms[0].strip()))
    rpms_progress = format(rpms_progress, '.1f')
    return rpms_progress


def check_migration_progress(data_j):
    uos_sysmig_conf = json.loads(getSysMigConf())
    AGENT_IP = json.loads(uos_sysmig_conf).get('agentip').strip()[1:-1]
    if not analysisProgress():
        messageProgress('0')
    with open(pstate,'r+') as fp:
        state = fp.readlines()
        fp.close()
        state = state[0]

    if re.fullmatch('9',state):
        messageState('0')
    mig_check_migration_progress()
    with open(progresslogdir,'r+') as fpro:
        data = fpro.readlines()
        keylist = ['ip','progress']
        valuelist = [AGENT_IP,data]
        fpro.close()

    keylist = ['ip','progress']
    valuelist = [AGENT_IP,data]
    return list_to_json(keylist,valuelist)


def Sysmig(data_j):
    os_version_ret = platform.dist()
    version = os_version_ret[1].split('.',-1)
    AGENT_OS = os_version_ret[0]+version[0]
    kernel_version = json.loads(data_j).get('kernel_version')
    if re.fullmatch('8',version[0]):
        cmd = 'python3 sysmig_agent/centos82uos.py'
        t = Process(target=run_cmd2file, args=(cmd,))
        t.start()
    elif re.search('centos7',AGENT_OS):
        ex_kernel = 'sh sysmig_agent/centos72uos.sh -e "kernel-devel* kernel-headers* kernel-tools* kernel* bpftool perf python-perf kernel-abi* kernel-modules kernel-core kmod-kvdo"'
        if kernel_version == '0':
            run_cmd2file(ex_kernel)
            messageState('3')
        elif kernel_version == '3.10.0' :
            run_cmd2file(ex_kernel)
            cmd_k = 'sh sysmig_agent/kernel.sh -k 3.10.0'
            run_cmd2file(cmd_k)
            messageState('3')
        else:
            cmd = 'sh sysmig_agent/centos72uos.sh'
            run_cmd2file(cmd)
            messageState('3')


def system_migration(data_j):
    uos_sysmig_conf = json.loads(getSysMigConf())
    AGENT_IP = json.loads(uos_sysmig_conf).get('agentip').strip()[1:-1]
    state = '1'
    res = '0'
    kernel_version = json.loads(data_j).get('kernel_version')
    with open(pstate,'r+') as fp:
        state = fp.readlines()
        fp.close()
    state = state[0]
    if re.match('0',state):
        messageState('1')
        ifnot_mig_kernel(kernel_version)
        t = Process(target=Sysmig, args=(data_j,))
        t.start()
    elif re.fullmatch('2',state):
        messageState('6')
        mig_kernel(kernel_version)
        with open(PRE_MIG,'r') as fp:
            stros = fp.readlines()
            oldos = stros[0]
            fp.close()
        oldos = oldos.split(':',1)
        main_conf(oldos[1]) 
        if os.path.exists('/var/tmp/uos-migration/data/exp-rst/systeminfo.txt'):
            run_cmd2file('sh sysmig_agent/Abitranrept.sh')
            abi_txt2xls_after_mig()
        messageState('4')
    elif re.fullmatch('4',state):
        messageState('5')
        if os.path.exists('/var/tmp/uos-migration/UOS_migration_log/rpms-verified-after.txt'):
            res = '0'
        else:
            res = '-1'
    elif re.fullmatch('3',state):
        messageState('5')
        if os.path.exists('/var/tmp/uos-migration/data/exp-rst/systeminfo.txt'):
            run_cmd2file('sysmig_agent/Abitranrept.sh')
            abi_txt2xls_after_mig()
        if os.path.exists('/var/tmp/uos-migration/UOS_migration_log/rpms-list-after.txt'):
            res = '0'
        else:
            res = '-1'
    elif re.fullmatch('5',state):
        if re.fullmatch('-1',res):
            data =' 迁移失败。'
            keylist = ['ip','res','error']
            valuelist = [AGENT_IP,res,data]
            return list_to_json(keylist,valuelist)
        else:
            data = '迁移成功。'
        keylist = ['ip','res','data']
        valuelist = [AGENT_IP,res,data]
        return list_to_json(keylist,valuelist)
    
    res = '2'
    data = '......'
    keylist = ['ip','res','data']
    valuelist = [AGENT_IP,res,data]
    return list_to_json(keylist,valuelist)
