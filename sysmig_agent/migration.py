# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier:   MulanPubL-2.0-or-later

from sysmig_agent.centos82uos import *

#sys.path.append("..")
from connect_sql import DBHelper

RPMS = '/var/tmp/uos-migration/.rpms'

# migrations function

# migrations progress
# 迁移进度

def mig_whether_success():
    # rpms = int(migprogress())
    cmdrpm = 'rpm -qa | wc -l'
    cmduelc = 'rpm -qa | grep oe1|wc -l'
    rpms = int(os.popen(cmdrpm).readlines()[0])
    ret = int(os.popen(cmduelc).readlines()[0])
    res = (ret / rpms)*100
    res = format(res, '.0f')
    return int(res)


def migprogress():
    with open(RPMS, 'r+') as fpro:
        data = fpro.read()
        fpro.close()
    return int(data)


def readline_log():
    path = '/var/tmp/uos-migration/UOS_migration_log/mig_log.txt'
    if not os.path.exists(path):
        return None
    else:
        ln = 0
        with open(path, 'r') as rf:
            for line in rf:
                ln = ln + 1
            rf.close()
        return ln


def migInit_porgress():
    uelc_rpm = os.popen('rpm -qa|wc -l').readlines()
    with open('/var/tmp/uos-migration/.rpms', 'w+') as fp:
        fp.write(uelc_rpm[0])
        fp.close()


# check_migration_progress
def mig_check_migration_progress():
    percent = 98
    rpms = migprogress()
    lines = readline_log()
    if not lines:
        return 0
    lines = lines // 6
    if lines >= rpms:
        lines = rpms
    data = percent * (lines / rpms)
    data = format(data, '.1f')
    return data



def up_to_date_sql_migrate():
    data = mig_check_migration_progress()
    sql_show_tables()
    sql = "UPDATE agent_task SET task_progress = {} ,task_Updatetime = NOW() WHERE agent_ip = '{}';".format(data, get_local_ip())
    try:
        ret = DBHelper().execute(sql)
    except:
        pass
    return 0


def Sysmig(kernel_version):
    os_version_ret = platform.dist()
    version = os_version_ret[1].split('.',-1)
    AGENT_OS = os_version_ret[0]+version[0]
    data = state =0
    if re.fullmatch('8',version[0]):
        cmd = 'python3 func/centos82uos.py'
        run_cmd2file(cmd)
        # t = Process(target=run_cmd2file, args=(cmd,))
        # t.start()
    elif re.search('centos7',AGENT_OS):
        ex_kernel = 'sh func/centos72uos.sh -e "kernel-devel* kernel-headers* kernel-tools* kernel* bpftool perf python-perf kernel-abi* kernel-modules kernel-core kmod-kvdo"'
        if kernel_version == '0':
            run_cmd2file(ex_kernel)
            sql_mig_statue('3')
        elif kernel_version == '3.10.0':
            run_cmd2file(ex_kernel)
            cmd_k = 'sh func/kernel.sh -k 3.10.0'
            run_cmd2file(cmd_k)
            sql_mig_statue('3')
        else:
            cmd = 'sh func/centos72uos.sh'
            run_cmd2file(cmd)
            sql_mig_statue('3')


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
    if kernel_version == '0' or kernel_version == '3.10.0':
        kernel_patterns = 'exclude= kernel* kernel-tools python3-perf kernel-headers kernel-devel bpftool perf kernel-core kmod-kvdo kpatch glibc-headers \n'
        with open('/etc/yum.conf', 'a+') as f:
            f.write(kernel_patterns)
            f.close()

def disable_exclude():
    with open('/etc/yum.conf', 'r') as f:
        content = f.read()
        f.close()
    if re.search(r'^exclude=', content, re.MULTILINE):
        content = re.sub(r"\n(exclude=)", r"\n#\1", content)
        #content = re.sub(r"\nexclude=", r"\n#exclude=", content)
    with open('/etc/yum.conf','w+') as f:
        f.write(content)
        f.close()


