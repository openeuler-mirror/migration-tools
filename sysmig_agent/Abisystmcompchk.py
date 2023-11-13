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


def system_version_id():
    fp = open('/etc/os-release', 'r')
    for line in fp:
        if 'VERSION_ID' in line:
            break
    fp.close()
    return line.split('=', 1)[1].replace('"', '').replace('\n', '')


def get_cur_sys_version():
    fp = open('/etc/os-release', 'r')
    for line in fp:
        if 'PRETTY_NAME' in line:
            break
    fp.close()
    return line.split('=', 1)[1].replace('"', '').replace('\n', '')


def get_migration_sys_info():

    behind_sys_info = exp_rst_dir + 'before-system-info.txt'
    with open(behind_sys_info, 'r') as file_object:
        behind_list_info = file_object.readlines()

    migration_sys_info = '1|2|' + get_cur_sys_version()
    behind_list_info.append(migration_sys_info)

    #20220107 modify lihp: get kernel version
    #migration_kernel_verison = '2|2|' + platform.release()
    migration_kernel_verison = '2|2|' + platform_release('1')
    behind_list_info.append(migration_kernel_verison)

    with open(migration_system_install, 'r') as frm:
        install_pkgs_num = str(len(frm.readlines()))
    behind_list_info.append('8|2|' + install_pkgs_num)

    return behind_list_info


#Create data list for write to .xls of sheet[0]
#ge：['1|1|CentOS Linux 8 (Core)', '2|1|4.18.0-147.el8.x86_64', '4|1|26.4GB', '5|1|x86_64', '8|1|1278', '11|1|1', '12|1|2', '13|1|2']
def get_cur_sys_info_list():
    list_info = []
    before_sys_info = exp_rst_dir + 'before-system-info.txt'
    sys_version_tmp = exp_rst_dir + 'sys-version-tmp'

    #Used after system migration
    with open(sys_version_tmp, 'w') as file_object:
        file_object.write(get_cur_sys_version())

    #current system version, write sheet[0]:1-row,1-column
    cur_sys_info = '1|1|' + get_cur_sys_version()
    list_info.append(cur_sys_info)

    #current kernel version, write sheet[0]:2-row,1-column
    #20220107 modify lihp: get kernel version of migrate before
    #cur_kernel_verison = '2|1|' + platform.release()
    cur_kernel_verison = '2|1|' + platform_release('0')
    list_info.append(cur_kernel_verison)

    #/var/cache available space,write sheet[0]:4-row,1-column
    cur_var_cache = '4|1|' + os_storage() + 'GB'
    list_info.append(cur_var_cache)

    #system architecture, write sheet[0]:5-row,1-line
    cur_arch = '5|1|' + platform.processor()
    list_info.append(cur_arch)

    #Be replaced rpm packages number,write sheet[0]:8-row,1-column
    with open(migration_system_total, 'r') as fr:
        replace_pkgs_num = str(len(fr.readlines()))
    list_info.append('8|1|' + replace_pkgs_num)

    #Compatible with the number, write sheet[0]:11-row,1-column
    with open(abi_comp_chk, 'r') as fc:
        comp_num_int = len(fc.readlines())
        comp_num = '11|1|' + str(comp_num_int)
    list_info.append(comp_num)

    #Icompatible with the number,write sheet[0]:12-row,1-column
    incomp_num = '12|1|' + str(incomp_pkg_num())
    list_info.append(incomp_num)

    #The total number of packages，write sheet[0]:13-row,1-column
    sum_num = comp_num_int + incomp_pkg_num()
    list_info.append('13|1|' + str(sum_num))

    #write to file,report generation after migration
    with open(before_sys_info, 'w') as fpbsi:
        fpbsi.write(cur_sys_info + '\n')
        fpbsi.write(cur_kernel_verison + '\n')
        fpbsi.write(cur_var_cache + '\n')
        fpbsi.write(cur_arch + '\n')
        fpbsi.write('8|1|' + replace_pkgs_num + '\n')
        fpbsi.write(comp_num + '\n')
        fpbsi.write(incomp_num + '\n')
        fpbsi.write('13|1|' + str(sum_num) + '\n')

    return list_info


def mycopyfile(srcfile, dstfile, logger):
    if not os.path.exists(srcfile):
        logger.info("Please check!!!! src file not exit:" +  srcfile)
        return False
    else:
        fpath,fname=os.path.split(dstfile)
        if not os.path.exists(fpath):
            os.makedirs(fpath)
        copyfile(srcfile,dstfile)

    return dstfile


