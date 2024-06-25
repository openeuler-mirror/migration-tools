# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier:   MulanPubL-2.0-or-later

import os
from sysmig_agent.config import *

# ABI_INCOMPAT_PATH = '/home/xzx/nfs/abi-incompat-pkg.txt'
# ABI_COMPAT_PATH = '/home/xzx/nfs/abi-compat-pkg.txt'
pwd = '/root/nfs'
if not os.path.exists(pwd):
    pwd = '/home/xzx/nfs'


def get_list_pkg(path):
    with open(path, 'r') as ap:
        rpm = ap.readlines()
        ap.close()
    return rpm


# 调用
def get_abi_incompat_pkg(path):
    query = []
    rpms = get_list_pkg(path)
    #ignore_abi = get_list_pkg(ignore_abi_check_8)
    for i in range(len(rpms)):
        rpm = rpms[i].split(',', -1)
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

    #app_weight_percent = (total_compat_app / (total_incompat_app + total_compat_app)) * app_weight
    #base_weight_percent = (total_compat_base / (total_incompat_base + total_compat_base)) * base_weight
    #AllWeight = app_weight_percent + base_weight_percent
    #AllWeight = format(AllWeight, '.0f')
    #return AllWeight


def first_high_weight(rpm_incompat_query):
    riq = ['gcc', 'glibc', 'binutils']
    for i in range(len(riq)):
        for n in range(len(rpm_incompat_query)):
            if riq[i] == rpm_incompat_query[n]:
                return False
    return True


def abi_check_priority():
    rpm_incompat_query = get_abi_incompat_pkg(ABI_INCOMPAT_PATH)
    rpm_compat_query = get_list_pkg(ABI_COMPAT_PATH)
    del rpm_incompat_query[:2]
    del rpm_compat_query[0]
    if first_high_weight(rpm_incompat_query):
        AllWeight = rpm_priority(rpm_compat_query, rpm_incompat_query)
    else:
        AllWeight = 0
    print(AllWeight)


class LayeredGrading(object):
    layered = [50, 50]
    layered_file = [AppStream, BaseOS]

    def __init__(self):
        self.rpm_incompat_query = ''
        self.rpm_compat_query = ''
        self.compatibility = 0

    def get_data(self):
        self.rpm_incompat_query = get_abi_incompat_pkg(ABI_INCOMPAT_PATH)
        # self.rpm_compat_query = get_list_pkg(ABI_COMPAT_PATH)
        self.rpm_compat_query = get_abi_incompat_pkg(ABI_COMPAT_PATH)

    def run(self):
        self.get_data()
        tmp_incompat = tmp_compat = 0
        for i in range(len(self.layered)):
            tmp_incompat = match_rpm(self.layered_file[i], self.rpm_incompat_query)
            tmp_compat = match_rpm(self.layered_file[i], self.rpm_compat_query)
            self.compatibility =  (tmp_compat / (tmp_incompat + tmp_compat)) * self.layered[i]
            if first_high_weight(self.rpm_incompat_query):
                self.compatibility += self.compatibility
        return format(self.compatibility, '.0f')


layered_Grading = LayeredGrading()
# layered_Grading.run()
