#!/bin/python3

import os
import datetime

class FixedPageInfo():

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    #repo sqlite name
    repo_sqlite_path = '../sysmig_agent/migrationTools/data/repo-sqlite/uos-1020e/x86_64'
    repo_sqlite_file = '2ad7cabc63634d5c75336929453bf9ff2054434547844df0c279c4759cd05409-primary.sqlite'
    sqlite_name = os.path.join(repo_sqlite_path, repo_sqlite_file)

    #UYi-V1.1存量数据目录
    inventory_data_dir = '/var/tmp/uos-migration/data/exp-rst'
    report_template_dir = 'mig_merge/report-template'
    report_dir = '/var/uos-migration'

    #数据文件
    unique_pkgname = os.path.join(inventory_data_dir, 'current-system-unique.csv')
    migrate_pkgname = os.path.join(inventory_data_dir, 'migration-system-install.csv')
    install_pkgname = os.path.join(inventory_data_dir, 'migration-system-total.csv')

    compatability_rpmpkg = os.path.join(inventory_data_dir, 'agent_ABI_check_result.csv')

    #前后端接口中涉及估计格式数据
    page_system_info = '{"type": "before_migration","general_tabs": {"name": "迁移评估检查-系统基本信息",'

    page_softpkg = '"packages_tabs": {"name": "软件包对比",'
    page_softpkg_first_column = page_softpkg + '"current_os_item": {"name": "当前系统特有（不替换）CentOS Linux 8 (Core)","data": ['
    page_softpkg_second_column = '"future_os_item": {"name": "迁移统特有（新安装）UOS Server Enterprise-C 20",'
    page_softpkg_third_column = '"total_list_item": {"name": "迁移系统软件包总列表 UOS Server Enterprise-C 20",'

    page_rpm_tabs = '"rpm_tabs": {"name": "RPM兼容性列表","data": ['

    page_hardware_tabs = '"hardware_tabs": {"name": "硬件兼容性","data": '
