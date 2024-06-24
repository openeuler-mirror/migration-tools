#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import socket

from mig_merge.config import FixedInfo
from mig_merge.merge.utils import dataplaceholder_replace
from mig_merge.stock_replace.stock import get_local_ip
from mig_merge.new_expansion.expansion import MigrationMerge

def new_expansion_check(logger):
    '''
        应用场景：新增扩容迁移检查-系统基本信息、软件包对比、RPM兼容性、
                  硬件兼容性评估、配置兼容性评估、RPM兼容性评估、系统修改配置
        功    能：生成迁移检查html报告
        输入参数：无
        返 回 值：绝对路径的检测报告名
    '''

    fixed_name = 'UOS_migration_report_'
    hostinfo = get_local_ip() + '_' + socket.gethostname()
    report_name = fixed_name + hostinfo + "_" + FixedInfo.timestamp + ".html"

    report_expansion_dir = FixedInfo.report_expansion_dir
    if not os.path.exists(report_expansion_dir):
        os.makedirs(report_expansion_dir)
    report_html = os.path.join(report_expansion_dir, report_name)

    return dataplaceholder_replace(FixedInfo.expansion_template,
        report_html, MigrationMerge(logger))

if __name__ == "__main__":
    new_expansion_check()

