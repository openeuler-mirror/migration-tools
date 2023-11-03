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