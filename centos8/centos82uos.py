#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.  

# SPDX-License-Identifier:   MulanPubL-2.0-or-later

import os
import subprocess
import re
import dnf
import socket
import sys
import shutil
import argparse
import platform

local_UniontechOS_repo = '''[UniontechOS-$releasever-AppStream]
name = UniontechOS $releasever AppStream
#baseurl = https://enterprise-c-packages.chinauos.com/server-enterprise-c/kongzi/1020/AppStream/$basearch
baseurl = file:///mnt/iso/AppStream
enabled = 1
username=$auth_u
password=$auth_p
gpgkey = file:///etc/pki/rpm-gpg/RPM-GPG-KEY-uos-release
gpgcheck = 0
skip_if_unavailable = 1

[UniontechOS-$releasever-BaseOS]
name = UniontechOS $releasever BaseOS
#baseurl = https://enterprise-c-packages.chinauos.com/server-enterprise-c/kongzi/1020/BaseOS/$basearch
baseurl = file:///mnt/iso/BaseOS
enabled = 1
username=$auth_u
password=$auth_p
gpgkey = file:///etc/pki/rpm-gpg/RPM-GPG-KEY-uos-release
gpgcheck = 0
skip_if_unavailable = 1

[UniontechOS-$releasever-PowerTools]
name = UniontechOS $releasever PowerTools
baseurl = https://enterprise-c-packages.chinauos.com/server-enterprise-c/kongzi/1020/PowerTools/$basearch
enabled = 0
username=$auth_u
password=$auth_p
gpgkey = file:///etc/pki/rpm-gpg/RPM-GPG-KEY-uos-release
gpgcheck = 0
skip_if_unavailable = 1

[UniontechOS-$releasever-Plus]
name = UniontechOS $releasever Plus
baseurl = https://enterprise-c-packages.chinauos.com/server-enterprise-c/kongzi/1020/Plus/$basearch
enabled = 0
username=$auth_u
password=$auth_p
gpgkey = file:///etc/pki/rpm-gpg/RPM-GPG-KEY-uos-release
gpgcheck = 0
skip_if_unavailable = 1

[UniontechOS-$releasever-Extras]
name = UniontechOS $releasever Extras
baseurl = https://enterprise-c-packages.chinauos.com/server-enterprise-c/kongzi/1020/Extras/$basearch
enabled = 0
username=$auth_u
password=$auth_p
gpgkey = file:///etc/pki/rpm-gpg/RPM-GPG-KEY-uos-release
gpgcheck = 0
skip_if_unavailable = 1

[UniontechOS-$releasever-Update]
name = UniontechOS $releasever Update
baseurl = https://enterprise-c-packages.chinauos.com/server-enterprise-c/kongzi/1020/Update/$basearch
enabled = 0
username=$auth_u
password=$auth_p
gpgkey = file:///etc/pki/rpm-gpg/RPM-GPG-KEY-uos-release
gpgcheck = 0
skip_if_unavailable = 1

[UniontechOS-$releasever-HA]
name = UniontechOS $releasever HighAvailability
baseurl = https://enterprise-c-packages.chinauos.com/server-enterprise-c/kongzi/1020/HighAvailability/$basearch
enabled = 0
username=$auth_u
password=$auth_p
gpgkey = file:///etc/pki/rpm-gpg/RPM-GPG-KEY-uos-release
gpgcheck = 0
skip_if_unavailable = 1

[UniontechOS-$releasever-OpenStack-U]
name = UniontechOS $releasever OpenStack-Ussuri
baseurl = https://enterprise-c-packages.chinauos.com/server-enterprise-c/kongzi/1020/OpenStack-U/$basearch
enabled = 0
username=$auth_u
password=$auth_p
gpgkey = file:///etc/pki/rpm-gpg/RPM-GPG-KEY-uos-release
gpgcheck = 0
skip_if_unavailable = 1

'''


install_baseurl = "sed -i 's/\$releasever/20/' /etc/yum.repos.d/UniontechOS.repo"
yum_url="file:///mnt/iso/AppStream"

#Three base rpm download here
repostr_uos = '''[UniontechOS-AppStream]
name = UniontechOS AppStream
baseurl = file:///mnt/iso/AppStream
enabled = 1
gpgcheck = 0

[UniontechOS-BaseOS]
name = UniontechOS BaseOS
baseurl = file:///mnt/iso/BaseOS
enabled = 1
gpgcheck = 0
'''

