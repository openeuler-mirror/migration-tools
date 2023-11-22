# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier:   MulanPubL-2.0-or-later

import os
import sys
import json
import sqlite3
import re
import subprocess
import shutil
import socket
import platform
import logging
from datetime import datetime

sys.path.append("..")
from connect_sql import DBHelper

defaultencoding = 'utf-8'
# logdss = Logger('./logdss.log',logging.DEBUG,logging.DEBUG)
new_os = '统信服务器操作系统V20({})'
AGENT_DIR = '/var/tmp/uos-migration/'
PRE_MIG = '/var/tmp/uos-migration/UOS_analysis_report/rpmva-before.txt'
PRE_MIG_DIR = '/var/tmp/uos-migration/UOS_analysis_report'
MIGRATION_DIR = '/var/tmp/uos-migration/UOS_migration_log'
MIGRATION_REPORT_DIR = '/var/tmp/uos-migration/UOS_migration_completed_report'


PROGRESS = '/var/tmp/uos-migration/.progress'
RPMS = '/var/tmp/uos-migration/.rpms'
MIGRATION_KERNEL = '/var/tmp/uos-migration/kernel'
MIGRATION_LOG = '/var/tmp/uos-migration/UOS_migration_log/log'
MIGRATION_DATA_RPMS_DIR = '/var/tmp/uos-migration/data/exp-rst'
MIGRATION_DATA_RPMS_3_INFO = '/var/tmp/uos-migration/data/exp-rst/pkginfo_3.txt'
pstate = '/var/tmp/uos-migration/.state'

abi_file = '/var/tmp/uos-migration/data/exp-rst/agent_ABI_check_result.csv'
#Abi
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



def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        return ip
    finally:
        s.close()



def sql_abi_progress(data):
    sql = "UPDATE agent_task SET task_progress = {} ,task_Updatetime = NOW() WHERE agent_ip = '{}';".format(data, get_local_ip())
    try:
        ret = DBHelper().execute(sql)
    except:
        pass


def sql_migration_log(report_name, report_type):
    print(report_name)
    name = report_name.split('/', -1)
    print('name' + str(name))
    name = name[len(name) - 1]
    print('name' + name)
    sql = " INSERT INTO report_info ( agent_ip , create_time , report_name , report_type ) VALUES \
    ('{}',NOW(),'{}','{}')".format(get_local_ip(), name, report_type)
    try:
        ret = DBHelper().execute(sql)
    except:
        pass


def targz_mig_dir_abi():
    if os.path.exists(PRE_MIG_DIR):
        report_type = '迁移检测报告'
        report_name = _targz_dir(PRE_MIG_DIR)
        sql_migration_log(report_name, report_type)


def targz_mig_dir_log():
    if os.path.exists(MIGRATION_DIR):
        report_type = '迁移日志'
        report_name = _targz_dir(MIGRATION_DIR)
        sql_migration_log(report_name, report_type)


def targz_mig_dir_report():
    if os.path.exists(MIGRATION_REPORT_DIR):
        report_type = '迁移分析报告'
        report_name = _targz_dir(MIGRATION_REPORT_DIR)
        sql_migration_log(report_name, report_type)



def _targz_dir(path):
    import tarfile
    '''
    :param path: 存放的文件夹路径
    :return:失败返回错误码
    '''
    hostname = socket.gethostname()
    ip = get_local_ip()
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    tar_name = path + "_%s" % ip + "_%s" % hostname + "_%s" % now
    tar_type = '.tar.gz'
    compression = "tar -zcvf " + tar_name + tar_type + " %s" % path
    print(compression)
    # filepwd = '/var/tmp/uos-migration'
    filepwd = AGENT_DIR
    tar = tarfile.open(tar_name + tar_type, "w:gz")
    # 创建压缩包
    for root, dir, files in os.walk(path):
        root_ = os.path.relpath(root, start=filepwd)
        print('root:'+str(root)+'dir'+str(dir)+'_root:'+str(root_))
        for file in files:
            fullpath = os.path.join(root, file)
            tar.add(fullpath, arcname=os.path.join(root_, file))
            # tar.add(fullpath, arcname=os.path.basename(filepwd))
    tar.close()
    # _, recode = run_subprocess(compression)
    # store migration log information in database
    return tar_name



