import os
import sys
import json
import socket
from shutil import copyfile

from logger import migration_log
from mig_merge.stock_replace.general_tabs import general_tabs
from mig_merge.stock_replace.packages_tabs import packages_tabs
from mig_merge.stock_replace.rpm_tabs import rpm_tabs
from mig_merge.stock_replace.sysconffile_tabs import sysconffile_tabs
from mig_merge.stock_replace.hardware_tabs import hardware_tabs
from mig_merge.stock_replace.confscan_tabs import confscan_tabs
from mig_merge.stock_replace.rpmscan_tabs import rpmscan_tabs

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def xlsTohtml(log):
    '''
        应用场景：存量替换迁移评估检查
        功    能：按照前后端接口生成json格式数据,包括系统基本信息、软件包对比、
                  RPM二进制金融性、配置兼容性评估、PRM provide兼容性评估
        输入参数：无
        返 回 值：json数据
    '''
    json_str = general_tabs('A', log)+packages_tabs()+\
    rpm_tabs('A')+sysconffile_tabs()+','+hardware_tabs(log)+\
    confscan_tabs(log)+rpmscan_tabs('A', log)+'}'

    log.info('stock replace check json data:{}'.format(json_str))

    return json_str

def main():
    print(xlsTohtml())


if __name__ == "__main__":
    main()

