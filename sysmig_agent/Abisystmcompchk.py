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


#Get migration behind rpm list, filter dist of '.uelc20'
def get_migrate_behind_rpm_pkg():
    dist='.uelc20'
    migration_before_uelc20_rpm = exp_rst_dir + 'migration-before-uelc20-rpm.csv'
    migration_behind_uelc20_rpm = exp_rst_dir + 'migration-behind-uelc20-rpm.csv'

    rpm_pkg_list=[]

    ts = rpm.TransactionSet()
    mi = ts.dbMatch()

    fhu = open(migration_behind_uelc20_rpm, 'w')
    if system_version_id() == '7':
        for rpm_pkg in mi:
            if dist in rpm_pkg['release'].decode():
                fhu.write(rpm_pkg['name'].decode()+'\n')
                rpm_pkg_list.append(rpm_pkg['name'].decode())
    else:
        for rpm_pkg in mi:
            if dist in rpm_pkg['release']:
                fhu.write(rpm_pkg['name']+'\n')
                rpm_pkg_list.append(rpm_pkg['name'])
    fcw.close()

    return rpm_pkg_list


# Get the current system package
def get_system_pkg_name(flag, mig_logger):
    dist = '.uelc20'
    rpm_pkg_list = ''
    rpm_pkg_oth = []

    if not os.path.exists(exp_rst_dir):
        os.makedirs(exp_rst_dir)

    migration_before_uelc20_rpm = exp_rst_dir + 'migration-before-uelc20-rpm.csv'
    migration_before_eln_rpm = exp_rst_dir + 'migration-before-eln-rpm.csv'

    ts = rpm.TransactionSet()
    mi = ts.dbMatch()

    # migration before filter dist of '.uelc20'
    if flag == '0':
        if os.path.exists(migration_before_uelc20_rpm):
            os.remove(migration_before_uelc20_rpm)
        if os.path.exists(migration_before_eln_rpm):
            os.remove(migration_before_eln_rpm)

        fbfu = open(migration_before_uelc20_rpm, 'w')
        fbfe = open(migration_before_eln_rpm, 'w')
        if system_version_id() == '7':
            for rpm_pkg in mi:
                if dist in rpm_pkg['release'].decode():
                    fbfu.write(rpm_pkg['name'].decode() + '\n')
                else:
                    fbfe.write(rpm_pkg['name'].decode() + '\n')
                    rpm_pkg_list = rpm_pkg_list + ' ' + rpm_pkg['name'].decode()
        else:
            for rpm_pkg in mi:
                if dist in rpm_pkg['release']:
                    fbfu.write(rpm_pkg['name'] + '\n')
                else:
                    fbfe.write(rpm_pkg['name'] + '\n')
                    rpm_pkg_list = rpm_pkg_list + ' ' + rpm_pkg['name']
        fbfu.close()
        fbfe.close()
        return rpm_pkg_list

    # migration behind filter dist of '.uelc20'
    elif flag == '1':
        if os.path.exists(migration_before_uelc20_rpm):
            with open(migration_before_uelc20_rpm, 'r') as fbfu:
                fbfu_list = fbfu.readlines()

            if os.path.exists(migration_system_install):
                os.remove(migration_system_install)

            fbhe = open(migration_system_install, 'w')
            rst = str(abi_check_sys())
            if rst == '7':
                for rpm_pkg in mi:
                    if dist in rpm_pkg['release'].decode():
                        if rpm_pkg['name'].decode() not in fbfu_list:
                            fbhe.write(rpm_pkg['name'].decode() + '\n')
            elif rst == '8':
                for rpm_pkg in mi:
                    if dist in rpm_pkg['release']:
                        if rpm_pkg['name'] not in fbfu_list:
                            fbhe.write(rpm_pkg['name'] + '\n')
            else:
                mig_logger.info('migrate behind not exit verison id  !!!')
            fbhe.close()
        else:
            mig_logger.info('file not exit:' + migration_before_uelc20_rpm)
            mig_logger.info('Please do migration before system compation check !!!')
            return False
        return True

    elif flag == '2':
        if system_version_id() == '7':
            for rpm_name in mi:
                if dist not in rpm_name['release'].decode():
                    rpm_pkg_oth.append(rpm_name['name'].decode())
                    dist_flag = '1'
        else:
            for rpm_name in mi:
                if dist not in rpm_name['release']:
                    rpm_pkg_oth.append(rpm_name['name'])
                    dist_flag = '1'

        if dist_flag == '1':
            return rpm_pkg_oth
        else:
            mig_logger.info('The current system is UOS, not support migration, please check !!!')
            return False



