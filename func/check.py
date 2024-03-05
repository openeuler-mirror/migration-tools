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
from func.utils import *
from func.share import *
from func.Abitxt2xls import *

os.chdir('/usr/lib/migration-tools-agent')


def mig_init_porgress():
    uelc_rpm = os.popen('rpm -qa|wc -l').readlines()
    with open('/var/tmp/uos-migration/.rpms', 'w+') as fp:
        fp.write(uelc_rpm[0])
        fp.close()
    return None


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
        with open(PRE_MIG, 'w+') as fp:
            fp.write(' ')
            fp.close()
    
    if not os.path.exists(PROGRESS):
        with open(PROGRESS, 'w+') as fp:
            fp.write(' ')
            fp.close()

    if not os.path.exists(MIGRATION_DATA_RPMS_3_INFO):
        with open(MIGRATION_DATA_RPMS_3_INFO, 'w+') as fp:
            fp.write(' ')
            fp.close()

    with open(pstate, 'w+') as fp:
        fp.write('0')
        fp.close()
    mig_init_porgress()
    return None


def pre_system_check():
    with open(PRE_MIG, 'w+') as pf:
        os_version_ret = platform.dist()
        pf.write('原系统   :'+os_version_ret[0]+'\n')
        pf.write('系统类型 :'+platform.system()+'\n')
        pf.write('系统内核 :'+platform.release()+'\n')
        pf.write('系统架构 : '+platform.machine()+'\n')
        pf.close()
    return None


