#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import socket

from mig_merge.config import FixedInfo
from mig_merge.merge.utils import dataplaceholder_replace
from mig_merge.migrationTools.utils.logger import Logger
from mig_merge.migrationTools.scanHardware import utils
import mig_merge.stock_replace.stock as stock 

logger = Logger(__name__)

def stock_replace_check(logger):
    '''
        应用场景：存量替换迁移检查-系统基本信息、软件包对比、RPM兼容性
                  配置兼容性评估、RPM兼容性评估
        功    能：按照前后端接口生成json数据，导出html报告
        输入参数：无
        返 回 值：绝对路径的检测报告名
    '''

    fixed_name = 'UOS_migration_report_'
    hostinfo = stock.get_local_ip() + '_' + socket.gethostname()
    report_name = fixed_name + hostinfo + "_" + FixedInfo.timestamp + ".html"

    report_check_dir = FixedInfo.report_check_dir
    if not os.path.exists(report_check_dir):
        os.makedirs(report_check_dir)
    report_html = report_check_dir + '/' + report_name 

    return dataplaceholder_replace(FixedInfo.stock_template_check, 
            report_html, stock.xlsTohtml(logger))

if __name__ == "__main__":
    stock_replace_check()

