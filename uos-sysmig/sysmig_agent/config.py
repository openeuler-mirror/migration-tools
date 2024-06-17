# 数据库填充字段
new_os = '统信服务器操作系统V20({})'
# 填充判断系统类型
c8 = ['1020a', '1021a', '1050a']
c7 = ['1000c', '1001c', '1002a']

# 创建和使用日志 报告的文件夹
AGENT_DIR = '/var/tmp/uos-migration/'
# 存量替换
PRE_MIG_DIR = '/var/tmp/uos-migration/UOS_analysis_report'
# 新增扩容
PRE_MIG_DIR_ADD = '/var/tmp/uos-migration/UOS_analysis_report_add'
# 日志
MIGRATION_DIR = '/var/tmp/uos-migration/UOS_migration_log'
# 迁移分析
MIGRATION_REPORT_DIR = '/var/tmp/uos-migration/UOS_migration_completed_report'

RPMS = '/var/tmp/uos-migration/.rpms'
MIGRATION_KERNEL = '/var/tmp/uos-migration/kernel'
# 迁移所使用到的badpackages
badpackage7 = 'uos-sysmig/sysmig_agent/data/7badpackage.txt'
badpackage8 = 'uos-sysmig/sysmig_agent/data/8badpackage.txt'
CACHE_SPACE = 10.0
# abi结果更新数据库
abi_file = '/var/tmp/uos-migration/data/exp-rst/agent_ABI_check_result.csv'