#Generate report name
def create_migrate_report_name(flag, logg):

    migrate_before_report_path = '/var/tmp/uos-migration/UOS_analysis_report/'
    migrate_behind_report_path = '/var/tmp/uos-migration/UOS_migration_completed_report/'

    migrate_report_before_sample_name = 'UOS_migration_report_HOSTIP_HOSTNAME_YYYYMMDDHHMM-BEFORE.xls'
    migrate_report_behind_sample_name = 'UOS_migration_report_HOSTIP_HOSTNAME_YYYYMMDDHHMM-BEHIND.xls'

    hostip = get_local_ip()
    hostname = socket.gethostname()
    hosttime = datetime.datetime.now().strftime('%Y%m%d%H%M')
    abs_path = os.path.abspath('sysmig_agent/txts/')

    if not os.path.exists(migrate_behind_report_path):
        os.makedirs(migrate_behind_report_path)

    #migration before
    if flag=='0':
        migrate_name_01 = migrate_report_before_sample_name.replace('HOSTIP', hostip)
        migrate_name_02 = migrate_name_01.replace('HOSTNAME', hostname)
        migrate_name = migrate_before_report_path + migrate_name_02.replace('YYYYMMDDHHMM-BEFORE', hosttime)
        migrate_path_name_sample = abs_path + '/' +  migrate_report_before_sample_name

    #migration behind
    elif flag=='1':
        migrate_name_01 = migrate_report_behind_sample_name.replace('HOSTIP', hostip)
        migrate_name_02 = migrate_name_01.replace('HOSTNAME', hostname)
        migrate_name = migrate_behind_report_path + migrate_name_02.replace('YYYYMMDDHHMM-BEHIND', hosttime)
        migrate_path_name_sample = abs_path + '/' + migrate_report_behind_sample_name

    #Rename the real report name
    return mycopyfile(migrate_path_name_sample, migrate_name, logg)


def write_row_and_column(report_name_rc, value_list, index):

    row_column_rb = xlrd.open_workbook(report_name_rc, formatting_info=True)
    r_sheet = row_column_rb.sheet_by_index(index)
    row_column_wb = copy(row_column_rb)
    row_column_sheet = row_column_wb.get_sheet(index)

    for data in value_list:
        row_column_sheet.write(int(data.split('|')[0]),int(data.split('|')[1]),data.split('|')[2])
    row_column_wb.save(report_name_rc)


def write_column_by_column(report_name_cc, column_value_list, row, column, index):

    column_column_rb = xlrd.open_workbook(report_name_cc, formatting_info=True)
    r_sheet = column_column_rb.sheet_by_index(index)
    column_column_wb = copy(column_column_rb)
    column_column_sheet = column_column_wb.get_sheet(index)

    row_cc = row
    for column_data in column_value_list:
        column_column_sheet.write(row_cc, column, column_data.replace('\n','').split(',')[0])
        row_cc = row_cc + 1

    column_column_wb.save(report_name_cc)

def write_row_by_row(report_name_rr, row_value_list, row, column, index):

    row_row_rb = xlrd.open_workbook(report_name_rr, formatting_info=True)
    r_sheet = row_row_rb.sheet_by_index(index)
    row_row_wb = copy(row_row_rb)
    row_row_sheet = row_row_wb.get_sheet(index)

    before_summary_info = r_sheet.row_values(0)[0].replace('INCOMP_NUM', str(incomp_pkg_num()))
    row_row_sheet.write(0, 0, before_summary_info)

    row_rr = row
    column_rr = column
    for row_data in row_value_list:
        row_list = row_data.replace('\n','').split(',')
        i = column
        column_rr = column
        while i < (len(row_list) - 1):
            if i==2 or i==3:
                i = i + 1
                continue
            elif i==5:
                row_row_sheet.write(row_rr, column_rr, row_list[i]+','+row_list[i+1])
            else:
                row_row_sheet.write(row_rr, column_rr, row_list[i])
            i = i + 1
            column_rr = column_rr + 1
        row_rr = row_rr + 1
    row_row_wb.save(report_name_rr)


def write_summary_data(report_name_summary, index, flag):
    summary_rb = xlrd.open_workbook(report_name_summary, formatting_info=True)
    r_sheet = summary_rb.sheet_by_index(index)
    summary_wb = copy(summary_rb)
    summary_sheet = summary_wb.get_sheet(index)

    if flag == '0':
        with open(abi_comp_chk, 'r') as fs:
            comp_num = len(fs.readlines())
        before_summary_num = comp_num + incomp_pkg_num()

        before_summary_info = r_sheet.row_values(0)[0].replace('REPLACE_NUM', str(before_summary_num))
        summary_sheet.write(0, 0, before_summary_info)
        summary_sheet.write(2, 0, get_cur_sys_version())

    elif flag == '1':
        migrbef_sysver = exp_rst_dir + 'sys-version-tmp'

        with open(abi_comp_chk, 'r') as fsp:
            comp_num = len(fsp.readlines())

        with open(migration_system_install, 'r') as fsmp:
            install_comp_num = str(len(fsmp.readlines()))
        behind_summary_num = comp_num + incomp_pkg_num()

        with open(migrbef_sysver, 'r') as file_object:
            sys_version = file_object.read()

        # 20220107 modify lihp: keep the history data
        # os.remove(migrbef_sysver)

        behind_summary_info_tmp = r_sheet.row_values(0)[0].replace('REPLACE_NUM', str(behind_summary_num))
        behind_summary_info = behind_summary_info_tmp.replace('INSTALL_NUM', install_comp_num)
        summary_sheet.write(0, 0, behind_summary_info)
        summary_sheet.write(2, 0, sys_version)
        summary_sheet.write(2, 2, get_cur_sys_version())

    summary_wb.save(report_name_summary)


