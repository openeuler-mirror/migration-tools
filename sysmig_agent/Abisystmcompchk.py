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

#20220107 add by lihp
#20220112 modify by lihp: add deal kernel migration fail
def platform_release(Flag):
    if Flag == '0':
        cmd = "rpm -qa | grep kernel | grep -E 'an7|an8|el7|el8'"
    else:
        cmd = "rpm -qa | grep kernel | grep -E 'el7|el8|an7|an8|uelc'"
    kernel_version=''
    for line in os.popen(cmd):
        pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
        if pattern.match(line[7]):
            kernel_version = line.split('-',1)[1]
            if 'uelc' in line:
                break
            elif 'oe1' in line:
                break
    return kernel_version.rsplit('.', 1)[0]


#Create agent ABI check result file
def agent_ABI_check_result():
    string = ',,,Y,,\n'

    #mycopyfile(abi_incomp_chk, agent_abi_check_result, abi_log)
    facp = open(agent_abi_check_result, 'w')
    for line in open(abi_incomp_chk):

        tmp01 = line.split(',', 5)
        tmp = tmp01[4]

        if tmp == '库差异':
            str_01 = tmp01[0]+','+tmp01[1]+','+tmp01[2]+','+tmp01[3]+',1,'+tmp01[5]
        elif tmp == '二进制差异':
            str_01 = tmp01[0]+','+tmp01[1]+','+tmp01[2]+','+tmp01[3]+',2,'+tmp01[5]
        elif tmp == '可执行文件差异':
            str_01 = tmp01[0]+','+tmp01[1]+','+tmp01[2]+','+tmp01[3]+',3,'+tmp01[5]
        elif tmp == '视频文件差异':
            str_01 = tmp01[0]+','+tmp01[1]+','+tmp01[2]+','+tmp01[3]+',4,'+tmp01[5]

        facp.write(str_01)
    facp.close()

    fp = open(agent_abi_check_result, 'a')
    for rpm_name in open(abi_comp_chk):
        fp.write(rpm_name.split(',')[0] + string)
    fp.close()


def logger_init():
    log_file = 'Abisystmcompchk.log' + '.' + datetime.datetime.now().strftime('%Y%m%d%H%M')
    log_path = '/var/tmp/uos-migration/UOS_migration_log/'
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    log_name = log_path + log_file
    logfile = log_name
    fh = logging.FileHandler(logfile, mode='w')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger


# Check whether it is an ELF file
def is_ELFfile(filepath, logger):
    if not os.path.exists(filepath):
        logger.info('file not exit:' + filepath)
        return False
    try:
        FileStates = os.stat(filepath)
        FileMode = FileStates[stat.ST_MODE]
        if not stat.S_ISREG(FileMode) or stat.S_ISLNK(FileMode):
            return False
        with open(filepath, 'rb') as f:
            header = (bytearray(f.read(4)[1:4])).decode(encoding="utf-8")
            # logger.info("header is {}".format(header))
            if header in ["ELF"]:
                return True
    except UnicodeDecodeError as e:
        # logger.info("is_ELFfile UnicodeDecodeError {}".format(filepath))
        # logger.info(str(e))
        pass
    return False
