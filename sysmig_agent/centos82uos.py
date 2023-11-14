# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier:   MulanPubL-2.0-or-later

import os
import subprocess
import re
import socket
import sys
import shutil
import argparse
import platform
import logging
from sysmig_agent.share import *
from utils import *

reposdir=''


def get_bad_packages():
    os_version_ret = platform.dist()
    version = os_version_ret[1].split('.', -1)
    local_os_version = version[0]
    badpackages = ''
    if '8' == local_os_version:
        with open('sysmig_agent/8badpackage.txt', 'r') as bf:
            for bad_package in bf:
                badpackages = badpackages + ' ' + bad_package.strip()
            bf.close()
    elif '7' == local_os_version:
        with open('sysmig_agent/7badpackage.txt', 'r') as bf:
            for bad_package in bf:
                badpackages = badpackages + ' ' + bad_package.strip()
            bf.close()
    return badpackages


def local_disabled_release_repo():
    path = '/etc/yum.repos.d'
    if os.path.exists(path):
        file_list = os.listdir(path)
    for file in file_list:
        fpath = os.path.join(path,file)
        if os.path.isdir(fpath):
            continue
        else:
            if re.fullmatch('switch-to-uos.repo',file,re.IGNORECASE):
                continue
            elif not re.search('repo',file,re.IGNORECASE):
                continue
            with open(fpath,'r') as fdst:
                allrepo = fdst.read()
                fdst.close()
                print(allrepo)
                with open(fpath+'.disabled','w+') as fdst:
                    fdst.write('#This is a yum repository file that was disabled . <Migration to UiniontechOS>\n'+allrepo)
                    fdst.close()
                    os.remove(fpath)



def check_pkg(pkg):
    if pkg.split('/')[0] == '':
        if os.path.exists(pkg):
            return True
        else:
            return False

    paths = os.environ['PATH'].split(':')
    for path in paths:
        if not os.path.isdir(path):
            continue
        for f in os.listdir(path):
            if os.path.isfile(os.path.join(path, f)):
                if f == pkg:
                    return True
    return False

def clean_and_exit():
    global reposdir
    repo_path = os.path.join(reposdir, 'switch-to-uos.repo')
    if os.path.exists(repo_path):
        os.remove(repo_path)
    sys.exit(1)


def get_disk_info(string):
    dev_name = ""
    part_name = ""
    length = len(string)
    for c in range(length - 1, -1, -1):
        if not string[c].isdigit():
            if string.find('nvme') != -1:
                dev_name = string[0:c]
                part_num = string[c + 1:length]
            else:
                dev_name = string[0:c + 1]
                part_num = string[c + 1:length]
            break
    return dev_name, part_num


def pre_system_rpms_info():
 # display rpms info before conversion
    print("Creating a list of RPMs installed before the switch")
    print("Verifying RPMs installed before the switch against RPM database")
    out1 = subprocess.check_output('rpm -qa --qf \
           "%{NAME}|%{VERSION}|%{RELEASE}|%{INSTALLTIME}|%{VENDOR}|%{BUILDTIME}|%{BUILDHOST}|%{SOURCERPM}|%{LICENSE}|%{PACKAGER}\\n" \
           | sort > "/var/tmp/uos-migration/UOS_migration_log/rpms-list-before.txt"', shell=True)
    out2 = subprocess.check_output('rpm -Va | sort -k3 > "/var/tmp/uos-migration/UOS_migration_log/rpms-verified-before.txt"',shell=True)
    files = os.listdir('/var/tmp/uos-migration/')
    hostname = socket.gethostname()
    print("Review the output of following files:")
    for f in files:
        if re.match(hostname+'-rpms-(.*)\.log', f):
            print(f)


