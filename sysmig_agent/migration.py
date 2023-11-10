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

