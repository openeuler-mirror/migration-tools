#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import socket

from mig_merge.config import FixedInfo
from mig_merge.merge.utils import dataplaceholder_replace
import mig_merge.stock_replace.stock as stock
import mig_merge.stock_replace.confirm as confirm 

def stock_replace_analysis():
    '''
        应用场景：存量替换迁移分析-软件包对比
        功    能：生成迁移分析html报告
        输入参数：无
        返 回 值：绝对路径的检测报告名
    '''
    
    fixed_name = 'UOS_migration_completed_report_'
    hostinfo = stock.get_local_ip() + '_' + socket.gethostname()
    report_name = fixed_name + hostinfo + "_" + FixedInfo.timestamp + ".html"

    report_analysis_dir = FixedInfo.report_analysis_dir

    if not os.path.exists(report_analysis_dir):
        os.makedirs(report_analysis_dir)
    report_html = os.path.join(report_analysis_dir, report_name)

    return dataplaceholder_replace(FixedInfo.stock_template_analysis,
            report_html, confirm.gen_migration_info())

def main():
    stock_replace_analysis()

if __name__ == "__main__":
    main()