def sql_online_statue(statue, task_id):
    """
    sql：agent主机的在线状态更新
    :param statue: 0：在线; 1：离线
    :param task_id:agent的json内的task_id
    :return:
    """
    # sql = "UPDATE agent_info SET agent_online_status = {} WHERE agent_ip = {};".format(statue, get_local_ip())
    sql = "UPDATE agent_info SET agent_online_status = {} WHERE agent_ip = (SELECT agent_ip FROM agent_task WHERE task_id = '{}');".format(
        statue, task_id)
    try:
        ret = DBHelper().execute(sql)
    except:
        pass


def sql_mig_statue(statue):
    # sql = "UPDATE agent_task SET task_statues = {} , task_Updatetime = NOW() WHERE task_id = '{}';".format(statue, task_id)
    sql = "UPDATE agent_task SET task_data = '{}' , task_Updatetime = NOW() WHERE agent_ip = '{}';".format(statue,
                                                                                                           get_local_ip())
    try:
        ret = DBHelper().execute(sql)
    except:
        pass


def sql_task_statue(statue, task_id = None):
    if task_id:
        sql = "UPDATE agent_task SET task_status = {} , task_Updatetime = NOW() WHERE task_id = '{}';".format(statue, task_id)
    else:
        sql = "UPDATE agent_task SET task_status = {} , task_Updatetime = NOW() WHERE agent_ip = '{}';".format(statue, get_local_ip())
    try:
        ret = DBHelper().execute(sql)
    except Exception :
        pass


def sql_show_tables():
    sql = "SELECT task_progress,task_data FROM agent_task WHERE agent_ip = '{}';".format(get_local_ip())
    ret_sql_msg_info = DBHelper().execute(sql)
    if ret_sql_msg_info:
        print(str(ret_sql_msg_info.fetchall()) + '\n')


def abi_file_connect(sql_r):
    abi_sql = "INSERT INTO agent_ABI_check_result VALUES('"+ get_local_ip()+"'," + sql_r + ',NOW());'
    s = DBHelper()
    ret_sql_msg = s.execute(abi_sql)

def local_disabled_release_repo():
    """
    将系统内存在的repository文件置为不可用，只保留switch-to-uos.repo
    :return:
    """
    path = '/etc/yum.repos.d'
    if os.path.exists(path):
        file_list = os.listdir(path)
    for file in file_list:
        fpath = os.path.join(path, file)
        if os.path.isdir(fpath):
            continue
        else:
            if re.fullmatch('switch-to-uos.repo', file, re.IGNORECASE):
                continue
            elif not re.search('repo', file, re.IGNORECASE):
                continue
            with open(fpath, 'r') as fdst:
                allrepo = fdst.read()
                fdst.close()
                with open(fpath + '.disabled', 'w+') as fdst:
                    fdst.write(
                        '#This is a yum repository file that was disabled . <Migration to UiniontechOS>\n' + allrepo)
                    fdst.close()
                    os.remove(fpath)




