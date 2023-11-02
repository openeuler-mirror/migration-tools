# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier:   MulanPubL-2.0-or-later
import os
import platform
import shutil
import subprocess
import logging


mig_log = '/var/tmp/uos-migration/UOS_migration_log/mig_log.txt'
if not os.path.exists(mig_log):
    os.system('mkdir -p /var/tmp/uos-migration/UOS_migration_log/')
    os.system('touch /var/tmp/uos-migration/UOS_migration_log/mig_log.txt')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler(mig_log)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

openeuler_repo = '''[openeuler]
name = openeuler
baseurl = http://mirrors.tuna.tsinghua.edu.cn/openeuler/openEuler-20.03-LTS-SP1/everything/$basearch
enabled = 1
gpgcheck = 0
'''


def check_migration_progress(message):
    with open('/var/tmp/uos-migration/.progress', 'w') as fp:
        fp.write(message)
        fp.close()


def run_subprocess(cmd):
    try:
        process = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,  # Avoid using shell=True
            check=True    # Check for non-zero return code and raise exception if found
        )
        output = process.stdout
        logger.info(output)
        return output, process.returncode
    except subprocess.CalledProcessError as e:
        logger.error(e.stderr)
        return e.stderr, e.returncode


def check_pkg(rpm):
    _, ret = run_subprocess('rpm -q {}'.format(rpm).split())
    if ret:
        return
    return True


def get_disk_info(string):
    dev_name = ""
    part_num = ""
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


def add_boot_option():
    """
    Current system is uefi, add boot option to boot manager.
    """
    subprocess.run('which efibootmgr > /dev/null 2>&1 || dnf install -y efibootmgr', shell=True)
    disk_name = subprocess.check_output('mount | grep /boot/efi | awk \'{print $1}\'', shell=True)
    disk_name = str(disk_name, 'utf-8')
    disk_name = disk_name.split('\n')[0]
    dev_name, part_num = get_disk_info(disk_name)
    if dev_name == "" or part_num == "":
        # Parse /boot/efi disk info failed, update boot loader failed.
        return

    cmd = ""
    arch = platform.machine()
    openEuler_path = '/boot/efi/EFI/openEuler'
    if os.path.exists(openEuler_path):
        efi_name = 'openEuler'
    else:
        efi_name = 'uos'
    if arch == "x86_64":
        cmd = 'efibootmgr -c -d ' + dev_name + ' -p ' + part_num + ' -l "/EFI/{}/grubx86.efi" -L "openEuler"'.format(
            efi_name)
    elif arch == "aarch64":
        cmd = 'efibootmgr -c -d ' + dev_name + ' -p ' + part_num + ' -l "/EFI/{}/grubaa64.efi" -L "openEuler"'.format(
            efi_name)
    try:
        run_subprocess(cmd.split())
    except Exception as e:
        logger.error(e)


def swap_release(release):
    tmp_dir = '/var/tmp'
    rpme_release = 'rpm -qf /etc/os-release | xargs -i rpm -e --nodeps {}'
    os.system(rpme_release)
    check_migration_progress('8')
    cmd = 'yumdownloader {} --destdir {}'.format(release, tmp_dir)
    run_subprocess(cmd.split())
    run_subprocess('rpm -ivh {}/*.rpm --nodeps --force'.format(tmp_dir).split())


def set_grub_biosdev_rules():
    """
    Set grub bisodev rule which can be don`t modify network configuration names.
    When the leapp has been made initrd, the function will set net.ifnames in /etc/default/grub.
    Returns:
    """
    default_grub_path = "/etc/default/grub"
    set_content = "net.ifnames=0  biosdevname=0"
    if not os.path.exists(default_grub_path):
        return
    with open(default_grub_path, 'r') as gf:
        gret = gf.readlines()
        gf.close()
    grub_content = ''
    for i in range(len(gret)):
        if "GRUB_CMDLINE_LINUX" in gret[i]:
            cmdline_tmp = gret[i].split('"', -1)[1]
            grub_content += 'GRUB_CMDLINE_LINUX="' + cmdline_tmp + ' ' + set_content + '"\n'
            continue
        grub_content += gret[i]
    try:
        if not os.path.exists(default_grub_path + '.disable'):
            shutil.copyfile(default_grub_path, default_grub_path + '.disable')
            os.remove(default_grub_path)
        else:
            logger.info("grub file has been modified")
            return
    except Exception as e:
        logger.error(e)
        return
    with open(default_grub_path, 'w+') as wgf:
        wgf.write(grub_content)
        wgf.close()
    return True


def conf_grub():
    if os.path.isdir('/sys/firmware/efi'):
        old_kernel = '3.10.0'
        if old_kernel:
            run_subprocess('rpm -e --nodeps kernel-{}'.format(old_kernel).split())
            run_subprocess('dnf install -y shim'.split())
        openEuler_path = '/boot/efi/EFI/openEuler'
        run_subprocess('grub2-mkconfig -o {}/grub.cfg'.format(openEuler_path).split())
        add_boot_option()
    else:
        run_subprocess('grub2-mkconfig -o /boot/grub2/grub.cfg'.split())
        try:
            run_subprocess('test -L /boot/grub2/grubenv'.split())
            run_subprocess('mv /boot/grub2/grubenv /boot/grub2/grubenv-bak'.split())
            run_subprocess('cat /boot/grub2/grubenv-bak > /boot/grub2/grubenv'.split())
        except Exception as e:
            logger.error(e)


