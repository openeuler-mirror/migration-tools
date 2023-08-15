#!/bin/bash


set -x
# Script to switch CentOS/RedHat (or other similar distribution) to the UniontechOS

set -e
unset CDPATH

while getopts n:e:d:k: opt
do
    case "$opt" in
    n) n=${OPTARG};;
    e) exclude_pkgs=${OPTARG};echo "Exclude is ${OPTARG} - $exclude_pkgs";;
    d) pwddir=${OPTARG};echo "Kernle diractory is ${OPTARG} - $pwddir";;
    k) knl=${OPTARG};echo "Kernel opt is ${OPTARG} - $knl";;
    *) echo "Null";;
    esac
done

echo "Kernel opt : $knl"
echo "Exlcude : $exclude_pkgs"
echo $pwddir



if [ -n  "$exclude_pkgs" ]
then
cat  > /etc/yum.conf <<-EOF
[main]
cachedir=/var/cache/yum/\$basearch/\$releasever
keepcache=0
debuglevel=2
logfile=/var/log/yum.log
exactarch=1
obsoletes=1
gpgcheck=1
plugins=1
installonly_limit=3
exclude=$exclude_pkgs
EOF
fi

comd=$knl

yum_url=file:///etc/yum.repos.d/
bad_packages=( subscription-manager gstreamer1-plugins-bad-free-gtk  python-meh-gui  clucene-contribs-lib centos-release centos-release-cr libreport-plugin-rhtsupport yum-rhn-plugin desktop-backgrounds-basic centos-logos libreport-centos libreport-plugin-mantisbt sl-logos python36-rpm) 


usage() {
    echo "Usage: ${0##*/} [OPTIONS]"
    echo
    echo "OPTIONS"
    echo "-h"
    echo "        Display this help and exit"
    exit 1
} >&2

have_program() {
    hash "$1" >/dev/null 2>&1
}
##命令未找到。请安装或添加到您的路径，然后重试。
dep_check() {
    if ! have_program "$1"; then
        exit_message "'${1}' command not found. Please install or add it to your PATH and try again."
    fi
}

exit_message() {
    echo "$1"
#    echo "For assistance, please email <${contact_email}>."
    exit 1
} >&2

restore_repos() {
    yum remove -y "${new_releases}"
    find . -name 'repo.*' | while read -r repo; do
        destination=$(head -n1 "$repo")
        if [ "${destination}" ]; then
            tail -n+2 "${repo}" > "${destination}"
        fi
    done
    rm "${reposdir}/${repo_file}"
    exit_message "Could not install UOS Server Enterprise-C 20 packages.
Your repositories have been restored to your previous configuration."
}

yum install -y uos-license-mini license-config 
## Start of script

while getopts "h" option; do
    case "$option" in
        h) usage ;;
        *) usage ;;

    esac
done
## id  -u是root的id号,必须是root执行
if [ "$(id -u)" -ne 0 ]; then
    exit_message "You must run this script as root.
Try running 'su -c ${0}'."
fi
echo "Checking for required packages..."
for pkg in rpm yum python2 curl; do
    dep_check "${pkg}"
done


echo "Checking your distribution..."
if ! old_release=$(rpm -q --whatprovides centos-release); then
    exit_message "You appear to be running an unsupported distribution."
fi

if [ "$(echo "${old_release}" | wc -l)" -ne 1 ]; then
    exit_message "Could not determine your distribution because multiple
packages are providing redhat-release:
$old_release
"
fi

case "${old_release}" in
    redhat-release*) ;;
    centos-release*) ;;
    sl-release*) ;;
    uos-release*|enterprise-release*)
        exit_message "You appear to be already running UOS Server Enterprise-C 20."
        ;;
    *) exit_message "You appear to be running an unsupported distribution." ;;
esac


rhel_version=$(rpm -q "${old_release}" --qf "%{version}")
base_packages=(basesystem initscripts uos-logos)
case "$rhel_version" in
    7*)
        repo_file=UOS.repo
        new_releases=(uos-release-server)
        base_packages=("${base_packages[@]}" plymouth grub2 grubby kernel* uos-rpm-config hypervvssd hypervfcopyd hypervkvpd kmod-kvdo compat-gnome-desktop* ) 
        ;;
    6*)
 #       repo_file=public-yum-ol6.repo
        new_releases=(uos-release-server)
        base_packages=("${base_packages[@]}" plymouth grub grubby kernel*)
        ;;
    *) exit_message "You appear to be running an unsupported distribution." ;;
esac
echo "Checking for yum lock..."
if [ -f /var/run/yum.pid ]; then
    yum_lock_pid=$(cat /var/run/yum.pid)
    yum_lock_comm=$(cat "/proc/${yum_lock_pid}/comm")
    exit_message "Another app is currently holding the yum lock.
The other application is: $yum_lock_comm
Running as pid: $yum_lock_pid
Run 'kill $yum_lock_pid' to stop it, then run this script again."
fi
echo "Looking for yumdownloader..."
if ! have_program yumdownloader; then
    yum -y install yum-utils || true
    dep_check yumdownloader
fi
##寻找存储库目录
echo "Finding your repository directory..."

