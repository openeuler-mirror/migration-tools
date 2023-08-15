#!/usr/libexec/platform-python

import os
import subprocess
import re
import socket
import sys
import shutil
import argparse
import platform
import logging
reposdir=''

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


def get_bad_packages():
    os_version_ret = platform.dist()
    version = os_version_ret[1].split('.',-1)
    local_os_version = version[0]
    badpackages = ''
    if '8' == local_os_version:
        with open('func/8badpackage.txt','r') as bf:
            for bad_package in bf:
                badpackages = badpackages + ' ' + bad_package.strip()
            bf.close()
    else:
        with open('func/7badpackage.txt','r') as bf:
            for bad_package in bf:
                badpackages = badpackages + ' ' + bad_package.strip()
            bf.close()
    return badpackages


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
    global reposdir
    repo_path = os.path.join(reposdir, 'switch-to-uos.repo')
    if os.path.exists(repo_path):
        os.remove(repo_path)
    sys.exit(1)


def process_special_pkgs():
    print("swap *-logos related packages with UniontechOS packages")
    subprocess.run('rpm -q centos-logos-ipa && dnf swap -y centos-logos-ipa uos-logos-ipa', shell=True)
    subprocess.run('rpm -q centos-logos-httpd && dnf swap -y centos-logos-httpd uos-logos-httpd', shell=True)				
    print("redhat-lsb is replaced by system-lsb on UniontechOS")
    subprocess.run('rpm -q redhat-lsb-core && dnf swap -y redhat-lsb-core system-lsb-core', shell=True)
    subprocess.run('rpm -q redhat-lsb-submod-security && dnf swap -y redhat-lsb-submod-security system-lsb-submod-security',shell=True)
    print("rhn related packages is not provided by UniontechOS")
    subprocess.run('rpm -q rhn-client-tools && dnf -y remove rhn-client-tools python3-rhn-client-tools python3-rhnlib', shell=True)		
    print("subscription-manager related packages is not provided by UniontechOS")
    subprocess.run('rpm -q subscription-manager && dnf -y remove subscription-manager', shell=True)
    print("python3-syspurpose is not provided by UniontechOS")
    subprocess.run('rpm -q python3-syspurpose && dnf -y remove python3-syspurpose', shell=True)
    print("remove centos gpg-pubkey")
    subprocess.run('rpm -e $(rpm -q gpg-pubkey --qf "%{NAME}-%{VERSION}-%{RELEASE} %{PACKAGER}\\n" | grep CentOS | awk \'{print $1}\')', shell=True)


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

