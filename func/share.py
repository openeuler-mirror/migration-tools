import os
import platform
import re
import subprocess

from func.utils import list_to_json

def getSysMigConf():
    confpath = '/etc/uos-sysmig/uos-sysmig.conf'
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
    print("Current system is uefi, add boot option to boot manager.")
    subprocess.run('which efibootmgr > /dev/null 2>&1 || dnf install -y efibootmgr', shell=True)
    disk_name = subprocess.check_output('mount | grep /boot/efi | awk \'{print $1}\'', shell=True)
    disk_name = str(disk_name, 'utf-8')
    disk_name = disk_name.split('\n')[0]
    dev_name,part_num = get_disk_info(disk_name)
    if dev_name == "" or part_num == "":
        print("Parse /boot/efi disk info failed, update boot loader failed.")
        return

    cmd=""
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