def centos8_main(osname,task_id):
    global reposdir

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    log_name = '/var/tmp/uos-migration/UOS_migration_log/migration_log.txt'
    cwd = '/var/tmp/uos-migration/UOS_migration_log'
    if not os.path.exists(cwd):
        os.mkdir(cwd)
    logfile = log_name
    fh = logging.FileHandler(logfile, mode='w')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    logger.info("Checking if the tool is executed by root user")
    # check if the script is executed by root user
    # if os.geteuid() != 0:
    #     logger.info("Please run the tool as root user.")
    #     sys.exit(1)
    badpackages = get_bad_packages()
    # check required packages
    logger.info('Checking required packages')
    for pkg in ['rpm', 'yum', 'curl']:
        if not check_pkg(pkg):
            logger.info("Could not found " + pkg)
            sys.exit(1)

    # sto system rpms info before migration
    pre_system_rpms_info()

    # check if the os old_version is supported
    logger.info("========= Checking: distribution =========")
    old_version = subprocess.check_output("rpm -q --whatprovides /etc/redhat-release", shell=True)
    old_version = str(old_version, 'utf-8')
    delect_release = old_version
    old_version = old_version.split('\n')[:-1]
    if len(old_version) == 0:
        logger.info("You appear to be running an unsupported distribution.")
        sys.exit(1)
    if len(old_version) > 1:
        logger.info("Could not determine your distribution because multiple packages are providing redhat-release:")
        logger.info('\n'.join(old_version))
        sys.exit(1)

    old_version = old_version[0]
    logger.info(old_version)
    osrelease = osname + '-release'
    linux_release = osname + '-linux-release'
    if re.match('uos-release', old_version):
        logger.info("You are already using Uniontech.")
        sys.exit(1)  #####get again
    elif re.match(linux_release, old_version):
        subver = old_version.split('-')[3]
    elif re.match(osrelease, old_version):
        subver = old_version.split('-')[2]
    else:
        logger.info("Your are using an unsupported distribution.")
        sys.exit(1)
    if re.match('7', subver):
        logger.info("Your system will be migrated from CentOS7 to UniontechOS")
    elif re.match('20', subver):
        logger.info("You appear to be running an unsupported distribution.")
        sys.exit(1)

    logger.info("========= Checking: required python packages =========")
    if not check_pkg('/usr/libexec/platform-python'):
        logger.info('/usr/libexec/platform-python not found.')
    base_packages = ['basesystem', 'initscripts', 'uos-logos', 'plymouth', 'grub2', 'grubby']

    logger.info("========= Checking: yum lock ===========")
    if os.path.exists('/var/run/yum.pid'):
        with open('/var/run/yum.pid', 'r') as f:
            pid = f.read()
            f.close()
            with open('/proc/' + pid + '/comm', 'r') as ff:
                comm = ff.read()
                logger.info('Another app is currently holding the yum lock: ' + comm)
                logger.info('Running as pid: ' + pid)
                logger.info('Please kill it and run the tool again.')
                ff.close()
            sql_mig_statue('18')
            #sql_task_statue(3)
            sql_task_statue(3, task_id)
            return None

    # check dnf
    if re.match('8\.', subver):
        logger.info("========= Checking: dnf =========")
        logger.info("Identifying dnf modules that are enabled...")
        enabled_modules = str(
            subprocess.check_output("dnf module list --enabled | grep rhel | awk '{print $1}'", shell=True),
            'utf-8')
        enabled_modules = enabled_modules.split('\n')[:-1]
        unknown_mods = []
        if len(enabled_modules) > 0:
            for mod in enabled_modules:
                if re.fullmatch('container-tools|llvm-toolset| perl-DBD-SQLite|perl-DBI|satellite-5-client|perl', mod):
                    subprocess.run('dnf module reset -y ' + mod, shell=True)
                if not re.fullmatch('container-tools|go-toolset|jmc|llvm-toolset|rust-toolset|virt', mod):
                    unknown_mods.append(mod)
            if len(unknown_mods) > 0:
                logger.info('This tool is unable to automatically switch module(s) ' \
                            + ','.join(unknown_mods) \
                            + ' from a CentOS \'rhel\' stream to an UniontechOS equivalent.' \
                            )
                sql_mig_statue('28')
                sql_task_statue(3)

    logger.info("========= Looking for yumdownloader ==========")
    cmd_license = 'yum -y install uos-license-mini license-config '
    run_subprocess(cmd_license)
    if not check_pkg('yumdownloader'):
        subprocess.run("yum -y install yum-utils --disablerepo C* || true", shell=True)
        # if not check_pkg('yumdownloader'):
        #    clean_and_exit()

    logger.info("========= Start converting =========")
    subprocess.run('rpm -e --nodeps {}'.format(delect_release) , shell=True)
    if re.match(osname + '-release', old_version):
        repos = 'rpm -qa ' + osname + '*repos'
        old_version = subprocess.check_output(repos, shell=True)
        old_version = str(old_version, 'utf-8')[:-1]
        subprocess.run('rpm -e --nodeps ' + old_version, shell=True)

    logger.info("Downloading uos release package...")
    dst_release = ['uos-release']
    try:
        downdir = ' --destdir /var/tmp/uos-migration '
        stat = subprocess.check_output("yumdownloader " + downdir + ' '.join(dst_release), shell=True)
        if not check_pkg('yumdownloader'):
            subprocess.run("yum -y install yum-utils --disablerepo C* || true", shell=True)
        if not check_pkg('yumdownloader'):
            clean_and_exit()
        pass
    except Exception:
        logger.info('\n'.join(dst_release))
        logger.info("Are you behind a proxy? If so, make sure the 'http_proxy' environmen")
        logger.info("variable is set with your proxy address.")
        logger.info("An error occurred while attempting to switch this system to Uniontech" + \
                    "and it may be in an unstable/unbootable state. To avoid further issues, " + \
                    "the script has terminated.")

    logger.info("Switching old release package with Uniontech...")
    dst_rpms = [s + '*.rpm' for s in dst_release]
    oldkeys = osname + '-gpg-keys'
    subprocess.run('rpm -e --nodeps ' + oldkeys, shell=True)
    subprocess.run('rpm -i --force ' + '/var/tmp/uos-migration/'+dst_rpms[0] + ' --nodeps', shell=True)
    # os.remove(dst_rpms)
    local_disabled_release_repo()
    # mig_kernel(kernel_version)
    logger.info("Installing base packages for UniontechOS...")
    cmd = 'yum shell -y <<EOF\n\
remove ' + badpackages + '\n\
install ' + ' '.join(base_packages) + '\n\
run\n\
EOF'

    _, code = run_subprocess(cmd)
    if code != 0:
        logger.info("Could not install base packages.Run 'yum distro-sync' to manually install them..{}.".format(code))
        sql_mig_statue('38')
        #sql_task_statue(3)
        sql_task_statue(3, task_id)
        return None
    '''
    try:
        cwd = '/var/tmp/uos-migration/UOS_migration_log'
        if not os.path.exists(cwd):
            os.mkdir(cwd)

        fdout = open("/var/tmp/uos-migration/UOS_migration_log/mig_log.txt", 'a')
        fdout.close()
        # run_cmd2file(cmd)
        if code != 0:
            logger.info("Could not install base packages.Run 'yum distro-sync' to manually install them....")
            sql_mig_statue('28')
            return None
    except:
        logger.info("Could not install base packages.Run 'yum distro-sync' to manually install them.")
    #     sys.exit(1)
'''
    if os.access('/usr/libexec/plymouth/plymouth-update-initrd', os.X_OK):
        logger.info("Updating initrd...")
        indexhtml = 'rpm -e --nodeps ' + osname + '-indexhtml'
        os.system(indexhtml)
        fdout = open("/var/tmp/uos-migration/UOS_migration_log/mig_log.txt", 'a')
        subprocess.run('/usr/libexec/plymouth/plymouth-update-initrd', stdout=fdout, shell=True)
        # run_cmd2file('/usr/libexec/plymouth/plymouth-update-initrd')
        fdout.close()
    logger.info("Switch successful. Syncing with UniontechOS repositories.")
    if subver == '8.3':
        subprocess.run('yum -y downgrade crypto-policies --allowerasing', shell=True)
    sql_mig_statue('02')