def getSysMigConf():
    confpath = '/etc/migration-tools/migration-tools.conf'
    if not os.path.exists(confpath):
        return None
    else:
        cfid=agentip=serverip=agentport=serverport=baseurl=cftype=agentdatabase_ip=serverdatabase_ip=agentdatabase_port=serverdatabase_port=''
        server = None
        with open(confpath,'r') as cf:
            for line in cf:
                line = line.strip().strip('\n')
                if not line:
                    continue
                if re.search('\[Agent\]',line):
                    server=0
                    continue
                elif re.search('\[Server\]',line):
                    server = None
                    continue
                else:
                    p=ret=''
                    if re.match('\=',line):
                        continue
                    else:
                        p,ret=line.split('=',1)
                    p = p.strip()
                    if re.fullmatch('ID',p):
                        cfid = ret.strip()
                    if re.fullmatch('IP',p):
                        if 0 == server:
                            agentip = str(ret).strip()
                        else:
                            serverip = str(ret).strip()
                    if re.fullmatch('PORT',p):
                        if 0 == server:
                            agentport = ret.strip()
                        else:
                            serverport = ret.strip()
                    if re.search('BASEURL',p):
                        baseurl = ret.strip()
                    if re.search('TYPE',p):
                        cftype = ret.strip()
                    if re.search('DATABASE_IP',p):
                        if 0 == server:
                            agentdatabase_ip = ret.strip()
                        else:
                            serverdatabase_ip = ret.strip()
                    if re.search('DATABASE_PORT',p):
                        if 0 == server:
                            agentdatabase_port = ret.strip()
                        else:
                            serverdatabase_port = ret.strip()
        cf.close()
        keylist = ['id','agentip','serverip','agentport','serverport','baseurl','type','agentdatabase_ip','serverdatabase_ip','agentdatabase_port','serverdatabase_port']
        valuelist = [cfid,agentip,serverip,agentport,serverport,baseurl,cftype,agentdatabase_ip,serverdatabase_ip,agentdatabase_port,serverdatabase_port]
        return list_to_json(keylist,valuelist)


def run_cmd2file(cmd):
    fdout = open("/var/tmp/uos-migration/UOS_migration_log/mig_log.txt",'a')
    fderr = open("/var/tmp/uos-migration/UOS_migration_log/err_log",'a')
    p = subprocess.Popen(cmd, stdout=fdout, stderr=fderr, shell=True)
    if p.poll():
       return
    p.wait()
    return


def get_disk_info(string):
    dev_name = ""
    part_num = ""
    length = len(string)
    for c in range(length-1, -1, -1):
        if not string[c].isdigit():
            if string.find('nvme') != -1:
                dev_name = string[0:c]
                part_num = string[c+1:length]
            else:
                dev_name = string[0:c+1]
                part_num = string[c+1:length]
            break
    return dev_name,part_num


def add_boot_option():
    """
    Current system is uefi, add boot option to boot manager.
    """
    subprocess.run('which efibootmgr > /dev/null 2>&1 || yum install -y efibootmgr', shell=True)
    disk_name = subprocess.check_output('mount | grep /boot/efi | awk \'{print $1}\'', shell=True)
    disk_name = str(disk_name, 'utf-8')
    disk_name = disk_name.split('\n')[0]
    dev_name, part_num = get_disk_info(disk_name)
    if dev_name == "" or part_num == "":
        # "Parse /boot/efi disk info failed, update boot loader failed.
        return

    cmd = ""
    arch = platform.machine()
    if arch == "x86_64":
        cmd = 'efibootmgr -c -d ' + dev_name + ' -p ' + part_num + ' -l "/EFI/uos/grubx86.efi" -L "Uniontech OS"'
    elif arch == "aarch64":
        cmd = 'efibootmgr -c -d ' + dev_name + ' -p ' + part_num + ' -l "/EFI/uos/grubaa64.efi" -L "Uniontech OS"'
    try:
        subprocess.check_call(cmd, shell=True)
    except:
        print("Use efibootmgr update boot loader failed, please update boot loader manually.")


def conf_grub():
    if os.path.isdir('/sys/firmware/efi'):
        subprocess.run('grub2-mkconfig -o /boot/efi/EFI/uos/grub.cfg' ,shell=True)
        add_boot_option()
    else:
        subprocess.run('grub2-mkconfig -o /boot/grub2/grub.cfg',shell=True)