reposdir=$(python2 -c "
import yum
import os

for dir in yum.YumBase().doConfigSetup(init_plugins=False).reposdir:
    if os.path.isdir(dir):
        print dir
        break
")

if [ -z "${reposdir}" ]; then
    exit_message "Could not locate your repository directory."
fi
cd "$reposdir"
echo "Downloading UOS Server Enterprise-C 20 yum repository file..."
if ! curl -o "switch-to-UOS.repo" "${yum_url}/${repo_file}"; then
    exit_message "Could not download $repo_file from $yum_url.
Are you behind a proxy? If so, make sure the 'http_proxy' environment
variable is set with your proxy address."
fi
if [[ "centos" =~ "old_release" ]];then
	cd "$(mktemp -d)"
	trap restore_repos ERR

	echo "Backing up and removing old repository files..."

	rpm -ql "$old_release" | grep '\.repo$' > repo_files

	while read -r repo; do
    	if [ -f "$repo" ]; then
        	cat - "$repo" > "$repo".disabled <<EOF
# This is a yum repository file that was disabled by
# ${0##*/}, a script to convert CentOS to UOS Server Enterprise-C 20.
# Please see $yum_url for more information.

EOF
       		tmpfile=$(mktemp repo.XXXXX)
        	echo "$repo" | cat - "$repo" > "$tmpfile"
        	rm "$repo"
    	fi
	done < repo_files
fi

echo "Downloading UOS Server Enterprise-C 20 release package..."
if ! yumdownloader "${new_releases[@]}"; then
    {
        echo "Could not download the following packages from ${yum_url}/${repo_file}:"
        echo "${new_releases[@]}"
        echo

        echo "Are you behind a proxy? If so, make sure the 'http_proxy' environment"
        echo "variable is set with your proxy address."
    } >&2
    restore_repos
fi



#################  使用uos-release-server默认软件源##
#: '
yum -y downgrade python-urlgrabber 
yum -y install python-urlgrabber 
#'
#####################################################

echo "Switching old release package with UOS Server Enterprise-C 20..."
rpm -i --force '*.rpm'
rpm -e --nodeps "$old_release"
if [[ "redhat" =~ "old_release" ]];then
	yum -y remove redhat-indexhtml*
else
	yum -y remove centos-indexhtml*
fi
rm -f "${reposdir}/switch-to-UOS.repo"
# At this point, the switch is completed.
trap - ERR


echo "Installing base packages for UOS Server Enterprise-C 20..."
sed  -i  "s/^enabled =.*/enabled = 0/g"  /etc/yum.repos.d/UniontechOS.repo

#rpm  -e   rpm-build
# rpm  -e   system-rpm-config
#rpm  -e  redhat-rpm-config
if ! yum shell -y <<EOF
remove ${bad_packages[@]}
install ${base_packages[@]}
run
EOF
then
    exit_message "Could not install base packages.
Run 'yum distro-sync' to manually install them."
fi
if [ -x /usr/libexec/plymouth/plymouth-update-initrd ]; then
    echo "Updating initrd..."
    /usr/libexec/plymouth/plymouth-update-initrd
fi

echo "Switch successful. Syncing with UOS Server Enterprise-C 20 repositories."

if ! yum -y distro-sync; then
    exit_message "Could not automatically sync with UOS Server Enterprise-C 20  repositories.
Check the output of 'yum distro-sync' to manually resolve the issue."
fi

echo "Sync successful. Switching default kernel to the UELC20."

arch=$(uname -m)
uek_path=$(find /boot -name "vmlinuz-*.uelc20.4.${arch}")
old_rhel=`rpm  -qa | grep  kernel | grep  "el${rhel_version}"`
yumdb=`find  /var/lib/yum/yumdb  -name  "*el${rhel_version}*"`
for  x  in  $yumdb;do
	rm  -rf  ${x}
done


# vmlinuz-3.10.0-1062.18.1.uelc20.4.x86_64
case "$rhel_version" in
    7*)
        if [ -d /sys/firmware/efi ]; then
            grub2-mkconfig -o /boot/efi/EFI/UOS/grub.cfg
        else
            grub2-mkconfig -o /boot/grub2/grub.cfg
        fi
        grubby --set-default="${uek_path}"
        ;;
    6*)
        grubby --set-default="${uek_path}"
        ;;
esac
rpm  -e  ${old_rhel}



#In order to specify the installation kernel, add parameters
if [ -n "$1" ]
then
        kernel_dir=/mnt/iso/kernel-$1
        if [ -d $kernel_dir ]
        then
                cd $kernel_dir
                rpm -Uvh kernel-devel* --oldpackage
                rpm -Uvh kernel-headers* --oldpackage
                rpm -Uvh kernel-tools* --oldpackage
                rpm -Uvh  kernel-3.10.0-1062.18.1.uelc20.4.x86_64.rpm --oldpackage
		rpm -Uvh bpftool-3.10.0-1062.18.1.uelc20.4.x86_64.rpm --oldpackage
		rpm -Uvh perf-3.10.0-1062.18.1.uelc20.4.x86_64.rpm --oldpackage
		rpm -Uvh python-perf-3.10.0-1062.18.1.uelc20.4.x86_64.rpm --oldpackage
		rpm -Uvh kernel-abi* --oldpackage

		rpm -ef kernel-modules --nodeps
		rpm -ef kernel-core --nodeps
        else
                echo "Error,The kernel-$1 packages was not found in the source"
                exit
        fi
fi


echo "Switch complete. UOS Server Enterprise-C 20 recommends rebooting this system."