def system_sync():
    subprocess.run('rpm --rebuilddb', shell=True)
    subprocess.run('dnf clean all', shell=True)
    cmd = 'dnf -y distro-sync --allowerasing --skip-broken'
    subprocess.run(cmd, shell=True)
    _, ret = run_subprocess('rpm -q kernel | grep oe1'.split())
    if ret:
        return False
    return True


def main():
    mig_log = '/var/tmp/uos-migration/UOS_migration_log/mig_log.txt'
    if not os.path.exists(mig_log):
        os.system('mkdir -p /var/tmp/uos-migration/UOS_migration_log/')
        os.system('touch /var/tmp/uos-migration/UOS_migration_log/mig_log.txt')

    check_migration_progress('5')
    if not check_pkg("yum-utils"):
        logger.error("please install yum-utils")
        return

    if not check_pkg('rsync'):
        logger.error('please install rsync')
        return
    
    if not check_pkg('python3'):
        logger.error('please install python3')
        return

    if not check_pkg('dnf'):
        logger.error('please install dnf')
        return
    paramiko_rpm_pwd = "/usr/lib/migration-tools-agent/agent-requires/paramiko/*.rpm"
    os.system('rpm -Uvh %s --force' % paramiko_rpm_pwd)
    remove_rpm_nodeps = 'rpm -e python-enum34 python-backports --nodeps'
    os.system(remove_rpm_nodeps)
    # disable centos repository
    os.system("yum-config-manager --disable base updates extras")

    repo_file = "/etc/yum.repos.d/openeuler.repo"
    with open(repo_file, 'w') as f:
        f.write(openeuler_repo)

    openEuler_release = 'openEuler-release'
    if not check_pkg(openEuler_release):
        logger.info("swaping release")
        swap_release(openEuler_release)
    check_migration_progress('10')
    # install basic packages
    os.system("yum install -y gdbm-help")
    check_migration_progress('15')
    remove_packages_nodeps = ['gdm', 'centos-logos', 'redhat-logos', 
                                'iwl7265-firmware', 'ivtv-firmware', 
                                'sysvinit-tools', 'sg3_utils-libs']
    for package in remove_packages_nodeps:
        nodeps_cmd = "rpm -q " + package + " && rpm -e --nodeps " + package
        os.system(nodeps_cmd)

        install_dir = os.path.join(os.path.dirname('/var/tmp'), 'DNF')
        if not os.path.exists(install_dir):
            os.makedirs(install_dir)
        else:
            shutil.rmtree(install_dir)
    check_migration_progress('30')
    install_cmd = 'yum install -y systemd python3-libdnf libreport-filesystem python3-gpg libmodulemd deltarpm python3-hawkey \
                    python3-libcomps python3-rpm util-linux --installroot={}'.format(install_dir)
    os.system(install_cmd)
    check_migration_progress('40')
    # download dnf
    download_dnf = '/usr/bin/yumdownloader {} --destdir={}'.format('dnf python3-dnf dnf-help', os.path.join(install_dir, 'root'))
    os.system(download_dnf)

    # rebuild dnfdb
    subprocess.run("/sbin/chroot /var/DNF /bin/bash -c 'rpm --rebuilddb'", shell=True)
    # install dnf 
    subprocess.run("/sbin/chroot /var/DNF /bin/bash -c 'rpm -ivh /root/*'", shell=True)

    # sync files
    rsync = '/usr/bin/rsync -a {}/ / --exclude="var/lib/rpm" --exclude="var/cache/yum" --exclude="tmp" ' \
                '--exclude="sys" --exclude="run" --exclude="lost+found" --exclude="mnt" --exclude="proc" ' \
                '--exclude="dev" --exclude="media" --exclude="etc" --exclude="root" '.format(install_dir)
    subprocess.run(rsync, shell=True)
    check_migration_progress('50')

    rpm_perl = '/etc/rpm/macros.perl'
    os.system('rpm --rebuilddb')
    if os.path.exists(rpm_perl):
        os.remove(rpm_perl)

    os.system("rpm -e --nodeps yum")
    if system_sync():
        subprocess.run('dnf -y groupinstall Minimal Install', shell=True)
    else:
        logger.info("Removing confilct package yum...")
        system_sync()
    check_migration_progress('60')
    # boot cui
    logger.info("set boot target to cui")
    cmd = 'systemctl set-default multi-user.target'
    run_subprocess(cmd.split())
    
    if not os.path.exists('/usr/bin/python3'):
        cmd = 'ln -s /usr/bin/python3.7 /usr/bin/python3'
        logger.info("Create symlink for python3")
        run_subprocess(cmd.split())
    check_migration_progress('70')
    yum_conflict_dir = '/etc/yum/'
    if os.path.exists(yum_conflict_dir):
        shutil.rmtree(yum_conflict_dir)
    logger.info("Installing yum...")
    set_grub_biosdev_rules()
    conf_grub()
    check_migration_progress('80')
    run_subprocess('dnf install -y yum'.split())
    run_subprocess('yum remove *uelc* -y'.split())
    check_migration_progress('100')

    logger.info("System migration completed, rebooting system")
    os.system("reboot")
    

if __name__ == '__main__':
    main()
