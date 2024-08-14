# 数据库填充字段
new_os = '统信服务器操作系统V20({})'
# 填充判断系统类型
c8 = ['1020a', '1021a', '1050a']
c7 = ['1000c', '1001c', '1002a']

# agent的安装目录
agent_install = '/usr/lib/uos-sysmig-agent/'
# 创建和使用日志 报告的文件夹
AGENT_DIR = '/var/tmp/uos-migration/'
# 存量替换
PRE_MIG_DIR = '/var/tmp/uos-migration/UOS_analysis_report'
# 新增扩容
PRE_MIG_DIR_ADD = '/var/tmp/uos-migration/UOS_analysis_report_add'
# 日志
MIGRATION_DIR = '/var/tmp/uos-migration/UOS_migration_log'
db_log = MIGRATION_DIR + '/' + 'migration.log'
# 迁移分析
MIGRATION_REPORT_DIR = '/var/tmp/uos-migration/UOS_migration_completed_report'
# 存放abi兼容性检测数据
abipwd = '/var/tmp/uos-migration/data/exp-rst'
# ABI_INCOMPAT_PATH = abipwd + '/abi-incompat-pkg.txt'
# ABI_COMPAT_PATH = abipwd + '/abi-compat-pkg.txt'
ABI_INCOMPAT_PATH = '/var/tmp/uos-migration/data/exp-rst/abi-incomp-chk.csv'
ABI_COMPAT_PATH = '/var/tmp/uos-migration/data/exp-rst/abi-comp-chk.csv'
AppStream ='sysmig_agent/data/AppStream.txt'
BaseOS = 'sysmig_agent/data/BaseOS.txt'

RPMS = '/var/tmp/uos-migration/.rpms'
MIGRATION_KERNEL = '/var/tmp/uos-migration/kernel'
# 迁移所使用到的badpackages
badpackage7 = 'sysmig_agent/data/7badpackage.txt'
badpackage8 = 'sysmig_agent/data/8badpackage.txt'
ignore_abi_check_8 = 'sysmig_agent/data/ignore_abi_check_8.txt'
CACHE_SPACE = 10.0
# abi结果更新数据库
abi_file = '/var/tmp/uos-migration/data/exp-rst/agent_ABI_check_result.csv'
# 兼容性检测、分层分级结果对比、迁移风险阈值：
COMP = 95