class myThread (threading.Thread):
    def __init__(self, threadID, name, q, lock, fpw, fpr, q_query, log):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
        self.lock = lock
        self.fpw = fpw
        self.fpr = fpr
        self.q_query = q_query
        self.log = log
    def run(self):
        self.log.info ("Open the thread" + self.name)
        process_data(self.name, self.q, self.lock, self.fpw, self.fpr, self.q_query, self.log)
        self.log.info ("Exit the thread" + self.name)

def is_binwary_file(filename):
    TEXT_BOMS = {
        codecs.BOM_UTF16_BE,
        codecs.BOM_UTF16_LE,
        codecs.BOM_UTF32_BE,
        codecs.BOM_UTF32_LE,
        codecs.BOM_UTF8,
            }
    with open(filename, 'rb') as file:
        CHUNKSIZE = 8192
        initial_bytes = file.read(CHUNKSIZE)
        file.close
    return not any(initial_bytes.startswith(bom) for bom in TEXT_BOMS) and b'\0' in initial_bytes

def incomp_binwary_desc(binwary_file):
    if binwary_file.endswith('.so'):
        incomp_info_desc = '库差异'
    elif binwary_file.endswith('.exec'):
        incomp_info_desc = '可执行文件'
    elif binwary_file.endswith('.mod'):
        incomp_info_desc = '视频文件'
    else:
        incomp_info_desc = '二进制差异'
    return incomp_info_desc

def deal_files_list(fwincomp, fwcomp, cur_file_list, trn_file_list, rpm_full_pkg_name, list_log):
    #compatiable
    comp_flag=1
    link_flag = '0'
    cur_file_deal = ''

    rpm_pkg_dir = local_dir + 'uos/rpms'
    rpm_pkg_name = rpm_full_pkg_name.rsplit('-',2)[0]
    pkg_version = rpm_full_pkg_name.rsplit('-',2)[1]

    for cur_file_name in cur_file_list:

        cur_file_binwary = cur_file_name.strip('\n')

        if not os.path.exists(cur_file_binwary):
            continue

        if os.path.isdir(cur_file_binwary):
            continue

        if '.' in cur_file_binwary.rsplit('/',1)[1]:
            if '.'+cur_file_binwary.rsplit('.',1)[1] in suffix_list:
                continue

        if not is_ELFfile(cur_file_binwary, list_log):
            continue

        if is_binwary_file(cur_file_binwary):
            trn_file_deal = rpm_pkg_dir + cur_file_binwary
            if not os.path.exists(trn_file_deal):
                continue

            #link file realpath
            if os.path.islink(cur_file_binwary):
                cur_file_deal = os.path.realpath(cur_file_binwary)
                if cur_file_name in trn_file_list:
                    trn_file_deal_tmp = rpm_pkg_dir + cur_file_binwary
                    trn_file_deal = os.path.realpath(trn_file_deal_tmp)
                    link_flag = '1'
                else:
                    continue
            else:
                if link_flag:
                    link_flag = '0'
                    continue
                if cur_file_name in trn_file_list:
                    trn_file_deal = rpm_pkg_dir + cur_file_binwary
                    cur_file_deal = cur_file_binwary
                else:
                    continue

            abidiff_rst_list = list(os.popen('abidiff  %s %s' %(trn_file_deal, cur_file_binwary)))
            if len(abidiff_rst_list):
                i = 0
                if cur_file_binwary.endswith('.exec'):
                    while i < 2:
                        for line in abidiff_rst_list[i].split(':',1)[1].split(','):
                            if line.split(' ', 2)[1] != '0':
                                bin_name = cur_file_name.strip('\n').rsplit('/', 1)[1]
                                compatiablity='N'
                                incomp_reason = incomp_binwary_desc(bin_name)
                                diff_detail = abidiff_rst_list[i].split(':', 1)[1]
                                fwincomp.write(rpm_pkg_name+','+bin_name+','+pkg_version+','+compatiablity+','+incomp_reason+','+diff_detail)
                                comp_flag = 0
                        i = i + 1
                #20220112 lihp: add if branch
                elif abidiff_rst_list[0].startswith('ELF SONAME'):
                    i = i + 1
                    while i < 2:
                        for line in abidiff_rst_list[i].split(':',1)[1].split(','):
                            if line.split(' ', 2)[1] != '0':
                                bin_name = cur_file_name.strip('\n').rsplit('/', 1)[1]
                                compatiablity='N'
                                incomp_reason = incomp_binwary_desc(bin_name)
                                diff_detail = abidiff_rst_list[i].split(':', 1)[1]
                                fwincomp.write(rpm_pkg_name+','+bin_name+','+pkg_version+','+compatiablity+','+incomp_reason+','+diff_detail)
                                comp_flag = 0
                        i = i + 1
                else:
                    while i < 4:
                        for line in abidiff_rst_list[i].split(':',1)[1].split(','):
                            if line.split(' ', 2)[1] != '0':
                                bin_name = cur_file_name.strip('\n').rsplit('/', 1)[1]
                                compatiablity='N'
                                incomp_reason = incomp_binwary_desc(bin_name)
                                diff_detail = abidiff_rst_list[i].split(':', 1)[1]
                                fwincomp.write(rpm_pkg_name+','+bin_name+','+pkg_version+','+compatiablity+','+incomp_reason+','+diff_detail)
                                comp_flag = 0
                        i = i + 1
            else:
                continue
    if comp_flag:
        fwcomp.write(rpm_pkg_name + ',' + ',' + ',' + 'Y,' + ',' + '\n')