def mig_distro_sync(skip,task_id):
    local_disabled_release_repo()
    cwdo = '/var/tmp/uos-migration/UOS_migration_log/mig_log.txt'
    cwde = '/var/tmp/uos-migration/UOS_migration_log/mig_err.txt'
    fdout = open(cwdo, 'a')
    fderr = open(cwde, 'a')
    if 0 == skip:
        cmd = 'yum -y distro-sync'
    else:  ##elif
        cmd = 'yum -y distro-sync --skip-broken'
    wt, code = run_subprocess(cmd)
    if 0 != code:
        cmd = 'yum -y update --skip-broken'
        wt_try, code_try = run_subprocess(cmd)
        if 0 != code_try:
            sql_mig_statue('48')
            sql_task_statue(3, task_id)
        else:
            sql_mig_statue('04')
        '''
            cmd = 'yum -y distro-sync'
            wt, code_atry = run_subprocess(cmd)
            if code_atry != 0:
                sql_mig_statue('04')
                #sql_mig_statue('48')
                #sql_task_statue(3, task_id)
            else:
                sql_mig_statue('04')
        '''
    else:
        sql_mig_statue('04')

# os_version_ret = platform.dist()
# osname = os_version_ret[0]
# centos8_main(osname)
# sys.exit(messageState('2'))