# Deal report of sheet by num value
def switch_write_migrate_report(report_name, num, flag):
    # sheet[0]-system info: write data:row|column|value
    if num == 0:
        if flag == '0':
            migration_value_list = get_cur_sys_info_list()
        elif flag == '1':
            migration_value_list = get_migration_sys_info()
        write_row_and_column(report_name, migration_value_list, num)
    # sheet[1]-rpm package
    elif num == 1:
        with open(current_system_unique, 'r') as fr_cur:
            column_cur_list = fr_cur.readlines()
        write_column_by_column(report_name, column_cur_list, 3, 0, num)

        if flag == '0':
            # sheet[1]:2-column
            with open(migration_system_total, 'r') as fr_migr:
                column_migr_list = fr_migr.readlines()
            write_column_by_column(report_name, column_migr_list, 3, 1, num)
        elif flag == '1':
            # sheet[1]:2-column
            with open(migration_system_install, 'r') as fr_migr:
                column_migr_list = fr_migr.readlines()
            write_column_by_column(report_name, column_migr_list, 3, 1, num)

            # sheet[1]:3-row
            with open(migration_system_total, 'r') as fr_migr:
                column_migr_list = fr_migr.readlines()
            write_column_by_column(report_name, column_migr_list, 3, 2, num)

        # summary data write to sheet[1]
        write_summary_data(report_name, num, flag)

    # sheet[2]-ABI compartion
    elif num == 2:
        with open(abi_comp_chk, 'r') as fr_comp:
            column_comp_list = fr_comp.readlines()
        write_column_by_column(report_name, column_comp_list, 1, 0, num)
    # sheet[3]-ABI Incompartion
    elif num == 3:
        with open(abi_incomp_chk, 'r') as fr_incomp:
            column_incomp_list = fr_incomp.readlines()
        write_row_by_row(report_name, column_incomp_list, 2, 0, num)


def get_system_unique_pkg(current_pkg_list, download_pkg_list):
    # clean history data
    if os.path.exists(current_system_unique):
        os.remove(current_system_unique)

    fcw = open(current_system_unique, 'w')
    for data in set(current_pkg_list).difference(set(download_pkg_list)):
        fcw.write(data + '\n')
    fcw.close()


#Check the environment before migration and generate a detection report
def migrate_before_abi_chk(q_query, task_status):
    i=0
    Flag='0'
    Oth='2'
    global percentage
    global total_rpm_nums
    task_status_error = '2'
    migration_download_list = []

    log = logger_init()
    log.info('==============  START TIME ：'+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' ==============')

    download_path = local_dir + 'uos/rpms'
    current_packages_string = get_system_pkg_name(Flag, log)
    if not current_packages_string:
        msg_tup = ('0', task_status_error)
        q_query.put(msg_tup)
        log.info('The current progress exit:' + str(msg_tup))
        #return False

    os.system('yumdownloader --destdir=%s%s --skip-broken' %(download_path, current_packages_string))

    download_list = get_system_pkg_list(migration_download_list)
    if not download_list:
        log.info('yumdownloader rpm pakcages failed ...')
        msg_tup = ('0', task_status_error)
        q_query.put(msg_tup)
        log.info('The current progress exit:' + str(msg_tup))
        #return False
    total_rpm_nums = len(download_list)

    current_list = get_system_pkg_name(Oth, log)
    if not current_list:
        msg_tup = ('0', task_status)
        q_query.put(msg_tup)
        log.info('The current progress exit:' + str(msg_tup_error))
        #return False

    get_system_unique_pkg(list(current_list), migration_download_list)

    cur_dir = os.getcwd()
    os.chdir(download_path)
    rst = MutilThread(download_list, q_query, log)
    os.chdir(cur_dir)

    agent_ABI_check_result()

    migrate_before_report_name = create_migrate_report_name(Flag, log)
    if not migrate_before_report_name:
        msg_tup = ('0', task_status)
        q_query.put(msg_tup)
        log.info('The current progress exit:' + str(msg_tup))
        #return False

    while i < 4:
        write_migrate_report_rst =switch_write_migrate_report(migrate_before_report_name, i, Flag)
        i = i + 1

    task_status = '0'
    msg_tup = (percentage, task_status)
    q_query.put(msg_tup)
    log.info('The current progress has been completed:' + str(msg_tup))
    log.info('==============  END TIME ：'+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' ==============')

    return '0'


#Check the environment after the migration and generate a detection report
def migrate_behind_abi_chk():
    i=0
    Flag='1'

    log = logger_init()

    current_install_uos_list = get_system_pkg_name(Flag, log)
    if not current_install_uos_list:
        return False

    migrate_behind_report_name = create_migrate_report_name(Flag, log)
    if not migrate_behind_report_name:
        return False

    while i < 4:
        write_migrate_report_rst =switch_write_migrate_report(migrate_behind_report_name, i, Flag)
        i = i + 1

    return '0'
