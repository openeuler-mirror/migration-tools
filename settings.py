# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier:   MulanPubL-2.0-or-later


defaultencoding = 'utf-8'
# logdss = Logger('./logdss.log',logging.DEBUG,logging.DEBUG)
new_os = '统信服务器操作系统V20({})'
AGENT_DIR = '/var/tmp/uos-migration/'
PRE_MIG = '/var/tmp/uos-migration/UOS_analysis_report/rpmva-before.txt'
PRE_MIG_DIR = '/var/tmp/uos-migration/UOS_analysis_report'
MIGRATION_DIR = '/var/tmp/uos-migration/UOS_migration_log'
MIGRATION_REPORT_DIR = '/var/tmp/uos-migration/UOS_migration_completed_report'


PROGRESS = '/var/tmp/uos-migration/.progress'
RPMS = '/var/tmp/uos-migration/.rpms'
MIGRATION_KERNEL = '/var/tmp/uos-migration/kernel'
MIGRATION_LOG = '/var/tmp/uos-migration/UOS_migration_log/log'
MIGRATION_DATA_RPMS_DIR = '/var/tmp/uos-migration/data/exp-rst'
MIGRATION_DATA_RPMS_3_INFO = '/var/tmp/uos-migration/data/exp-rst/pkginfo_3.txt'
pstate = '/var/tmp/uos-migration/.state'

abi_file = '/var/tmp/uos-migration/data/exp-rst/agent_ABI_check_result.csv'
#Abi
local_dir = '/var/tmp/uos-migration/data/'
exp_rst_dir = local_dir+'exp-rst/'

current_system_unique = exp_rst_dir + 'current-system-unique.csv'
migration_system_install = exp_rst_dir + 'migration-system-install.csv'
migration_system_total = exp_rst_dir + 'migration-system-total.csv'
abi_comp_chk = exp_rst_dir + 'abi-comp-chk.csv'
abi_incomp_chk = exp_rst_dir + 'abi-incomp-chk.csv'
exitFlag = 0
total_rpm_nums = 0
percentage = ''
deal_rpm_num = 0
agent_abi_check_result = exp_rst_dir + 'agent_ABI_check_result.csv'
suffix_list = ['.mo', '.gz', '.xml', '.conf', '.png', '.page', '.woff', '.ttf', '.pyc', '.typelib', '.pdf', '.ppt', '.txt', '.ico', '.icc', '.tcc', '.gif', '.oga', '.rom', '.jpg', '.dict', '.webm', '.pyc', '.wav', '.ucode', '.ttc', '.gresource', '.otf', '.t1', '.db', '.elc', '.cache', '.fd', '.iso', '.efi', '.mmdb', '.bz2', '.img', '.bin', '.fw', '.cis', '.itb', '.inp', '.sbcf', '.ddc', '.sfi', '.bseq', '.mfa2', '.chk', '.mgc', '.stub', '.dfu', '.dat', '.sys', '.bts', '.dlmem', '.brd', '.hwm', '.pwd', '.pwi', '.exe', '.der', '.p12', '.ogg', '.signed', '.dafsa', '.gpg', '.tri', '.x86_64']

