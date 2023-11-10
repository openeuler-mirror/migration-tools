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
os.chdir('/usr/lib/migration-tools-agent')
sys.path.append('/usr/lib/migration-tools-agent')
from settings import install_baseurl, repostr_uos, old_packages, yum_url


repos_dir = ''


def run_cmd(args):
    process = subprocess.Popen(args,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               close_fds=True,
                               shell=False,
                               encoding='utf-8',
                               universal_newlines=False
                               )
    out_std, out_err = process.communicate()
    retval = process.returncode
    return out_std, out_err, retval


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
    global repos_dir
    repo_path = os.path.join(repos_dir, 'switch-to-uos.repo')
    if os.path.exists(repo_path):
        os.remove(repo_path)
    sys.exit(1)


def get_disk_info(string):
    dev_name = ""
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


def main(reinstall_all_rpms=False, verify_all_rpms=False):
    global repos_dir

    # check if the script is executed by root user
    print("Checking if the tool is executed by root user")
    if os.geteuid() != 0:
        print("Please run the tool as root user.")
        sys.exit(1)

    # check required packages
    print('Checking required packages')
    for pkg in ['rpm', 'yum', 'curl']:
        if not check_pkg(pkg):
            print("Could not found "+pkg)
            sys.exit(1)

    # display rpms info before conversion
    if verify_all_rpms:
        print("Creating a list of RPMs installed before the switch")
        print("Verifying RPMs installed before the switch against RPM database")
        subprocess.check_output('rpm -qa --qf \
               "%{NAME}|%{VERSION}|%{RELEASE}|%{INSTALLTIME}|%{VENDOR}|%{BUILDTIME}|%{BUILDHOST}|%{SOURCERPM}|%{LICENSE}|%{PACKAGER}\\n" \
               | sort > "/var/tmp/$(hostname)-rpms-list-before.log"', shell=True)
        subprocess.check_output('rpm -Va | sort -k3 > "/var/tmp/$(hostname)-rpms-verified-before.log"', shell=True)
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

    base_packages = ['basesystem', 'initscripts', 'uos-logos', 'plymouth', 'grub2', 'grubby']

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
    if re.match('8\.', subver):
        print("========= Checking: dnf =========")
        print("Identifying dnf modules that are enabled...")
        enabled_modules = str(
            subprocess.check_output("dnf module list --enabled | grep rhel | awk '{print $1}'", shell=True), 
            'utf-8')
        enabled_modules = enabled_modules.split('\n')[:-1]
        unknown_mods = []
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
    if re.match('8\.', subver):
        dir = dnf.Base().conf.get_repos_dir
        if os.path.isdir(dir):
            repos_dir = dir
        else:
            print("repository directory not found")
            sys.exit(1)

    print("========= Learning which repositories are enabled ==========")
    if re.match('8\.', subver):
        base = dnf.Base()
        base.read_all_repos()
        enabled_repos = []
        for repo in base.repos.iter_enabled():
            enabled_repos.append(repo.id)
    print("Repositories enabled before update include:")
    print(enabled_repos)

    if len(repos_dir) == 0:
        print("Could not locate your repository directory.")
        sys.exit(1)

    if re.match('8\.', subver):
        repo_file = os.path.join(repos_dir, 'switch-to-uos.repo')
        with open(repo_file, 'w') as f:
            f.write(repostr_uos)

    os.system("sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*")
    os.system("sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*")

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
        subprocess.check_output("yumdownloader "+' '.join(dst_release), shell=True)
        pass
    except Exception:
        print("Could not download the following packages from " + yum_url)
        print('\n'.join(dst_release))
        print("Are you behind a proxy? If so, make sure the 'http_proxy' environmen")
        print("variable is set with your proxy address.")
        print("An error occurred while attempting to switch this system to Uniontech" + \
        "and it may be in an unstable/unbootable state. To avoid further issues, " +\
        "the script has terminated.")

    print("Switching old release package with Uniontech...")
    dst_rpms = [s+'*.rpm' for s in dst_release]
    subprocess.run('rpm -e --nodeps ' + old_version + ' centos-gpg-keys', shell=True)
    subprocess.run('rpm -i --force ' + ' '.join(dst_rpms) + ' --nodeps', shell=True)
    subprocess.run(install_baseurl, shell=True)
    os.remove('/etc/yum.repos.d/UniontechOS.repo')

    repositories={}
    if re.match('8\.', subver):
        repositories['AppStream'] = 'REPO AppStream'
        repositories['BaseOS'] = 'REPO BaseOS'
        repositories['PowerTools'] = 'REPO PowerTools'

    for repo in enabled_repos:
        if repo in repositories:
            action = repositories[repo].split(' ')
            if action[0] == 'REPO':
                print('Enabling ' + action[1] + 'which replaces ' + repo)
                if re.match('https\..*', action[1]):
                    subprocess.run('yum-config-manager --add-repo '+action[1], shell=True)
                else:
                    subprocess.run('yum-config-manager --enable '+action[1], shell=True)
            elif action[0] == 'RPM':
                print('Installing ' + action[1] + ' to get content that replaces ' + repo)
                subprocess.run('yum --assumeyes install '+action[1], shell=True)

    print("Installing base packages for UniontechOS...")
    cmd='yum shell -y <<EOF\n\
remove '+ old_packages +'\n\
install '+ ' '.join(base_packages) + '\n\
run\n\
EOF'
    try:
        subprocess.run(cmd, shell=True)
    except:
        print("Could not install base packages.Run 'yum distro-sync' to manually install them.")
        sys.exit(1)

    if os.access('/usr/libexec/plymouth/plymouth-update-initrd', os.X_OK):
        print("Updating initrd...")
        os.system('rpm -e --nodeps centos-indexhtml')
        subprocess.run('/usr/libexec/plymouth/plymouth-update-initrd')
        print("Switch successful. Syncing with UniontechOS repositories.")

    if subver == '8.3':
        subprocess.run('yum -y downgrade crypto-policies --allowerasing', shell=True)

    out_std, out_err, retval = run_cmd(["yum", "list", "kernel-headers"])
    if retval != 0:
        print("Unable to find kernel-headers in repository")
        sys.exit(1)

    try:
        subprocess.run('yum -y distro-sync', shell=True)
    except:
        print("Could not automatically sync with UniontechOS repositories.\n\
        Check the output of 'yum distro-sync' to manually resolve the issue.")
        sys.exit(1)

    if re.match('8\.', subver):
        if len(enabled_modules) > 0:
            for mod in enabled_modules:
                subprocess.run('dnf module reset -y '+mod, shell=True)
                if re.fullmatch('container-tools|go-toolset|jmc|llvm-toolset|rust-toolset', mod):
                    subprocess.run('dnf module install -y '+mod+':uelc20', shell=True)
                elif mod == 'virt':
                    subprocess.run('dnf module install -y '+mod+':uelc', shell=True)
                else:
                    print("Unsure how to transform module"+mod)
            subprocess.run('dnf -y update', shell=True)
        try:
            subprocess.check_call('dnf module list --enabled | grep satellite-5-client', shell=True)
            print("UniontechOS does not provide satellite-5-client module, disable it.")
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
        print("redhat-lsb is replaced by system-lsb on uos")
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
        print("Testing for remaining CentOS RPMs")
        centos_rpms = subprocess.check_output('rpm -qa --qf "%{NAME}-%{VERSION}-%{RELEASE} %{VENDOR}\n" \
        | grep CentOS | grep -v kernel | awk \'{print $1}\'', \
        shell=True)
        centos_rpms = str(centos_rpms,'utf-8')
        centos_rpms = centos_rpms.split('\n')[:-1]
        if len(centos_rpms) > 0:
            print("Reinstalling RPMs:")
            print(' '.join(centos_rpms))
            subprocess.run('yum --assumeyes reinstall ' + ' '.join(centos_rpms), shell=True)

        non_uos_rpms = subprocess.check_output('rpm -qa --qf "%{NAME}-%{VERSION}-%{RELEASE}|%{VENDOR}|%{PACKAGER}\\n" \
        |grep -v Uniontech', shell=True)
        non_uos_rpms = str(non_uos_rpms, 'utf-8')
        non_uos_rpms = non_uos_rpms.split('\n')[:-1]
        if len(non_uos_rpms) > 0:
            print("The following non-UniontechOS RPMs are installed on the system:")
            print(' '.join(non_uos_rpms))
            print("This may be expected of your environment and does not necessarily indicate a problem.")

    print("Removing yum cache")
    if os.path.isfile('/var/cache/yum'):
        os.remove('/var/cache/yum')
    elif os.path.isdir('/var/cache/yum'):
        shutil.rmtree('/var/cache/yum')
    if os.path.isfile('/var/cache/dnf'):
        os.remove('/var/cache/dnf')
    elif os.path.isdir('/var/cache/dnf'):
        shutil.rmtree('/var/cache/dnf')

    if verify_all_rpms:
        print("Creating a list of RPMs installed after the switch")
        print("Verifying RPMs installed after the switch against RPM database")
        subprocess.check_output('rpm -qa --qf \
        "%{NAME}|%{VERSION}|%{RELEASE}|%{INSTALLTIME}|%{VENDOR}|%{BUILDTIME}|%{BUILDHOST}|%{SOURCERPM}|%{LICENSE}|%{PACKAGER}\\n" \
        | sort > "/var/tmp/$(hostname)-rpms-list-after.log"', shell=True)
        subprocess.check_output('rpm -Va | sort -k3 > "/var/tmp/$(hostname)-rpms-verified-after.log"',shell=True)
        files = os.listdir('/var/tmp/')
        hostname = socket.gethostname()
        print("Review the output of following files:")
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
    parser.add_argument('-r', action='store_true', help='reinstall all CentOS RPMs with UniontechOS RPMs'
                                                        ' (Note: This is not necessary for support)')
    parser.add_argument('-V', action='store_true', help='Verify RPM information before and after the switch')
    args = parser.parse_args()
    sys.exit(main(args.r, args.V))
