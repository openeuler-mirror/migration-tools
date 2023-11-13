# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier:   MulanPubL-2.0-or-later


import queue,os,string
import threading,codecs
import time,rpm,stat,re
import datetime
import platform
import json,xlrd,xlwt
import socket
from xlutils.copy import copy
from shutil import copyfile
#from sysmig_agent.share import *
from multiprocessing import Process
from multiprocessing import cpu_count

from logger import *
#from connect_sql import DBHelper

workQueue = queue.Queue()
queueLock = threading.Lock()

#为便于测试将变量、接口从share.py中拷贝到当前文件，待联调通过后删除即可
######################## add for test start ########################
local_dir = '/var/tmp/uos-migration/data/'
exp_rst_dir = local_dir+'exp-rst/'

current_system_unique = exp_rst_dir + 'current-system-unique.csv'
migration_system_install = exp_rst_dir + 'migration-system-install.csv'
migration_system_total = exp_rst_dir + 'migration-system-total.csv'
abi_comp_chk = exp_rst_dir + 'abi-comp-chk.csv'
abi_incomp_chk = exp_rst_dir + 'abi-incomp-chk.csv'
exitFlag = 0
total_rpm_nums = 0
percentage = ''
deal_rpm_num = 0
agent_abi_check_result = exp_rst_dir + 'agent_ABI_check_result.csv'
suffix_list = ['.mo', '.gz', '.xml', '.conf', '.png', '.page', '.woff', '.ttf', '.pyc', '.typelib', '.pdf', '.ppt', '.txt', '.ico', '.icc', '.tcc', '.gif', '.oga', '.rom', '.jpg', '.dict', '.webm', '.pyc', '.wav', '.ucode', '.ttc', '.gresource', '.otf', '.t1', '.db', '.elc', '.cache', '.fd', '.iso', '.efi', '.mmdb', '.bz2', '.img', '.bin', '.fw', '.cis', '.itb', '.inp', '.sbcf', '.ddc', '.sfi', '.bseq', '.mfa2', '.chk', '.mgc', '.stub', '.dfu', '.dat', '.sys', '.bts', '.dlmem', '.brd', '.hwm', '.pwd', '.pwi', '.exe', '.der', '.p12', '.ogg', '.signed', '.dafsa', '.gpg', '.tri', '.x86_64']

#Queue = queue.Queue()

def os_storage():
    """
    判断系统剩余空间大小
    :return: GB
    """
    path = '/var/cache'
    stat = os.statvfs(path)
    CACHE_SPACE = 10.0
    state = 1
    ava_cache = format(stat.f_bavail * stat.f_frsize / 1024 // 1024 / 1024, '.1f')
    if stat:
        # with open(PRE_MIG,'a+') as pf:
        #     pf.write('/var/cache可用空间为'+ava_cache+'GB')
        #     pf.close()
        if float(ava_cache) >= CACHE_SPACE:
            state = 0
            return ava_cache
            # data = '可用空间为'+ava_cache+'GB'
        else:
            return ava_cache
            # data = '可用空间为' + ava_cache + 'GB,请清理/var/cache的空间后重试。'
    else:
        return ava_cache
        # data = '可用空间为'+ava_cache+'GB,请清理/var/cache的空间后重试。'
        # return list_to_json(keylist,valuelist)

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        return ip
    finally:
        s.close()

def abi_check_sys_type():
    path = '/etc/os-version'
    if os.path.exists(path):
        with open(path,'r') as v:
            ret = v.readlines()
            localos=ostype=''
            for i in range(len(ret)):
                if not ret[i]:
                    continue
                if 'MinorVersion' in ret[i]:
                    strminor = str(ret[i])
                    _, localos = strminor.split('=',1)
                if 'EditionName[zh_CN]' in ret[i]:
                    strminor = str(ret[i])
                    _, ostype = strminor.split('=',1)
                    ostype = re.sub('[^a-zA-Z]+','',ostype)
            localos = localos.strip().strip('\n') + ostype.strip().strip('\n')
            #localos = new_os.format(localos.strip().strip('\n'))
            return localos

def abi_check_sys():
    c8 = ['1020a', '1021a', '1050a']
    c7 = ['1000c', '1001c', '1002a']
    system_type = abi_check_sys_type()
    if not system_type:
        os_version_ret = platform.dist()
        osname = os_version_ret[1].strip()
        osn = osname.split('.',-1)[0]
        return osn.strip('\n')
    for i in range(len(c8)):
        if c8[i] in system_type:
            return 8
    for i in range(len(c7)):
        if  c7[i] in system_type:
            return 7
    return None

######################## add for test end ########################
######################## add for test end ########################