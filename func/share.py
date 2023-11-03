# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier:   MulanPubL-2.0-or-later
import logging
import os
import platform
import re
import shutil
import subprocess
from func.utils import list_to_json


def get_sysmig_conf():
    conf_path = '/etc/migration-tools/migration-tools.conf'
    if not os.path.exists(conf_path):
        return None
    else:
        cfid = agentip = serverip = agentport = serverport = baseurl = cftype = agentdatabase_ip \
            = serverdatabase_ip = agentdatabase_port = serverdatabase_port = ''
        server = None
        with open(conf_path, 'r') as cf:
            for line in cf:
                line = line.strip().strip('\n')
                if not line:
                    continue
                if re.search('\[Agent\]',line):
                    server = 0
                    continue
                elif re.search('\[Server\]',line):
                    server = None
                    continue
                else:
                    p = ret = ''
                    if re.match('\=',line):
                        continue
                    else:
                        p, ret = line.split('=', 1)
                    p = p.strip()
                    if re.fullmatch('ID', p):
                        cfid = ret.strip()
                    if re.fullmatch('IP', p):
                        if 0 == server:
                            agentip = str(ret).strip()
                        else:
                            serverip = str(ret).strip()
                    if re.fullmatch('PORT', p):
                        if 0 == server:
                            agentport = ret.strip()
                        else:
                            serverport = ret.strip()
                    if re.search('BASEURL', p):
                        baseurl = ret.strip()
                    if re.search('TYPE', p):
                        cftype = ret.strip()
                    if re.search('DATABASE_IP', p):
                        if 0 == server:
                            agentdatabase_ip = ret.strip()
                        else:
                            serverdatabase_ip = ret.strip()
                    if re.search('DATABASE_PORT', p):
                        if 0 == server:
                            agentdatabase_port = ret.strip()
                        else:
                            serverdatabase_port = ret.strip()
        cf.close()
        k_list = ['id', 'agentip', 'serverip', 'agentport', 'serverport', 'baseurl', 'type', 'agentdatabase_ip',
                   'serverdatabase_ip', 'agentdatabase_port', 'serverdatabase_port']
        v_list = [cfid, agentip, serverip, agentport, serverport, baseurl, cftype, agentdatabase_ip,
                     serverdatabase_ip, agentdatabase_port, serverdatabase_port]
        return list_to_json(k_list, v_list)


def run_cmd2file(cmd):
    fdout = open("/var/tmp/uos-migration/UOS_migration_log/mig_log.txt", 'a')
    f = open("/var/tmp/uos-migration/UOS_migration_log/err_log", 'a')
    p = subprocess.Popen(cmd, stdout=fdout, stderr=f, shell=True)
    if p.poll():
       return None
    p.wait()
    return None


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
    return dev_name, part_num


def add_boot_option():
    print("Current system is uefi, add boot option to boot manager.")
    subprocess.run('which efibootmgr > /dev/null 2>&1 || dnf install -y efibootmgr', shell=True)
    disk_name = subprocess.check_output('mount | grep /boot/efi | awk \'{print $1}\'', shell=True)
    disk_name = str(disk_name, 'utf-8')
    disk_name = disk_name.split('\n')[0]
    dev_name, part_num = get_disk_info(disk_name)
    if dev_name == "" or part_num == "":
        print("Parse /boot/efi disk info failed, update boot loader failed.")
        return None

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
    return None


def conf_grub():
    if os.path.isdir('/sys/firmware/efi'):
        subprocess.run('grub2-mkconfig -o /boot/efi/EFI/uos/grub.cfg', shell=True)
        add_boot_option()
    else:
        subprocess.run('grub2-mkconfig -o /boot/grub2/grub.cfg', shell=True)
    return None


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
    return None


def title_conf(ols_os_name):
    ols_os_name = ols_os_name.strip()
    path = '/boot/loader/entries'
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
        fpath = os.path.join(path, file)
        if os.path.isdir(fpath):
            continue
        else:
            with open(fpath, 'r') as fp:
                strall = fp.read()
                fp.close()
            if re.search(ols_os_name, strall, re.IGNORECASE):
                if fl:
                    os.remove(fpath)
                    continue
                else:
                    ustr = re.sub(ols_os_name, "UniontechOS", strall, 1, flags=re.IGNORECASE)
            if re.search('8 \(Core\)',strall):
                ustr = re.sub(' 8 ', ' 20 ', ustr, 1, flags=re.IGNORECASE)
                ustr = re.sub("Core", "kongzi", ustr, 1, flags=re.IGNORECASE)
                with open(fpath, 'w') as ptitle:
                    ptitle.write(ustr)
                    ptitle.close()
    return None


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
            elif mod == 'virt':
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
    out2 = subprocess.check_output('rpm -Va | sort -k3 > "/var/tmp/uos-migration/UOS_migration_log/rpms-verified-after.txt"', shell=True)

    logger.info("Switch complete.UniontechOS recommends rebooting this system.")
    return 0
