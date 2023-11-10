# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier:   MulanPubL-2.0-or-later

# AGENT目录
AGENT_DIR = '/var/tmp/uos-migration/'

#迁移数据目录
MIGRATION_DATA_RPMS_DIR = '/var/tmp/uos-migration/data/exp-rst'
MIGRATION_DATA_RPMS_3_INFO = '/var/tmp/uos-migration/data/exp-rst/pkginfo_3.txt'
MIGRATION_DIR = '/var/tmp/uos-migration/UOS_migration_log'
MIGRATION_KERNEL = '/var/tmp/uos-migration/kernel'
pstate = '/var/tmp/uos-migration/.state'
progresslogdir = AGENT_DIR + '.progress'
PROGRESS = '/var/tmp/uos-migration/.progress'

# 迁移前分析目录
PRE_MIG = '/var/tmp/uos-migration/UOS_analysis_report/rpmva-before.txt'
PRE_MIG_DIR = '/var/tmp/uos-migration/UOS_analysis_report'

RPMS = '/var/tmp/uos-migration/.rpms'
MIG_LOG = '/var/tmp/uos-migration/UOS_migration_log/mig_log.txt'
OPENEULER_REPO = '''[openeuler]
name = openeuler
baseurl = http://mirrors.tuna.tsinghua.edu.cn/openeuler/openEuler-20.03-LTS-SP1/everything/$basearch
enabled = 1
gpgcheck = 0
'''

report_path_bef = "/var/tmp/uos-migration/UOS_analysis_report/"
report_path_ago = '/var/tmp/uos-migration/UOS_migration_log/'
txtFileName = '/var/tmp/uos-migration/data/exp-rst/abi-compat-pkg.txt'
txtFileName1 = '/var/tmp/uos-migration/data/exp-rst/abi-incompat-pkg.txt'
SysInfoFile = '/var/tmp/uos-migration/data/exp-rst/systeminfo.txt'
SysInfoFile_after = '/var/tmp/uos-migration/data/exp-rst/trans-end-sysinfo.txt'
PkgCompFile1 = '/var/tmp/uos-migration/data/exp-rst/pkginfo_1.txt'
PkgCompFile2 = '/var/tmp/uos-migration/data/exp-rst/pkginfo_2.txt'
PkgCompFile3 = '/var/tmp/uos-migration/data/exp-rst/pkginfo_3.txt'
PkgCompFile4 = '/var/tmp/uos-migration/data/exp-rst/pkginfo_4.txt'
PkgCompFile1_after = '/var/tmp/uos-migration/data/exp-rst/pkginfo_1_trans.txt'

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

install_baseurl = "sed -i 's/\$releasever/20/' /etc/yum.repos.d/UniontechOS.repo"

yum_url="file:///mnt/iso/AppStream"
