#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import socket

from merge.utils import dataplaceholder_replace
from migrationTools.utils.logger import Logger
from migrationTools.scanHardware import utils
#from Abisystmcompchk import migrate_before_abi_chk 
from config import FixedInfo
import stock_replace.stock as stock 

logger = Logger(__name__)

#def stock_replace_check(query, sta):
def stock_replace_check():
    '''
        应用场景：存量替换迁移检查-系统基本信息、软件包对比、RPM兼容性
        功    能：基于1xxxa版本，转换检测结果为html报告
        输入参数：无
        返 回 值：绝对路径的检测报告名
    '''

    #1xxxa原有接口保留
    #migrate_before_abi_chk(query, sta)

    fixed_name = 'UOS_migration_report_'
    hostinfo = stock.get_local_ip() + '_' + socket.gethostname()
    report_name = fixed_name + hostinfo + "_" + FixedInfo.timestamp + ".html"
    report_html = FixedInfo.report_stock_dir + '/' + report_name 

    return dataplaceholder_replace(FixedInfo.stock_template_check, 
            report_html, stock.xlsTohtml())

def main():
    stock_replace_check()

if __name__ == "__main__":
    main()