def process_data(threadName, q, queueLock, incompfw, compfw, Queue, pro_log):
    global exitFlag
    global total_rpm_nums
    global percentage
    global deal_rpm_num
    status = '1'

    rpm_pkg_path = local_dir + 'uos/rpms/'

    abisys =str(abi_check_sys())
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            rpm_full_name=q.get()
            rpm_pkg_name=rpm_full_name.rsplit('-',2)[0]
            rpm_path_name=rpm_pkg_path + rpm_full_name
            if '7' == abisys:
                print('----------7-0---------')
                list_file_cur=list(os.popen('rpm -ql  %s ' %(rpm_pkg_name)))
                list_file_trn=list(os.popen('rpm -qpl  %s ' %(rpm_path_name)))
            else:
                list_file_cur=list(os.popen('rpm -ql --noartifact  %s ' %(rpm_pkg_name)))
                list_file_trn=list(os.popen('rpm -qpl --noartifact  %s ' %(rpm_path_name)))
            os.system('rpm2cpio %s | cpio -idmv' %(rpm_full_name))
            deal_files_list(incompfw, compfw, list_file_cur, list_file_trn, rpm_full_name, pro_log)
            deal_rpm_num = deal_rpm_num + 1
            percentage = ("%d" % (deal_rpm_num/total_rpm_nums*100))
            msg_tup = (percentage, status)
            Queue.put(msg_tup)
            pro_log.info('message tup queue:' + str(msg_tup))
            queueLock.release()
        else:
            queueLock.release()


def get_system_pkg_list(migbeflist):
    download_rpm_nums = 0
    migration_rpm_pkg_path = local_dir + 'uos/rpms'

    #clean history data
    if os.path.exists(migration_system_total):
        os.remove(migration_system_total)

    ftw = open(migration_system_total, 'w')
    items = os.listdir(migration_rpm_pkg_path)
    newlist = []
    for names in items:
        if names.endswith(".rpm"):
            ftw.write(names.rsplit('-',1)[0].rsplit('-',1)[0] + '\n')
            migbeflist.append(names.rsplit('-',1)[0].rsplit('-',1)[0])
            newlist.append(names)
            download_rpm_nums = download_rpm_nums + 1
    ftw.close()
    if download_rpm_nums:
        return newlist
    else:
        return False


def incomp_pkg_num():
    tmp=''
    num=0
    for line in open(abi_incomp_chk, 'r').readlines():
        tmp_01 = line.split(',')[0]
        if tmp!=tmp_01:
            num = num + 1
        tmp = line.split(',')[0]
    return num