def process_special_pkgs():
    subprocess.run('rpm -q centos-logos-ipa && dnf swap -y centos-logos-ipa uos-logos-ipa', shell=True)
    subprocess.run('rpm -q centos-logos-httpd && dnf swap -y centos-logos-httpd uos-logos-httpd', shell=True)
    subprocess.run('rpm -q anolis-logos-ipa && dnf swap -y anolis-logos-ipa uos-logos-ipa', shell=True)
    subprocess.run('rpm -q anolis-logos-httpd && dnf swap -y anolis-logos-httpd uos-logos-httpd', shell=True)
    subprocess.run('rpm -q redhat-lsb-core && dnf swap -y redhat-lsb-core system-lsb-core', shell=True)
    subprocess.run('rpm -q redhat-lsb-submod-security && dnf swap -y redhat-lsb-submod-security system-lsb-submod-security',shell=True)
    subprocess.run('rpm -q rhn-client-tools && dnf -y remove rhn-client-tools python3-rhn-client-tools python3-rhnlib', shell=True)
    subprocess.run('rpm -q subscription-manager && dnf -y remove subscription-manager', shell=True)
    subprocess.run('rpm -q python3-syspurpose && dnf -y remove python3-syspurpose', shell=True)
    subprocess.run('rpm -e $(rpm -q gpg-pubkey --qf "%{NAME}-%{VERSION}-%{RELEASE} %{PACKAGER}\\n" | grep CentOS | awk \'{print $1}\')', shell=True)


def title_conf(oldosname):
    """
    Change the boot start option after system migration
    :param oldosname:old system name
    :return:
    """
    oldosname = oldosname.strip()
    if oldosname == 'redhat':
        capital = 'Red Hat'
    elif oldosname == 'centos':
        capital = 'CentOS'
    path = '/boot/loader/entries'
    # path='/root/a'
    if os.path.exists(path):
        file_list = os.listdir(path)
    else:
        return None
    fl = False
    for file in file_list:
        fpath = os.path.join(path, file)
        if os.path.isdir(fpath):
            continue
        else:
            with open(fpath, 'r') as fp:
                strall = fp.read()
                fp.close()
            if re.search('uniontech', strall, re.IGNORECASE):
                fl = True
    for file in file_list:
        ustr = None
        brackets = ""
        fpath = os.path.join(path, file)
        if os.path.isdir(fpath):
            continue
        else:
            with open(fpath, 'r') as fp:
                strall = fp.read()
                fp.close()
            '''
            if re.search(oldosname, strall, re.IGNORECASE):
                if fl:
                    os.remove(fpath)
                    continue
                else:
                    print(strall,capital)
                    ustr = re.sub(capital, "UniontechOS", strall, 1, flags=re.IGNORECASE)
            '''
            if re.search(capital, strall):
                line = strall.split('\n', -1)[0]
                for char in range(len(line)):
                    if line[char] == '(':
                        p = char
                        continue
                    if line[char] == ')':
                        e = char+1
                        brackets = line[p:e]
                        break
                title = 'title UniontechOS Linux ' + brackets + ' 20 (kongzi)'
                open(fpath, 'w').write(strall.replace(line, title))


def json_list_to_json(keylist, valuelist):
    res = dict(zip(keylist, valuelist))
    #    logdss.info (res)
    return json.dumps(res)

def list_to_json(keylist, valuelist):
    res = dict(zip(keylist, valuelist))
    res = json.dumps(res)
    #    logdss.info (res)
    return json.dumps(res)