def check_storage(data):
    uos_sysmig_conf = json.loads(get_sysmig_conf())
    agent_ip = json.loads(uos_sysmig_conf).get('agentip').strip()[1:-1]
    path = '/var/cache'
    stat = os.statvfs(path)
    cache_space = 10.0
    state = 1
    ava_cache = 0
    time.sleep(5)
    if stat:
        ava_cache = format(stat.f_bavail * stat.f_frsize / 1024 // 1024 / 1024, '.1f')
        with open(PRE_MIG, 'a+') as pf:
            pf.write('/var/cache可用空间为'+ava_cache+'GB')
            pf.close()
        if float(ava_cache) >= cache_space:
            state = 0
            k_list = ['ip', 'ret', 'data']
            data = '可用空间为'+ava_cache+'GB'
            v_list = [agent_ip, state, data]
            return list_to_json(k_list, v_list)
        else:
            k_list = ['ip', 'ret', 'error']
            data = '可用空间为' + ava_cache + 'GB,请清理/var/cache的空间后重试。'
            v_list = [agent_ip, state, data]
            return list_to_json(k_list, v_list)
    else:
        k_list = ['ip', 'ret', 'error']
        data = '可用空间为'+ava_cache+'GB,请清理/var/cache的空间后重试。'
        v_list = [agent_ip, state, data]
        return list_to_json(k_list, v_list)


def check_os(data):
    uos_sysmig_conf = json.loads(get_sysmig_conf())
    agent_ip = json.loads(uos_sysmig_conf).get('agentip').strip()[1:-1]
    init_dir()
    pre_system_check()
    message_progress('0')
    os_version_ret = platform.dist()
    version = os_version_ret[1].split('.', -1)
    local_os_version = os_version_ret[0]+version[0]
    state = 0

    if re.match('.entos8', local_os_version):
        data = '当前操作系统为CentOS 8'
        return list_to_json(['ip', 'ret', 'data'], [agent_ip, state, data])
    elif re.match('.entos7', local_os_version):
        data = '当前操作系统为CentOS 7'
        return list_to_json(['ip', 'ret', 'data'], [agent_ip, state, data])
    else:
        state = 1
        error = '无法检测到当前系统，请检查/etc/os-release文件，确认后重试.'
        return list_to_json(['ip', 'ret', 'error'], [agent_ip, state, error])


def check_ssh_client(user, passwd, ip, port):
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
                    if re.match('sudo', ret[i].strip()[0:4]):
                        flag = False
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
    with open('/usr/lib/migration-tools-agent/.passwd.txt', 'w', encoding='utf-8') as f:
        text = json_data['passwd']
        f.write(text)
    uos_sysmig_conf = json.loads(get_sysmig_conf())
    agent_ip = json.loads(uos_sysmig_conf).get('agentip').strip()[1:-1]
    re_data = check_ssh_client(json_data['user'], json_data['passwd'], agent_ip, 22)
    return re_data


def init_remove_old_repo():
    backup_comment = '#This is a yum repository file that was disabled . <Migration to UiniontechOS> \
            \n'
    path = '/etc/yum.repos.d/'
    repos = os.listdir(path)
    for repo in repos:
        path_file = path+'/'+repo
        if not os.path.isfile(path_file):
            continue
        if not re.search('repo$', repo):
            continue
        with open(path_file, 'r') as fsrc:
            content = fsrc.read()
            with open(path_file+'.disabled', 'w') as fdst:
                fdst.write(repo+'\n'+backup_comment+content)
                fdst.close()
            fsrc.close()
        os.remove(path_file)
    return None


def init_repo_file(baseurl):
    os_version_ret = platform.dist()
    version = os_version_ret[1].split('.', -1)
    repos_dir = '/etc/yum.repos.d/'
    kernel_310 = baseurl + '/kernel-3.10'
    if re.fullmatch('8', version[0]):
        appstream = baseurl+'/AppStream'
        baseos = baseurl+'/BaseOS'
        kernel_419 = baseurl+'/kernel419'
        kernel_510 = baseurl+'/kernel510'
        repostr_uos = '''[UniontechOS-AppStream]\nname = UniontechOS AppStream\nbaseurl = '''+appstream.strip('\n')+'''\nenabled = 1\ngpgcheck = 0\n\n[UniontechOS-BaseOS]\nname = UniontechOS BaseOS\nbaseurl = '''+baseos.strip('\n')+'''\nenabled = 1\ngpgcheck = 0\n\n[UniontechOS-kernel-4.19.0]\nname = UniontechOS Kernel-4.19.0\nbaseurl = '''+kernel_419.strip('\n')+'''\nenabled = 0\ngpgcheck = 0\nskip_if_unavailable = 1\n\n[UniontechOS-kernel-5.10.0]\nname = UniontechOS Kernel-5.10.0\nbaseurl = '''+kernel_510.strip('\n')+'''\nenabled = 0\ngpgcheck = 0\nskip_if_unavailable = 1\n\n
'''
    else:
        repostr_uos = '''[UniontechOS-AppStream]\nname = UniontechOS AppStream\nbaseurl = '''+baseurl.strip('\n')+'''\nenabled = 1\ngpgcheck = 0\n\n[UniontechOS-kernel-3.10.0]\nname = UniontechOS Kernel-3.10.0\nbaseurl = '''+kernel_310.strip('\n')+'''\nenabled = 0\ngpgcheck = 0\nskip_if_unavailable = 1\n
        '''
    repo_file = os.path.join(repos_dir, 'switch-to-uos.repo')
    with open(repo_file, 'w') as f_repo:
        f_repo.write(repostr_uos)
        f_repo.close()
    return None


def check_repo_makecache():
    os.system('yum clean all')
    os.system('yum makecache')
    os_version_ret = platform.dist()
    os_arch = platform.machine()
    version = os_version_ret[1].split('.', -1)
    ret = os.path.exists('/var/cache/dnf/UniontechOS-AppStream.solv')
    if ret:
        ret = os.path.exists('/var/cache/dnf/UniontechOS-BaseOS.solv')
        if ret or re.fullmatch('7', version[0]):
            return 0
        else:
            return 1
    else:
        if re.fullmatch('7', version[0]):
            ret = os.path.exists('/var/cache/yum/%s/7/UniontechOS-AppStream/repomd.xml' % os_arch)
            if ret:
                return 0
        return 1


def check_repo(data_j):
    uos_sysmig_conf = json.loads(get_sysmig_conf())
    agent_ip = json.loads(uos_sysmig_conf).get('agentip').strip()[1:-1]
    baseurl = json.loads(data_j).get('repo_pwd')
    init_remove_old_repo()
    init_repo_file(baseurl)
    state = check_repo_makecache()
    if state == 0:
        k_list = ['ip', 'res', 'data']
        v_list = [agent_ip, state, '连接成功']
    else:
        data = '下载失败，请检查您的软件源'
        k_list = ['ip', 'res', 'error']
        v_list = [agent_ip, state, data]
    return list_to_json(k_list, v_list)


def check_os_kernel(data):
    uos_sysmig_conf = json.loads(get_sysmig_conf())
    agent_ip = json.loads(uos_sysmig_conf).get('agentip').strip()[1:-1]
    platform_info = platform.platform()
    system_kernel_version = platform_info.split('-', -1)
    kernel_version = system_kernel_version[1]
    return list_to_json(['ip', 'data'], [agent_ip, kernel_version])


def check_repo_kernel(data):
    uos_sysmig_conf = json.loads(get_sysmig_conf())
    agent_ip = json.loads(uos_sysmig_conf).get('agentip').strip()[1:-1]
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
                kernel_version = kernel_version.split(' ', -1)
                kernel = kernel_version[len(kernel_version)-1]
                version_list.append(kernel.strip())
        cmd_419 = 'yum list kernel'
        ret = os.popen(cmd_419)
        for r in ret.readlines():
            if re.match('kernel', r) and re.search('uelc', r):
                kernel_version = re.sub('kernel-', '', r)
                kernel_version = re.sub('-.*$', '', kernel_version)
                kernel_version=kernel_version.split(' ', -1)
                kernel = kernel_version[len(kernel_version)-1]
                version_list.append(kernel.strip())
    else:
        version_list = ''
    k_list = ['ip', 'data']
    v_list = [agent_ip, version_list]
    return list_to_json(k_list, v_list)


def export_reports(data):
    """
    导出接口
    :param data:
    :return:
    """
    json_data = json.loads(data)
    hostname = socket.gethostname()
    uos_sysmig_conf = json.loads(get_sysmig_conf())
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


def system_check_requires(conflist):
    os.system('rpm --rebuilddb')
    cmd = ('rpm -qa|xargs -i rpm -V --nordev --nomode  --nomtime  --nogroup --nouser  --nosize '
           '--nofiledigest --nolinkto --noscripts --nofiles --nodigest {} >>') + PRE_MIG
    rets = os.popen(cmd)
    if rets:
        for ret in rets.readlines():
            conflist.append(ret)
        if len(conflist) > 1:
            return conflist
    return None


def fork_sh(cmd):
    try:
        f = open("/var/tmp/uos-migration/UOS_migration_log/err_log", 'a')
        subprocess.run(cmd, stderr=f, shell=True)
        message_state('2')
        f.close()
        return None
    except:
        return 0


def env():
    cmd = 'sh func/Abisystmcompchk.sh'
    t = Process(target=fork_sh, args=(cmd,))
    t.start()
    return None


def check_environment(data_j):
    uos_sysmig_conf = json.loads(get_sysmig_conf())
    agent_ip = json.loads(uos_sysmig_conf).get('agentip').strip()[1:-1]
    with open(pstate, 'r+') as fp:
        state = fp.readlines()
        fp.close()
        state = state[0]
    if re.match('0', state):
        message_state('1')
        system_check_requires([])
        env()
    if re.match('1', state):
        data = '1'
        k_list = ['ip', 'res', 'data']
        v_list = [agent_ip, '2', data]
        return list_to_json(k_list, v_list)
    elif re.match('2', state):
        abi_txt2xls()
        message_state('3')
    elif re.match('3', state) or re.match('9', state):
        data = '1'
        res = 0
        k_list = ['ip', 'res', 'data']
        v_list = [agent_ip, res, data]
        message_state('9')
        return list_to_json(k_list, v_list)
    data = '1'
    k_list = ['ip', 'res', 'data']
    v_list = [agent_ip, '2', data]
    return list_to_json(k_list, v_list)


def analysis_progress():
    path = '/var/tmp/uos-migration/data/uos/rpms'
    if os.path.exists(path):
        file_list = os.listdir(path)
    else:
        return None
    noan = oked = 1

    for file in file_list:
        path = re.sub('/$', "", path)
        cur_path = os.path.join(path, file)
        if os.path.isdir(cur_path):
            continue
        else:
            ret = file.split('.', -1)
            fret = ret[len(ret)-1]
            if re.fullmatch('rpm', fret):
                noan = noan + 1
            elif re.fullmatch('oked', fret):
                oked = oked + 1
    data = (oked/(noan+oked))*98
    data = format(data, '.1f')
    message_progress(str(data))
    return data


def check_progress(data):
    uos_sysmig_conf = json.loads(get_sysmig_conf())
    agent_ip = json.loads(uos_sysmig_conf).get('agentip').strip()[1:-1]

    with open(pstate, 'r+') as fp:
        state = fp.readlines()
        fp.close()
        state = state[0]
    if re.fullmatch('1', state):
        if not analysis_progress():
            message_progress('0')
        with open(progresslogdir, 'r+') as fpro:
            data = fpro.readlines()
            fpro.close()
    elif re.fullmatch('0', state):
        data = '0'
    elif re.fullmatch('2', state):
        data = '99'
    elif re.fullmatch('3', state):
        data = '100'
    else:
        data = '0'
    k_list = ['ip', 'progress']
    v_list = [agent_ip, data]
    return list_to_json(k_list, v_list)


def if_not_mig_kernel(kernel_version):
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
        kernel_patterns = ('exclude= kernel* kernel-tools python3-perf kernel-headers kernel-devel '
                           'bpftool perf kernel-core kmod-kvdo kpatch glibc-headers \n')
        with open('/etc/yum.conf', 'a+') as f:
            f.write(kernel_patterns)
            f.close()
    return None


def mig_kernel(kernel_version):
    cwd = '/var/tmp/uos-migration/kernel/'
    ret = os.listdir(cwd)
    for i in ret:
        os.unlink(cwd+i)
    cmd = 'rpm -qa | grep "kernel\|bpftool\|perf" |xargs -i rpm -q --qf "%{NAME}\\n" {}'
    if kernel_version == '0':
        return 0
    else:
        if re.fullmatch('4.18.0', kernel_version):
            repo = 'UniontechOS-kernel-'+kernel_version.strip()
        elif re.fullmatch('5.10.0', kernel_version):
            repo = 'UniontechOS-kernel-'+kernel_version.strip()
        else:
            return 1
        down_cmd = 'yumdownloader  --destdir "/var/tmp/uos-migration/kernel" --enablerepo '+repo
        ret = os.popen(cmd).readlines()
        for i in ret:
            download_pkg = down_cmd+' '+i.strip()+'-'+kernel_version.strip()
            os.system(download_pkg)

        cwd = '/var/tmp/uos-migration/kernel/'
        if os.listdir(cwd):
            os.system('rpm -Uvh "/var/tmp/uos-migration/kernel/*" --nodeps --oldpackage')
        else:
            if_not_mig_kernel()
            return 1


def mig_progress():
    with open(RPMS, 'r+') as fpro:
        data = fpro.read()
        fpro.close()
    return int(data)


def migration_details(data_j):
    uos_sysmig_conf = json.loads(get_sysmig_conf())
    agent_ip = json.loads(uos_sysmig_conf).get('agentip').strip()[1:-1]
    path = '/var/tmp/uos-migration/UOS_migration_log/mig_log.txt'
    if os.path.exists(path):
        with open(path, 'r') as lf:
           data = lf.read()
        lf.close()
    else:
        data = 'Init... ...'
    k_list = ['ip', 'data']
    v_list = [agent_ip, data]
    return list_to_json(k_list, v_list)


def readline_log():
    path = '/var/tmp/uos-migration/UOS_migration_log/mig_log.txt'
    if not os.path.exists(path):
        return 0
    else:
        with open(path, 'r') as rf:
            ln = len(rf.readlines())
            rf.close()
        return ln


def rpms_progress():
    percent = 99
    uelc_rpm = os.popen('rpm -qa|grep uelc20|wc -l').readlines()
    all_rpms = os.popen('rpm -qa|wc -l').readlines()
    rpms_progress = percent * (int(uelc_rpm[0].strip()) / int(all_rpms[0].strip()))
    rpms_progress = format(rpms_progress, '.1f')
    return rpms_progress


def mig_check_migration_progress():
    percent = 98
    rpms = mig_progress()
    lines = readline_log()
    lines = lines//4
    if lines >= rpms:
        lines = rpms
    data = percent*(lines/rpms)
    data = format(data, '.1f')
    message_progress(data)
    return None


def check_migration_progress(data_j):
    uos_sysmig_conf = json.loads(get_sysmig_conf())
    agent_ip = json.loads(uos_sysmig_conf).get('agentip').strip()[1:-1]
    with open(pstate, 'r+') as fp:
        state = fp.readlines()
        fp.close()
        state = state[0]
    if state == 'euler' or state == '20.03':
         with open(progresslogdir, 'r+') as fprogress:
             progress = fprogress.readlines()
         k_list = ['ip', 'progress']
         v_list = [agent_ip, progress]
         return list_to_json(k_list, v_list)

    if not analysis_progress():
        message_progress('0')

    if re.fullmatch('9', state):
        message_state('0')
    
    mig_check_migration_progress()
    with open(progresslogdir, 'r+') as fpro:
        data = fpro.readlines()
        fpro.close()

    k_list = ['ip', 'progress']
    v_list = [agent_ip, data]
    return list_to_json(k_list, v_list)


def start_sysmig(data_j):
    os_version_ret = platform.dist()
    version = os_version_ret[1].split('.', -1)
    agent_os = os_version_ret[0]+version[0]
    kernel_version = json.loads(data_j).get('kernel_version')
    if re.fullmatch('8', version[0]):
        cmd = 'python3 func/centos82uos.py'
        t = Process(target=run_cmd2file, args=(cmd,))
        t.start()
    elif re.search('centos7', agent_os):
        ex_kernel = ('sh func/centos72uos.sh -e "kernel-devel* kernel-headers* kernel-tools* kernel* '
                     'bpftool perf python-perf kernel-abi* kernel-modules kernel-core kmod-kvdo"')
        if kernel_version == '0':
            run_cmd2file(ex_kernel)
            message_state('3')
        elif kernel_version == '3.10.0':
            run_cmd2file(ex_kernel)
            cmd_k = 'sh func/kernel.sh -k 3.10.0'
            run_cmd2file(cmd_k)
            message_state('3')
        else:
            cmd = 'sh func/centos72uos.sh'
            run_cmd2file(cmd)
            message_state('3')
    return None


def mig_euler():
    cmd = "python3 /usr/lib/migration-tools-agent/ut-Migration-tools-0.1/centos7/openeuler/centos72openeuler.py"
    os.system(cmd)
    return None


def system_migration(data_j):
    uos_sysmig_conf = json.loads(get_sysmig_conf())
    agent_ip = json.loads(uos_sysmig_conf).get('agentip').strip()[1:-1]
    res = '0'
    kernel_version = json.loads(data_j).get('kernel_version')
    if kernel_version == 'euler':
        message_state('euler')
        t = Process(target=mig_euler)
        t.start()
    with open(pstate, 'r+') as fp:
        state = fp.readlines()
        fp.close()
    state = state[0]
    if re.match('0', state):
        message_state('1')
        if_not_mig_kernel(kernel_version)
        t = Process(target=start_sysmig, args=(data_j,))
        t.start()
    elif re.fullmatch('2', state):
        message_state('6')
        mig_kernel(kernel_version)
        with open(PRE_MIG, 'r') as fp:
            stros = fp.readlines()
            old_os = stros[0]
            fp.close()
        old_os = old_os.split(':', 1)
        main_conf(old_os[1]) 
        if os.path.exists('/var/tmp/uos-migration/data/exp-rst/systeminfo.txt'):
            run_cmd2file('sh func/Abitranrept.sh')
            abi_txt2xls_after_mig()
        message_state('4')
    elif re.fullmatch('4', state):
        message_state('5')
        if os.path.exists('/var/tmp/uos-migration/UOS_migration_log/rpms-verified-after.txt'):
            res = '0'
        else:
            res = '-1'
    elif re.fullmatch('3', state):
        message_state('5')
        if os.path.exists('/var/tmp/uos-migration/data/exp-rst/systeminfo.txt'):
            run_cmd2file('func/Abitranrept.sh')
            abi_txt2xls_after_mig()
        if os.path.exists('/var/tmp/uos-migration/UOS_migration_log/rpms-list-after.txt'):
            res = '0'
        else:
            res = '-1'
    elif re.fullmatch('5', state):
        if re.fullmatch('-1', res):
            data = '迁移失败。'
            k_list = ['ip', 'res', 'error']
            v_list = [agent_ip, res, data]
            return list_to_json(k_list, v_list)
        else:
            data = '迁移成功。'
        k_list = ['ip', 'res', 'data']
        v_list = [agent_ip, res, data]
        return list_to_json(k_list, v_list)
    
    res = '2'
    data = '......'
    k_list = ['ip', 'res', 'data']
    v_list = [agent_ip, res, data]
    return list_to_json(k_list, v_list)
