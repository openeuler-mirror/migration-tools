#!/bin/bash
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.  

# SPDX-License-Identifier:   MulanPubL-2.0-or-later

set -x
# Script to switch RedHat OS (or other similar distribution) to the UniontechOS

set -e
unset CDPATH

comd=$1

cat  > /etc/yum.repos.d/UOS.repo  <<-EOF
[UniontechOS-AppStream]
name = UniontechOS AppStream
gpgkey = file:///etc/pki/rpm-gpg/RPM-GPG-KEY-uos-release
gpgcheck = 0
baseurl = file:///mnt/iso/
enabled = 1
skip_if_unavailable = 1

EOF

yum_url=file:///etc/yum.repos.d
bad_packages=(gstreamer1-plugins-bad-free-gtk  python-meh-gui  redhat-release* redhat-release-cr  clucene-contribs-lib libreport-plugin-rhtsupport yum-rhn-plugin desktop-backgrounds-basic redhat-logos libreport-redhat libreport-plugin-mantisbt sl-logos python36-rpm subscription-manager gnome-shell-extension-horizontal-workspaces python-meh-guia  Red_Hat_Enterprise* redhat-support-tool redhat-support-lib-python  redhat-access-gui  ) 
#bad_packages=(redhat-release* redhat-release-cr libreport-plugin-rhtsupport yum-rhn-plugin desktop-backgrounds-basic redhat-logos libreport-redhat libreport-plugin-mantisbt sl-logos python36-rpm ) 


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
    exit_message "Could not install UniontechOS Server Enterprise-C 20 packages.
Your repositories have been restored to your previous configuration."
}

yum install -y uos-license-mini license-config 
## Start of script



echo "Checking your distribution..."
if ! old_release=$(rpm -q --whatprovides redhat-release); then
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
        exit_message "You appear to be already running UniontechOS Server Enterprise-C 20."
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
echo "Downloading UniontechOS Server Enterprise-C 20 yum repository file..."
if ! curl -o "switch-to-UOS.repo" "${yum_url}/${repo_file}"; then
    exit_message "Could not download $repo_file from $yum_url.
Are you behind a proxy? If so, make sure the 'http_proxy' environment
variable is set with your proxy address."
fi


echo "Backing up and removing old repository files..."


echo "Downloading UniontechOS Server Enterprise-C 20 release package..."
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

echo "Switching old release package with UniontechOS Server Enterprise-C 20..."
rpm -i --force '*.rpm'
rpm -e --nodeps "$old_release"
yum -y remove redhat-indexhtml*
rm -f "${reposdir}/switch-to-UOS.repo"
# At this point, the switch is completed.
trap - ERR


echo "Installing base packages for UniontechOS Server Enterprise-C 20..."
sed  -i  "s/^enabled =.*/enabled = 0/g"  /etc/yum.repos.d/UniontechOS.repo
sed  -i  "s/^enabled.*/enabled = 0/g"  /etc/yum/pluginconf.d/langpacks.conf

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

echo "Switch successful. Syncing with UniontechOS Server Enterprise-C 20 repositories."

if ! yum -y distro-sync; then
    exit_message "Could not automatically sync with UniontechOS Server Enterprise-C 20  repositories.
Check the output of 'yum distro-sync' to manually resolve the issue."
fi

echo "Sync successful. Switching default kernel to the UELC20."

arch=$(uname -m)
uek_path=$(find /boot -name "vmlinuz-*.uelc20.4.${arch}")
yumdb=`find  /var/lib/yum/yumdb  -name  "*el${rhel_version}*"`
for  x  in  $yumdb;do
	rm  -rf  ${x}
done

rm  -rf  /usr/share/doc/redhat*
rm  -rf  /etc/yum.repos.d/redhat*


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


#In order to specify the installation kernel, add parameters
if [ -n "$comd" ]
then
        kernel_dir=/mnt/iso/kernel-$comd
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
                echo "Error,The kernel-$comd packages was not found in the source"
                exit
        fi
fi


echo "Switch complete. UOS Server Enterprise-C 20 recommends rebooting this system."
