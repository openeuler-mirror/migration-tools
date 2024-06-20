#!/bin/python3

import os
import datetime

class FixedInfo():

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    #sqlite 数据目录
    sqlite_dir = '/root/uos-sysmig/uos-sysmig/mig_merge/migrationTools/data/repo-sqlite'

    local_dir = '/var/tmp/uos-migration'
    template_dir = '../ui/report_templates/dist'
    inventory_dir = os.path.join(local_dir, 'data/exp-rst')
    repo_diff_path = os.path.join(local_dir, 'uos/rpms')
    report_check_dir = os.path.join(local_dir, 'UOS_analysis_report')
    report_expansion_dir = os.path.join(local_dir, 'UOS_analysis_report_add')
    report_analysis_dir = os.path.join(local_dir, 'UOS_migration_completed_report')

    #前端html报告模板
    stock_template_analysis = os.path.join(template_dir, 'stock_replace_analysis.html')
    stock_template_check = os.path.join(template_dir, 'stock_replace_check.html')
    expansion_template = os.path.join(template_dir, 'new_expansion_check.html')

    #repo sqlite name
    repo_sqlite_path = 'migrationTools/data/repo-sqlite/uos-1020e/x86_64'
    repo_sqlite_file = '2ad7cabc63634d5c75336929453bf9ff2054434547844df0c279c4759cd05409-primary.sqlite'
    sqlite_name = os.path.join(repo_sqlite_path, repo_sqlite_file)


    #数据文件
    agent_abi_result = os.path.join(inventory_dir, 'agent_ABI_check_result.csv')
    migration_eln = os.path.join(inventory_dir, 'migration-before-eln-rpm-tmp.csv')
    migration_uelc = os.path.join(inventory_dir, 'migration-before-uelc20-rpm-tmp.csv')
    sys_version = os.path.join(inventory_dir, 'sys-version-tmp')


    unique_pkgname = os.path.join(inventory_dir, 'current-system-unique.csv')
    migrate_pkgname = os.path.join(inventory_dir, 'migration-system-install.csv')
    total_pkgname = os.path.join(inventory_dir, 'migration-system-total.csv')

    diff_rpmpkg = os.path.join(inventory_dir, 'repo-diff-rpmpkg.txt')
    same_rpmpkg = os.path.join(inventory_dir, 'repo-current-system-unique.txt')


    compatability_rpmpkg = os.path.join(inventory_dir, 'agent_ABI_check_result.csv')

    #存量替换迁移检查-前后端接口中涉及固定格式数据
    page_system_info = '{"type": "stock_replace_check","general_tabs": {"name": "系统基本信息",'
    page_softpkg = '"packages_tabs": {"name": "软件包对比",'
    current_head_info = page_softpkg + '"current_os_item": {"name": "当前系统特有（不替换）'
    total_head_info = '"total_list_item": {"name": "迁移系统软件包总列表 UOS Server Enterprise-C 20"'

    #存量替换迁移分析-前后端接口中涉及固定格式数据
    head_info = '{"type":"stock_replace_analysis","packages_tabs": {"name": "软件包列表",'
    current_info = '"current_os_item": {"name":"当前系统特有（不替换）'
    future_info = '"future_os_item": {"name": "迁移统特有（新安装）'
    total_info = '"total_list_item": {"name": "迁移系统软件包总列表 '

    #新增扩容迁移检查-前后端接口中涉及固定格式数据
    expansion_haed = '{"type": "new_expansion_check",'
    page_hardware_tabs = '"hardware_tabs": {"name": "硬件兼容性","data": '
    page_rpm_tabs = '"rpm_tabs": {"name": "RPM兼容性","data": ['
    expansion_gen_tabs = 'general_tabs": {"name": "系统基本信息",'

    #融合1xxxe版
    expansion_page_head = '{"type": "new_expansion_check","sysconffile_tabs": {"name": "SysSconf","data": ['
    hardware_tabs_head = '"hardware_tabs": {"name": "硬件兼容性","data":'

    suffix_list = ['.mo', '.gz', '.xml', '.conf', '.png', '.page', '.woff', '.ttf', '.pyc', '.typelib', '.pdf', '.ppt', '.txt', '.ico', '.icc', '.tcc', '.gif', '.oga', '.rom', '.jpg', '.dict', '.webm', '.pyc', '.wav', '.ucode', '.ttc', '.gresource', '.otf', '.t1', '.db', '.elc', '.cache', '.fd', '.iso', '.efi', '.mmdb', '.bz2', '.img', '.bin', '.fw', '.cis', '.itb', '.inp', '.sbcf', '.ddc', '.sfi', '.bseq', '.mfa2', '.chk', '.mgc', '.stub', '.dfu', '.dat', '.sys', '.bts', '.dlmem', '.brd', '.hwm', '.pwd', '.pwi', '.exe', '.der', '.p12', '.ogg', '.signed', '.dafsa', '.gpg', '.tri', '.x86_64', '.pm']