def centos8_main(osname):
    global reposdir

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    #rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    log_name = '/var/tmp/uos-migration/UOS_migration_log/log'
    logfile = log_name
    fh = logging.FileHandler(logfile, mode='w')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)


    logger.info("Checking if the tool is executed by root user")
    # check if the script is executed by root user
    if os.geteuid() != 0:
        logger.info("Please run the tool as root user.")
        sys.exit(1)
    # check required packages
    logger.info('Checking required packages')
    for pkg in ['rpm','yum','curl']:
        if not check_pkg(pkg):
            logger.info("Could not found "+pkg)
            sys.exit(1)
    #sto system rpms info before migration
    pre_system_rpms_info()

    # check if the os old_version is supported
    logger.info("========= Checking: distribution =========")
    old_version = subprocess.check_output("rpm -q --whatprovides /etc/redhat-release", shell=True)
    old_version = str(old_version, 'utf-8')
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
    linux_release = osname+'-linux-release'
    if re.match('uos-release', old_version):
        logger.info("You are already using Uniontech.")
        sys.exit(1)
    elif re.match(linux_release, old_version):
        subver = old_version.split('-')[3]
    elif re.match(osrelease, old_version):
        subver = old_version.split('-')[2]
    else:
        logger.info("Your are using an unsupported distribution.")
        sys.exit(1)
    if not re.match('8',subver):
        logger.info("You appear to be running an unsupported distribution.")
        sys.exit(1)

    logger.info("========= Checking: required python packages =========")
    if not check_pkg('/usr/libexec/platform-python'):
        logger.info('/usr/libexec/platform-python not found.')
        sys.exit(1)
    base_packages=['basesystem','initscripts','uos-logos','plymouth','grub2','grubby']

    logger.info("========= Checking: yum lock ===========")
    if os.path.exists('/var/run/yum.pid'):
        with open('/var/run/yum.pid', 'r') as f:
            pid = f.read()
            f.close()
            with open('/proc/'+pid+'/comm', 'r') as ff:
                comm = ff.read()
                logger.info('Another app is currently holding the yum lock: '+comm)
                logger.info('Running as pid: '+pid)
                logger.info('Please kill it and run the tool again.')
                ff.close()
        sys.exit(1)

    # check dnf
    if re.match('8\.',subver):
        logger.info("========= Checking: dnf =========")
        logger.info("Identifying dnf modules that are enabled...")
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
                logger.info('This tool is unable to automatically switch module(s) ' \
                + ','.join(unknown_mods) \
                + ' from a CentOS \'rhel\' stream to an UniontechOS equivalent.'\
                )
                opt = input('Do you want to continue and resolve it manually? (Yes or No)\n' )
                if opt != 'Yes':
                    sys.exit(1)


    logger.info("========= Looking for yumdownloader ==========")
    os.system('yum -y install uos-license-mini license-config ')
    if not check_pkg('yumdownloader'):
        subprocess.run("yum -y install yum-utils --disablerepo C* || true", shell=True)

    logger.info("========= Start converting =========")
    if re.match(osname+'-release-8', old_version):
        repos = 'rpm -qa '+osname+'*repos'
        old_version = subprocess.check_output(repos, shell=True)
        old_version = str(old_version, 'utf-8')[:-1]
        subprocess.run('rpm -e --nodeps ' + old_version , shell=True)

    logger.info("Downloading uos release package...")
    dst_release = ['uos-release']
    try:
        stat = subprocess.check_output("yumdownloader "+' '.join(dst_release), shell=True)
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
        "and it may be in an unstable/unbootable state. To avoid further issues, " +\
        "the script has terminated.")

    logger.info("Switching old release package with Uniontech...")
    dst_rpms = [s+'*.rpm' for s in dst_release]
    oldkeys = osname+'-gpg-keys'
    subprocess.run('rpm -e --nodeps ' + oldkeys, shell=True)
    subprocess.run('rpm -i --force ' + ' '.join(dst_rpms) + ' --nodeps', shell=True)
    local_disabled_release_repo()
    logger.info("Installing base packages for UniontechOS...")
    cmd='yum shell -y <<EOF\n\
remove '+ badpackages +'\n\
install '+ ' '.join(base_packages) + '\n\
run\n\
EOF'
    try:
        fdout = open("/var/tmp/uos-migration/UOS_migration_log/mig_log.txt",'a')
        subprocess.run(cmd,stdout=fdout , shell=True)
        fdout.close()
    except:
        logger.info("Could not install base packages.Run 'yum distro-sync' to manually install them.")
        sys.exit(1)

    if os.access('/usr/libexec/plymouth/plymouth-update-initrd', os.X_OK):
        logger.info("Updating initrd...")
        indexhtml ='rpm -e --nodeps ' + osname+'-indexhtml'
        os.system(indexhtml)
        fdout = open("/var/tmp/uos-migration/UOS_migration_log/mig_log.txt",'a')
        subprocess.run('/usr/libexec/plymouth/plymouth-update-initrd',stdout=fdout,shell=True)
        #run_cmd2file('/usr/libexec/plymouth/plymouth-update-initrd')
        fdout.close()
    logger.info("Switch successful. Syncing with UniontechOS repositories.")
    logger.debug('358')

    if subver == '8.3':
        subprocess.run('yum -y downgrade crypto-policies --allowerasing', shell=True)
    try:
        fdout = open("/var/tmp/uos-migration/UOS_migration_log/mig_log.txt",'a')
        subprocess.run('yum -y distro-sync', stdout=fdout ,shell=True)
        fdout.close()
    except:
        logger.info("error distro-sync migration ....")
    messageState('2')


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
            subprocess.run('yum --assumeyes reinstall '+ ' '.join(centos_rpms), shell=True)

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
        out1 = subprocess.check_output('rpm -qa --qf \
        "%{NAME}|%{VERSION}|%{RELEASE}|%{INSTALLTIME}|%{VENDOR}|%{BUILDTIME}|%{BUILDHOST}|%{SOURCERPM}|%{LICENSE}|%{PACKAGER}\\n" \
        | sort > "/var/tmp/$(hostname)-rpms-list-after.log"', shell=True)
        out2 = subprocess.check_output('rpm -Va | sort -k3 > "/var/tmp/$(hostname)-rpms-verified-after.log"',shell=True)
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
    parser.add_argument('-r', action='store_true', help='reinstall all CentOS RPMs with UniontechOS RPMs (Note: This is not necessary for support)')
    parser.add_argument('-V', action='store_true', help='Verify RPM information before and after the switch')
    args=parser.parse_args()
    sys.exit(main(args.r, args.V))