def main_conf(osname):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    log_name = '/var/tmp/uos-migration/UOS_migration_log/log'
    logfile = log_name
    fh = logging.FileHandler(logfile, mode='w')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    enabled_modules = str(
        subprocess.check_output("dnf module list --enabled | grep rhel | awk '{print $1}'", shell=True),
        'utf-8')
    enabled_modules = enabled_modules.split('\n')[:-1]
    if len(enabled_modules) > 0:
        for mod in enabled_modules:
            subprocess.run('dnf module reset -y '+mod, shell=True)
            if re.fullmatch('container-tools|go-toolset|jmc|llvm-toolset|rust-toolset', mod):
                subprocess.run('dnf module install -y '+mod, shell=True)
            elif mod =='virt':
                subprocess.run('dnf module install -y '+mod, shell=True)
            else:
                logger.info("Unsure how to transform module"+mod)

    try:
        subprocess.check_call('dnf module list --enabled | grep satellite-5-client', shell=True)
        logger.info("UniontechOS does not provide satellite-5-client module, disable it.")
        subprocess.run('dnf module disable -y satellite-5-client', shell=True)
    except:
        pass
    process_special_pkgs()   
    logger.info("Removing yum cache")
    if os.path.isfile('/var/cache/yum'):
        os.remove('/var/cache/yum')
    elif os.path.isdir('/var/cache/yum'):
        shutil.rmtree('/var/cache/yum')
    if os.path.isfile('/var/cache/dnf'):
        os.remove('/var/cache/dnf')
    elif os.path.isdir('/var/cache/dnf'):
        shutil.rmtree('/var/cache/dnf')
    logger.info("------------- : "+osname)
    
    conf_grub()
    title_conf(osname)

    logger.info("Creating a list of RPMs installed after the switch")
    logger.info("Verifying RPMs installed after the switch against RPM database")
    out1 = subprocess.check_output('rpm -qa --qf \
    "%{NAME}|%{VERSION}|%{RELEASE}|%{INSTALLTIME}|%{VENDOR}|%{BUILDTIME}|%{BUILDHOST}|%{SOURCERPM}|%{LICENSE}|%{PACKAGER}\n" \
    | sort > "/var/tmp/uos-migration/UOS_migration_log/rpms-list-after.txt"', shell=True)
    out2 = subprocess.check_output('rpm -Va | sort -k3 > "/var/tmp/uos-migration/UOS_migration_log/rpms-verified-after.txt"',shell=True)

    logger.info("Switch complete.UniontechOS recommends rebooting this system.")
    return 0


def sql_os_newversion(localos):
    sql = "UPDATE agent_info SET agent_migration_os = '{}' WHERE agent_ip = '{}';".format(localos, get_local_ip())
    try:
        ret = DBHelper().execute(sql)
    except:
        pass


def get_new_osversion():
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
            localos = new_os.format(localos.strip().strip('\n'))
            sql_os_newversion(localos)

    else:
        sql_os_newversion('NULL')


def run_subprocess(cmd="", print_cmd=True, print_output=True):
    """Call the passed command and optionally log the called command (print_cmd=True) and its
    output (print_output=True). Switching off printing the command can be useful in case it contains
    a password in plain text.
    """
    cwdo = '/var/tmp/uos-migration/UOS_migration_log/mig_log.txt'
    cwde = '/var/tmp/uos-migration/UOS_migration_log/mig_err.txt'
    # fderr = open(cwde, 'a')
    # from logging import *
    # if print_cmd:
    #     log.debug("Calling command '%s'" % cmd)

    # Python 2.6 has a bug in shlex that interprets certain characters in a string as
    # a NULL character. This is a workaround that encodes the string to avoid the issue.
    if print_output:
        fdout = open(cwdo, 'a')
        fderr = open(cwde, 'a')
    if sys.version_info[0] == 2 and sys.version_info[1] == 6:
        cmd = cmd.encode("ascii")
    # cmd = shlex.split(cmd, False)
    process = subprocess.Popen(
        cmd,
        # stdout=subprocess.PIPE,
        # stderr=subprocess.STDOUT,
        stdout=fdout,
        stderr=fderr,
        bufsize=1,
        shell=True
    )
    output = ""
    try:
        for line in iter(process.stdout.readline, b""):
            output += line.decode()
    except:
        pass

    #            loggerinst.info(line.decode().rstrip("\n"))

    # Call communicate() to wait for the process to terminate so that we can get the return code by poll().
    # It's just for py2.6, py2.7+/3 doesn't need this.
    process.communicate()

    return_code = process.poll()
    return output, return_code



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

