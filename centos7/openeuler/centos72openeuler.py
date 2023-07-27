import os
import platform
import shutil
import subprocess


openeuler_repo = '''[openeuler]
name = openeuler
baseurl = http://mirrors.tuna.tsinghua.edu.cn/openeuler/openEuler-20.03-LTS-SP1/everything/$basearch
enabled = 1
gpgcheck = 0
'''


def run_subprocess(cmd):
    try:
        process = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,  # Avoid using shell=True
            text=True,    # Capture output as text
            check=True    # Check for non-zero return code and raise exception if found
        )
        output = process.stdout
        print(output)  # Print the output to console
        return output, process.returncode
    except subprocess.CalledProcessError as e:
        print(f"Command '{e.cmd}' failed with return code {e.returncode}.")
        print(e.stderr)  # Print the error output to console
        return e.stderr, e.returncode


def check_pkg(rpm):
    _, ret = run_subprocess('rpm -q {}'.format(rpm))
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
        # "Parse /boot/efi disk info failed, update boot loader failed.
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
        run_subprocess(cmd)
    except Exception as e:
        print(e)

def swap_release(release):
    tmp_dir = '/var/tmp'
    rpme_release = 'rpm -qf /etc/os-release|xargs -i rpm -e --nodeps {}'
    run_subprocess(rpme_release)
    cmd = 'yumdownloader {} --destdir {}'.format(release, tmp_dir)
    run_subprocess(cmd)
    run_subprocess('rpm -ivh {}/*.rpm --nodeps --force'.format(tmp_dir))


def conf_grub():
    if os.path.isdir('/sys/firmware/efi'):
        old_kernel = '3.10.0'
        if old_kernel:
            run_subprocess('rpm -e --nodeps kernel-{}'.format(old_kernel))
            run_subprocess('dnf install -y shim')
        openEuler_path = '/boot/efi/EFI/openEuler'
        if not os.path.exists(openEuler_path):
            uos_path = '/boot/efi/EFI/openEuler'
        run_subprocess('grub2-mkconfig -o {}/grub.cfg'.format(openEuler_path))
        add_boot_option()
    else:
        run_subprocess('grub2-mkconfig -o /boot/grub2/grub.cfg')
        try:
            run_subprocess('test -L /boot/grub2/grubenv')
            run_subprocess('mv /boot/grub2/grubenv /boot/grub2/grubenv-bak')
            run_subprocess('cat /boot/grub2/grubenv-bak > /boot/grub2/grubenv')
        except Exception as e:
            print(e)


def system_sync():
    rebuilddb = 'rpm --rebuilddb;dnf clean all'
    run_subprocess(rebuilddb)
    cmd = 'dnf -y distro-sync --allowerasing --skip-broken'
    _, ret = run_subprocess(cmd)
    _, ret = run_subprocess('rpm -q kernel|grep {}'.format('oe1'))
    if ret:
        return False
    return True

def main():
    if not check_pkg("yum-utils"):
        print("please install yum-utils")
        return

    if not check_pkg('rsync'):
        print('please install rsync')
        return
    
    if not check_pkg('python3'):
        print('please install python3')
        return

    if not check_pkg('dnf'):
        print('please install dnf')
        return

    # disable centos repository
    os.system("yum-config-manager --disable base updates extras")

    repofile = "/etc/yum.repos.d/openeuler.repo"
    with open(repofile, 'w') as f:
        f.write(openeuler_repo)


    openEuler_release = 'openEuler-release'
    if not check_pkg(openEuler_release):
        print("swaping release")
        swap_release(openEuler_release)

    # install basic packages
    os.system("yum install -y gdbm-help")

    remove_packages_nodeps = ['gdm', 'centos-logos', 'redhat-logos', 
                                'iwl7265-firmware', 'ivtv-firmware', 
                                'sysvinit-tools', 'sg3_utils-libs']
    for package in remove_packages_nodeps:
        nodeps_cmd = f"rpm -q {package} && rpm -e --nodeps {package}"
        os.system(nodeps_cmd)

        dnf_path = '/usr/bin/dnf'
        install_dir = os.path.join(os.path.dirname('/var/tmp'), 'DNF')
        if not os.path.exists(install_dir):
            os.makedirs(install_dir)
        else:
            shutil.rmtree(install_dir)
    install_cmd = 'yum install -y systemd python3-libdnf libreport-filesystem python3-gpg libmodulemd deltarpm python3-hawkey \
                    python3-libcomps python3-rpm util-linux --installroot={}'.format(install_dir)
    os.system(install_cmd)

    # download dnf
    download_dnf = '/usr/bin/yumdownloader {} --destdir={}'.format('dnf python3-dnf dnf-help', os.path.join(install_dir, 'root'))
    os.system(download_dnf)

    # rebuild dnfdb
    ivh_dnf = '/sbin/chroot {} /bin/bash -c "rpm --rebuilddb"'.format(install_dir)
    _, ret = run_subprocess(ivh_dnf)
    if ret:
        print("rebuild yum db failed")
        return

    # install dnf 
    ivh_dnf = '/sbin/chroot {} /bin/bash -c "rpm -ivh {}/*"'.format(install_dir, '/root')
    _, ret = run_subprocess(ivh_dnf)
    if ret:
        print("Install dnf failed")
        return

    # sync files
    rsync = '/usr/bin/rsync -a {}/ / --exclude="var/lib/rpm" --exclude="var/cache/yum" --exclude="tmp" ' \
                '--exclude="sys" --exclude="run" --exclude="lost+found" --exclude="mnt" --exclude="proc" ' \
                '--exclude="dev" --exclude="media" --exclude="etc" --exclude="root" '.format(install_dir)
    _, ret = run_subprocess(rsync)
    if ret:
        return

    rpm_perl = '/etc/rpm/macros.perl'
    os.system('rpm --rebuilddb')
    if os.path.exists(rpm_perl):
        os.remove(rpm_perl)

    if os.path.exists(dnf_path):
        pass

    if system_sync():
        install_cmd = 'dnf -y groupinstall "Minimal Install"'
        run_subprocess(install_cmd)
        conf_grub()
    else:
        print("Removing confilct package yum...")
        run_subprocess("rpm -e --nodeps yum")
        system_sync()

    
    # boot cui
    print("set boot target to cui")
    cmd = 'systemctl set-default multi-user.target'
    run_subprocess(cmd)
    
    if not os.path.exists('/usr/bin/python3'):
        cmd = 'ln -s /usr/bin/python3.7 /usr/bin/python3'
        print("Create symlink for python3")
        run_subprocess(cmd)

    yum_conflict_dir = '/etc/yum/'
    if os.path.exists(yum_conflict_dir):
        shutil.rmtree(yum_conflict_dir)
    print("Installing yum...")
    run_subprocess('dnf install -y yum')
    
    print("System migration completed, rebooting system")
    os.system("reboot")
    


if __name__ == '__main__':
    main()
