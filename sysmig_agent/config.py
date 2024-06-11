# 数据库填充字段
new_os = '统信服务器操作系统V20({})'
# 填充判断系统类型
c8 = ['1020a', '1021a', '1050a']
c7 = ['1000c', '1001c', '1002a']

# 创建和使用日志 报告的文件夹
AGENT_DIR = '/var/tmp/uos-migration/'
PRE_MIG_DIR = '/var/tmp/uos-migration/UOS_analysis_report'
MIGRATION_DIR = '/var/tmp/uos-migration/UOS_migration_log'
MIGRATION_REPORT_DIR = '/var/tmp/uos-migration/UOS_migration_completed_report'
RPMS = '/var/tmp/uos-migration/.rpms'
MIGRATION_KERNEL = '/var/tmp/uos-migration/kernel'
# 迁移所使用到的badpackages
badpackage7 = 'sysmig_agent/txts/7badpackage.txt'
badpackage8 = 'sysmig_agent/txts/8badpackage.txt'
CACHE_SPACE = 10.0
# abi结果更新数据库
abi_file = '/var/tmp/uos-migration/data/exp-rst/agent_ABI_check_result.csv'