old_packages = 'centos-backgrounds centos-logos centos-release centos-release-cr desktop-backgrounds-basic \
centos-release-advanced-virtualization centos-release-ansible26 centos-release-ansible-27 \
centos-release-ansible-28 centos-release-ansible-29 centos-release-azure \
centos-release-ceph-jewel centos-release-ceph-luminous centos-release-ceph-nautilus \
centos-release-ceph-octopus centos-release-configmanagement centos-release-dotnet centos-release-fdio \
centos-release-gluster40 centos-release-gluster41 centos-release-gluster5 \
centos-release-gluster6 centos-release-gluster7 centos-release-gluster8 \
centos-release-gluster-legacy centos-release-messaging centos-release-nfs-ganesha28 \
centos-release-nfs-ganesha30 centos-release-nfv-common \
centos-release-nfv-openvswitch centos-release-openshift-origin centos-release-openstack-queens \
centos-release-openstack-rocky centos-release-openstack-stein centos-release-openstack-train \
centos-release-openstack-ussuri centos-release-opstools centos-release-ovirt42 centos-release-ovirt43 \
centos-release-ovirt44 centos-release-paas-common centos-release-qemu-ev centos-release-qpid-proton \
centos-release-rabbitmq-38 centos-release-samba411 centos-release-samba412 \
centos-release-scl centos-release-scl-rh centos-release-storage-common \
centos-release-virt-common centos-release-xen centos-release-xen-410 \
centos-release-xen-412 centos-release-xen-46 centos-release-xen-48 centos-release-xen-common \
libreport-centos libreport-plugin-mantisbt libreport-plugin-rhtsupport python3-syspurpose \
python-oauth sl-logos yum-rhn-plugin'


reposdir=''

def local_repo():
    with open('UniontechOS.repo','w',encoding = 'utf-8-sig')as local_repo:
        local_repo.write(local_UniontechOS_repo)
    repo_str = '\cp UniontechOS.repo /etc/yum.repos.d/UniontechOS.repo'
    subprocess.run(repo_str,shell=True)

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