# migration kernel
def mig_kernel(kernel_version):
    disable_exclude()
    cwd = '/var/tmp/uos-migration/kernel/'
    if not os.path.exists(cwd):
        os.mkdir(cwd)
    ret = os.listdir(cwd)
    for i in ret:
        os.unlink(cwd+i)
    cmd = ' rpm -qa | grep "kernel\|bpftool\|perf" |xargs -i rpm -q --qf "%{NAME}\\n" {}'
    if '0' == kernel_version:
        return None
    else:
        repo = ''
        if '4.18.0' == kernel_version:
            repo = 'UniontechOS-kernel-'+kernel_version.strip()
        elif '5.10.0' == kernel_version:
            repo = 'UniontechOS-kernel-'+kernel_version.strip()
        elif '3.10.0' == kernel_version:
            repo = 'UniontechOS-kernel-' + kernel_version.strip()
        else:
            return 1
        down_cmd = 'yumdownloader  --destdir "/var/tmp/uos-migration/kernel" --enablerepo '+repo
        ret = os.popen(cmd).readlines()
        for i in ret:
            downpackage = down_cmd+' '+i.strip()+'-'+kernel_version.strip()
            # os.system(downpackage)
            run_subprocess(downpackage)

        cwd = '/var/tmp/uos-migration/kernel/'
        if os.listdir(cwd):
            cmd = 'rpm -Uvh "{}*" --nodeps --oldpackage'.format(cwd)
            # os.system(cmd)
            run_subprocess(cmd)
        else:
            # loggen.debug('Can not download kernel .')
            #log.err
            return 1


def init_log_dir():
    if not os.path.isdir(PRE_MIG_DIR):
        os.makedirs(PRE_MIG_DIR)
    if not os.path.isdir(MIGRATION_KERNEL):
        os.makedirs(MIGRATION_KERNEL)
    if not os.path.isdir(MIGRATION_DIR):
        os.makedirs(MIGRATION_DIR)
    if not os.path.isdir(MIGRATION_DATA_RPMS_DIR):
        os.makedirs(MIGRATION_DATA_RPMS_DIR)
    if not os.path.exists(PROGRESS):
        with open(PROGRESS,'w+') as fp:
            fp.write(' ')
            fp.close()
    if not os.path.exists(MIGRATION_DATA_RPMS_3_INFO):
        with open(MIGRATION_DATA_RPMS_3_INFO,'w+') as fp:
            fp.write(' ')
            fp.close()
    if not os.path.exists(MIGRATION_LOG):
        with open(MIGRATION_LOG,'w+') as fp:
            fp.write(' ')
            fp.close()
    if not os.path.exists(PRE_MIG):
        with open(PRE_MIG,'w+') as fp:
            fp.write(' ')
            fp.close()
    migInit_porgress()


def get_mig_state(task_id):
    sql = "SELECT task_data FROM agent_task WHERE task_id = {} ;".format(task_id)
    ret_sql_msg_info = DBHelper().execute(sql)
    try:
        state = ret_sql_msg_info.fetchall()[0][0]
        if len(state):
            return str(state)
    except:
        return None


def get_old_osnameversion():
    sql = "SELECT agent_os FROM agent_info WHERE agent_ip = '{}' ;".format(get_local_ip())
    ret_sql_msg_info = DBHelper().execute(sql)
    try:
        state = ret_sql_msg_info.fetchall()[0][0]
        if len(state):
            return str(state)
    except:
        return None


def get_old_osname():
    nv = get_old_osnameversion()
    oldosname = re.sub(r'[0-9]', '', nv)
    return oldosname


def get_old_osversion():
    nv = get_old_osnameversion()
    oldosversion = re.sub(r'[A-Z,a-z]', '', nv)
    return oldosversion



def mig_system_migration(kernel_version):
    res = '0'
    #state = str(get_mig_state())
    state = 0
    print('-GET MIG STATE-'+state)
    if '0' == state:
        sql_mig_statue('1')
        ifnot_mig_kernel(kernel_version)
        # t = Process(target=Sysmig, args=(kernel_version,))
        # t.start()
        Sysmig(kernel_version)
    elif '2' == state:
        sql_mig_statue('6')
        mig_kernel(kernel_version)
        with open(PRE_MIG, 'r') as fp:
            stros = fp.readlines()
            oldos = stros[0]
            fp.close()
        oldos = oldos.split(':',1)
        main_conf(oldos[1])
        if os.path.exists('/var/tmp/uos-migration/data/exp-rst/systeminfo.txt'):
            run_cmd2file('sh func/Abitranrept.sh')
            # abi_txt2xls_trans()
        sql_mig_statue('4')
    elif '4' == state:
        sql_mig_statue('5')
        if os.path.exists('/var/tmp/uos-migration/UOS_migration_log/rpms-verified-after.txt'):
            res = '0'
        else:
            res = '-1'
    elif '3' == state:
        sql_mig_statue('5')
        if os.path.exists('/var/tmp/uos-migration/data/exp-rst/systeminfo.txt'):
            run_cmd2file('func/Abitranrept.sh')
            # abi_txt2xls_trans()
        if os.path.exists('/var/tmp/uos-migration/UOS_migration_log/rpms-list-after.txt'):
            res = '0'
        else:
            res = '-1'
    elif '5' == state:
        if '-1' == res :
            data =' 迁移失败。'
            keylist = ['ip','res','error']
            return 3
        else:
            data = '迁移成功。'
        return 2
    return 1


