#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import socket

#for test
sys.path.append("..")

from sysmig_agent.migrationTools.utils.logger import Logger
from sysmig_agent.migrationTools.scanHardware import utils
from sysmig_agent.Abisystmcompchk import migrate_before_abi_chk 
from mig_merge.config import FixedPageInfo
import mig_merge.stock_replace.stock as stock 

logger = Logger(__name__)

#def stock_replace_check(query, sta):
def stock_replace_check():
    '''UYi-V1.2版本存量替换迁移检查场景
        基于1xxxa版本，按照前后端接口生成json数据
        替换html报告中数据占位符"dataPlaceholder"为json数据
        参数：
            无
        返回：
            success
    '''
    #1xxxa原有接口保留
    #migrate_before_abi_chk(query, sta)

    template_html = FixedPageInfo.report_template_dir + '/uos-sysmig-A.html'

    hostinfo = stock.get_local_ip() + '_' + socket.gethostname()
    report_name = "UOS_migration_report_" + hostinfo + "_" + FixedPageInfo.timestamp + ".html"
    report_html = FixedPageInfo.report_dir + '/' + report_name 

    compatability_list = utils.get_compatability_list(
        utils.get_pci_list(), utils.get_supported_device_list(), False)
    jsonstr = stock.xlsTohtml(json.dumps(compatability_list))
    dataplaceholder_replace(template_html, report_html, jsonstr)
    return 'success'

def main():
    stock_replace_check()

if __name__ == "__main__":
    main()

