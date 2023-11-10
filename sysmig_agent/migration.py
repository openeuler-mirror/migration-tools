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
