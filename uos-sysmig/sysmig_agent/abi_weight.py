# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier:   MulanPubL-2.0-or-later

import os

# ABI_INCOMPAT_PATH = '/home/xzx/nfs/abi-incompat-pkg.txt'
# ABI_COMPAT_PATH = '/home/xzx/nfs/abi-compat-pkg.txt'
pwd = '/root/nfs'
ABI_INCOMPAT_PATH = pwd+'/abi-incompat-pkg.txt'
ABI_COMPAT_PATH = pwd + '/abi-compat-pkg.txt'
AppStream =pwd + '/uos-sysmig/ut-Migration-tools/sysmig_agent/AppStream.txt'
BaseOS = pwd + '/uos-sysmig/ut-Migration-tools/sysmig_agent/txts/BaseOS.txt'


def get_list_pkg(path):
    with open(path, 'r') as ap:
        rpm = ap.readlines()
        ap.close()
    return rpm
#

# 调用
def get_abi_incompat_pkg():
    query = []
    rpms = get_list_pkg(ABI_INCOMPAT_PATH)
    for i in range(len(rpms)):
        rpm = rpms[i].split('|', -1)
        if len(query) > 0:
            for q in range(len(query)):
                if str(rpm[0]).strip() == str(query[q]):
                    break
                if q == len(query) - 1:
                    query.append(rpm[0])
        else:
            query.append(rpm[0])
    return query


def return_error(debuginfo):
    #####logging debug info
    print(debuginfo)


# 传入txt和rpm队列返回匹配个数
def match_rpm(txt_path, rpm_query):
    with open(txt_path, 'r') as ap:
        appstream_rpms = ap.readlines()
        ap.close()
    total_rpm = 0
    q = []
    for i in range(len(rpm_query)):
        for n in range(len(appstream_rpms)):
            if str(rpm_query[i].strip().strip('\n')) == str(appstream_rpms[n].strip().strip('\n')):
                total_rpm = total_rpm + 1
                q.append(rpm_query[i])
                break
            if n == (len(appstream_rpms)):
                print('No compat with AppStream and BaseOS list : ' + rpm_query[i])
    return total_rpm


def rpm_priority(rpm_compat_query, rpm_incompat_query):
    app_weight = 50
    base_weight = 50
    if not os.path.exists(AppStream) and os.path.exists(BaseOS):
        return return_error('debuginfo:can not open this file...')
    total_incompat_app = match_rpm(AppStream, rpm_incompat_query)
    total_incompat_base = match_rpm(BaseOS, rpm_incompat_query)
    total_compat_app = match_rpm(AppStream, rpm_compat_query)
    total_compat_base = match_rpm(BaseOS, rpm_compat_query)
    app_weight_percent = (total_compat_app / (total_incompat_app + total_compat_app)) * app_weight
    base_weight_percent = (total_compat_base / (total_incompat_base + total_compat_base)) * base_weight
    AllWeight = app_weight_percent + base_weight_percent
    AllWeight = format(AllWeight, '.0f')
    return AllWeight


def first_high_weight(rpm_incompat_query):
    riq = ['gcc', 'glibc', 'binutils']
    for i in range(len(riq)):
        for n in range(len(rpm_incompat_query)):
            if riq[i] == rpm_incompat_query[n]:
                return False
    return True


def abi_check_priority():
    rpm_incompat_query = get_abi_incompat_pkg()
    rpm_compat_query = get_list_pkg(ABI_COMPAT_PATH)
    del rpm_incompat_query[:2]
    del rpm_compat_query[0]
    if first_high_weight(rpm_incompat_query):
        AllWeight = rpm_priority(rpm_compat_query, rpm_incompat_query)
    else:
        AllWeight = 0
    print(AllWeight)

