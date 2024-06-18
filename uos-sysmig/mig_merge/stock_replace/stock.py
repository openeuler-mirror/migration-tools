import os
import sys
import json
import socket
from shutil import copyfile

from logger import migration_log
from stock_replace.general_tabs import general_tabs
from stock_replace.packages_tabs import packages_tabs
from stock_replace.rpm_tabs import rpm_tabs
from stock_replace.confscan_tabs import confscan_tabs
from stock_replace.rpmscan_tabs import rpmscan_tabs

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def xlsTohtml():
    '''
        应用场景：存量替换迁移评估检查，包括系统基本信息，软件包对比，RPM兼容性检测
        功    能：1xxxa版系统基本信息，软件包对比，RPM兼容性对比，按照前后端接口生成json格式数据
        输入参数：无
        返 回 值：json数据
    '''
    return general_tabs()+packages_tabs()+rpm_tabs()+confscan_tabs()+rpmscan_tabs()+'}'

def main():
    xlsTohtml()


if __name__ == "__main__":
    main()