def main(reinstall_all_rpms=False, verify_all_rpms=False):
    global reposdir

    # check if the script is executed by root user
    print("Checking if the tool is executed by root user")
    if os.geteuid() != 0:
        print("Please run the tool as root user.")
        sys.exit(1)

    # check required packages
    print('Checking required packages')
    for pkg in ['rpm','yum','curl']:
        if not check_pkg(pkg):
            print("Could not found "+pkg)
            sys.exit(1)

    # display rpms info before conversion
    if verify_all_rpms:
        print("Creating a list of RPMs installed before the switch")
        print("Verifying RPMs installed before the switch against RPM database")
        out1 = subprocess.check_output('rpm -qa --qf \
               "%{NAME}|%{VERSION}|%{RELEASE}|%{INSTALLTIME}|%{VENDOR}|%{BUILDTIME}|%{BUILDHOST}|%{SOURCERPM}|%{LICENSE}|%{PACKAGER}\\n" \
               | sort > "/var/tmp/$(hostname)-rpms-list-before.log"', shell=True)
        out2 = subprocess.check_output('rpm -Va | sort -k3 > "/var/tmp/$(hostname)-rpms-verified-before.log"',shell=True)
        files = os.listdir('/var/tmp/')
        hostname = socket.gethostname()
        print("Review the output of following files:")
        for f in files:
            if re.match(hostname+'-rpms-(.*)\.log', f):
                print(f)



    # check if the os old_version is supported
    print("========= Checking: distribution =========")
    old_version = subprocess.check_output("rpm -q --whatprovides /etc/redhat-release", shell=True)
    old_version = str(old_version, 'utf-8')
    old_version = old_version.split('\n')[:-1]
    if len(old_version) == 0:
        print("You appear to be running an unsupported distribution.")
        sys.exit(1)
    if len(old_version) > 1:
        print("Could not determine your distribution because multiple packages are providing redhat-release:")
        print('\n'.join(old_version))
        sys.exit(1)

    old_version = old_version[0]
    if re.match('uos-release', old_version):
        print("You are already using Uniontech.")
        sys.exit(1)
    
    elif re.match('centos-linux-release', old_version):
        subver = old_version.split('-')[3]
    
    elif re.match('redhat-release|centos-release|sl-release', old_version):
        subver = old_version.split('-')[2]
        
    else:
        print("Your are using an unsupported distribution.")
        sys.exit(1)

    if not re.match('8',subver):
        print("You appear to be running an unsupported distribution.")
        sys.exit(1)

    print("========= Checking: required python packages =========")
    if not check_pkg('/usr/libexec/platform-python'):
        print('/usr/libexec/platform-python not found.')
        sys.exit(1)

    base_packages=['basesystem','initscripts','uos-logos','plymouth','grub2','grubby']

    print("========= Checking: yum lock ===========")
    if os.path.exists('/var/run/yum.pid'):
        with open('/var/run/yum.pid', 'r') as f:
            pid = f.read()
            with open('/proc/'+pid+'/comm', 'r') as ff:
                comm = ff.read()
                print('Another app is currently holding the yum lock: '+comm)
                print('Running as pid: '+pid)
                print('Please kill it and run the tool again.')
        sys.exit(1)

    # check dnf
    if re.match('8\.',subver):
        print("========= Checking: dnf =========")
        print("Identifying dnf modules that are enabled...")
        enabled_modules = str(
            subprocess.check_output("dnf module list --enabled | grep rhel | awk '{print $1}'", shell=True), 
            'utf-8')
        enabled_modules = enabled_modules.split('\n')[:-1]
        unknown_mods=[]
        if len(enabled_modules) > 0:
            for mod in enabled_modules:
                if re.fullmatch('container-tools|llvm-toolset| perl-DBD-SQLite|perl-DBI|satellite-5-client|perl', mod):
                    subprocess.run('dnf module reset -y '+mod, shell=True)
                if not re.fullmatch('container-tools|go-toolset|jmc|llvm-toolset|rust-toolset|virt', mod):
                    unknown_mods.append(mod)
            if len(unknown_mods) > 0:
                print('This tool is unable to automatically switch module(s) ' \
                + ','.join(unknown_mods) \
                + ' from a CentOS \'rhel\' stream to an UniontechOS equivalent.'\
                )
                opt = input('Do you want to continue and resolve it manually? (Yes or No)\n' )
                if opt != 'Yes':
                    sys.exit(1)

    print("========= Finding your repository directory =========")
    if re.match('8\.',subver):
        dir = dnf.Base().conf.get_reposdir
        if os.path.isdir(dir):
            reposdir = dir
        else:
            print("repository directory not found")
            sys.exit(1)

    print("========= Learning which repositories are enabled ==========")
    if re.match('8\.',subver):
        base = dnf.Base()
        base.read_all_repos()
        enabled_repos = []
        for repo in base.repos.iter_enabled():
            enabled_repos.append(repo.id)
    print("Repositories enabled before update include:")
    print(enabled_repos)

    if len(reposdir) == 0:
        print("Could not locate your repository directory.")
        sys.exit(1)

    if re.match('8\.',subver):
        repofile = os.path.join(reposdir, 'switch-to-uos.repo')
        with open(repofile, 'w') as f:
            f.write(repostr_uos)

    os.system('yum -y install uos-license-mini license-config ')
    print("========= Looking for yumdownloader ==========")
    if not check_pkg('yumdownloader'):
        subprocess.run("yum -y install yum-utils --disablerepo C* || true", shell=True)
        if not check_pkg('yumdownloader'):
            clean_and_exit()

    print("========= Start converting =========")
    if re.match('centos-release-8\.*|centos-linux-release-8\.*', old_version):
        old_version = subprocess.check_output('rpm -qa centos*repos', shell=True)
        old_version = str(old_version, 'utf-8')[:-1]

    print("Backing up and removing old repository files...")
    try:
        repos = subprocess.check_output("rpm -ql "+old_version+" | grep '\.repo$'", shell=True)
        pass
    except Exception:
        os.system('yum -y install centos-linux-repos')
        old_version = subprocess.check_output('rpm -qa centos*repos', shell=True)
        old_version = str(old_version, 'utf-8')[:-1]
        repos = subprocess.check_output("rpm -ql "+old_version+" | grep '\.repo$'", shell=True)
    repos = str(repos, 'utf-8').split('\n')[:-1]
    num_centos_repos = subprocess.check_output('rpm -qa "centos-release-*" | wc -l', shell=True)
    if int(str(num_centos_repos,'utf-8')[0]) > 0:
        addtional_repos = subprocess.check_output('rpm -qla "centos-release-*"', shell=True)
        addtional_repos = str(addtional_repos, 'utf-8')
        if addtional_repos != '':
            addtional_repos = addtional_repos.split('\n')
            for r in addtional_repos:
                if re.match('.*\.repo$', r):
                    repos.append(r)

    backup_comment = '# This is a yum repository file that was disabled by\n' \
    + '# ' + __file__+ ', a script to convert CentOS to Uniontech.\n' \
    + '# Please see '+yum_url+' for more information.\n\n'

    for repo in repos:
        if not os.path.isfile(repo):
            continue
        with open(repo, 'r') as fsrc:
            content = fsrc.read()
            with open(repo+'.disabled','w') as fdst:
                fdst.write(repo+'\n'+backup_comment+content)
        os.remove(repo)

    print("Removing CentOS-specific yum configuration from /etc/yum.conf ...")
    with open('/etc/yum.conf', 'r') as f:
        content = f.read()
    if re.search(r'^distroverpkg=', content, re.MULTILINE):
        content = re.sub(r"\n(distroverpkg=)", r"\n#\1", content)
    if re.search(r'bugtracker_url=', content, re.MULTILINE):
        content = re.sub(r"\n(bugtracker_url=)", r"\n#\1", content)
    with open('/etc/yum.conf', 'w') as f:
        f.write(content)
     
    print("Downloading uos release package...")   
    dst_release = ['uos-release']
    try:
        stat = subprocess.check_output("yumdownloader "+' '.join(dst_release), shell=True)
        pass
    except Exception:
        print("Could not download the following packages from " + yum_url)
        print('\n'.join(dst_release))
        print()
        print("Are you behind a proxy? If so, make sure the 'http_proxy' environmen")
        print("variable is set with your proxy address.")
        print("An error occurred while attempting to switch this system to Uniontech" + \
        "and it may be in an unstable/unbootable state. To avoid further issues, " +\
        "the script has terminated.")

    dst_rpms = [s+'*.rpm' for s in dst_release]
    subprocess.run('rpm -e --nodeps ' + old_version + ' centos-gpg-keys', shell=True)
    subprocess.run('rpm -i --force ' + ' '.join(dst_rpms) + ' --nodeps', shell=True)
    local_repo()
    subprocess.run(install_baseurl,shell=True)
    os.remove(repofile)
    # switch completed

    repositories={}
    if re.match('8\.',subver):
        repositories['AppStream'] = 'REPO AppStream'
        repositories['BaseOS'] = 'REPO BaseOS'
        repositories['PowerTools'] = 'REPO PowerTools'

    for repo in enabled_repos:
        if repo in repositories:
            action = repositories[repo].split(' ')
            if action[0] == 'REPO':
                if re.match('https\..*', action[1]):
                    subprocess.run('yum-config-manager --add-repo '+action[1], shell=True)
                else:
                    subprocess.run('yum-config-manager --enable '+action[1], shell=True)
            elif action[0] == 'RPM':
                subprocess.run('yum --assumeyes install '+action[1], shell=True)

    cmd='yum shell -y <<EOF\n\
remove '+ old_packages +'\n\
install '+ ' '.join(base_packages) + '\n\
run\n\
EOF'
    try:
        subprocess.run(cmd, shell=True)
    except:
        sys.exit(1)

    if os.access('/usr/libexec/plymouth/plymouth-update-initrd', os.X_OK):
        os.system('rpm -e --nodeps centos-indexhtml')
        subprocess.run('/usr/libexec/plymouth/plymouth-update-initrd')

    if subver == '8.3':
        subprocess.run('yum -y downgrade crypto-policies --allowerasing', shell=True)

    try:
        subprocess.run('yum -y distro-sync', shell=True)
    except:
        print("Could not automatically sync with UniontechOS repositories.\n\
        Check the output of 'yum distro-sync' to manually resolve the issue.")
        sys.exit(1)


    if re.match('8\.',subver):
        if len(enabled_modules) > 0:
            for mod in enabled_modules:
                subprocess.run('dnf module reset -y '+mod, shell=True)
                if re.fullmatch('container-tools|go-toolset|jmc|llvm-toolset|rust-toolset', mod):
                    subprocess.run('dnf module install -y '+mod+':uelc20', shell=True)
                elif mod =='virt':
                    subprocess.run('dnf module install -y '+mod+':uelc', shell=True)
                else:
                    print("Unsure how to transform module"+mod)
            #subprocess.run('dnf --assumeyes --disablerepo "*" --enablerepo "AppStream" update', shell=True)
            subprocess.run('dnf -y update', shell=True)
        try:
            subprocess.check_call('dnf module list --enabled | grep satellite-5-client', shell=True)
            subprocess.run('dnf module disable -y satellite-5-client', shell=True)
        except:
            pass

    try:
        subprocess.check_call('rpm -q centos-logos-ipa', shell=True)
        subprocess.run('dnf swap -y centos-logos-ipa uos-logos-ipa', shell=True)
    except:
        pass
    
    try:
        subprocess.check_call('rpm -q centos-logos-httpd', shell=True)
        subprocess.run('dnf swap -y centos-logos-httpd uos-logos-httpd', shell=True)
    except:
        pass

    try:
        subprocess.check_call('rpm -q redhat-lsb-core', shell=True)
        subprocess.run('dnf swap -y redhat-lsb-core uos-lsb-core', shell=True)
        subprocess.run('dnf swap -y redhat-lsb-submod-security uos-lsb-submod-security',shell=True)
    except:
        pass

    try:
        subprocess.check_call('rpm -q rhn-client-tools', shell=True)
        print("rhn related packages is not provided by Uniontech")
        subprocess.run('dnf -y remove rhn-client-tools python3-rhn-client-tools python3-rhnlib', shell=True)
    except:
        pass

    try:
        subprocess.check_call('rpm -q gpg-pubkey --qf "%{NAME}-%{VERSION}-%{RELEASE} %{PACKAGER}\\n" | grep CentOS', shell=True)
        print("remove centos gpg-pubkey")
        subprocess.run('rpm -e $(rpm -q gpg-pubkey --qf "%{NAME}-%{VERSION}-%{RELEASE} %{PACKAGER}\\n" | grep CentOS | awk \'{print $1}\')', shell=True)
    except:
        pass

    if reinstall_all_rpms:
        centos_rpms = subprocess.check_output('rpm -qa --qf "%{NAME}-%{VERSION}-%{RELEASE} %{VENDOR}\n" \
        | grep CentOS | grep -v kernel | awk \'{print $1}\'', \
        shell=True)
        centos_rpms = str(centos_rpms,'utf-8')
        centos_rpms = centos_rpms.split('\n')[:-1]
        if len(centos_rpms) > 0:
            print("Reinstalling RPMs:")
            print(' '.join(centos_rpms))
            subprocess.run('yum --assumeyes reinstall '+ ' '.join(centos_rpms), shell=True)

        non_uos_rpms = subprocess.check_output('rpm -qa --qf "%{NAME}-%{VERSION}-%{RELEASE}|%{VENDOR}|%{PACKAGER}\\n" \
        |grep -v Uniontech', shell=True)
        non_uos_rpms = str(non_uos_rpms, 'utf-8')
        non_uos_rpms = non_uos_rpms.split('\n')[:-1]
        if len(non_uos_rpms) > 0:
            print("The following non-UniontechOS RPMs are installed on the system:")
            print(' '.join(non_uos_rpms))
            print("This may be expected of your environment and does not necessarily indicate a problem.")

    if os.path.isfile('/var/cache/yum'):
        os.remove('/var/cache/yum')
    elif os.path.isdir('/var/cache/yum'):
        shutil.rmtree('/var/cache/yum')
    if os.path.isfile('/var/cache/dnf'):
        os.remove('/var/cache/dnf')
    elif os.path.isdir('/var/cache/dnf'):
        shutil.rmtree('/var/cache/dnf')

    if verify_all_rpms:
        out1 = subprocess.check_output('rpm -qa --qf \
        "%{NAME}|%{VERSION}|%{RELEASE}|%{INSTALLTIME}|%{VENDOR}|%{BUILDTIME}|%{BUILDHOST}|%{SOURCERPM}|%{LICENSE}|%{PACKAGER}\\n" \
        | sort > "/var/tmp/$(hostname)-rpms-list-after.log"', shell=True)
        out2 = subprocess.check_output('rpm -Va | sort -k3 > "/var/tmp/$(hostname)-rpms-verified-after.log"',shell=True)
        files = os.listdir('/var/tmp/')
        hostname = socket.gethostname()
        for f in files:
            if re.match(hostname+'-rpms-(.*)\.log', f):
                print(f)

    if os.path.isdir('/sys/firmware/efi'):
        subprocess.run('grub2-mkconfig -o /boot/efi/EFI/uos/grub.cfg', shell=True)
        add_boot_option()
    else:
        subprocess.run('grub2-mkconfig -o /boot/grub2/grub.cfg', shell=True)
    os.system('grep -rl "CentOS" /boot/loader | xargs -i rm -rf {}')
    print("Switch complete.UniontechOS recommends rebooting this system.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', action='store_true', help='reinstall all CentOS RPMs with UniontechOS RPMs (Note: This is not necessary for support)')
    parser.add_argument('-V', action='store_true', help='Verify RPM information before and after the switch')
    args=parser.parse_args()
    sys.exit(main(args.r, args.V))
