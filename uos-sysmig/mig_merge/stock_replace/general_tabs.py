import os
import sys
import json
import socket
from shutil import copyfile

from logger import migration_log
from migrationTools.scanHardware import utils
from stock_replace.confirm import get_cur_sys_version
from config import FixedInfo

def general_tabs():
    '''
        应用场景：存量替换迁移检测-系统基本信息
        功    能：1xxxa版系统基本信息，按照前后端接口生成json格式系统基本信息
        输入参数：无
        返 回 值：json数据
    '''
    line_num = 0

    sysinfo_name = FixedInfo.inventory_dir + '/systeminfo.txt'
    for line in open(sysinfo_name, 'r'):
        line_num += 1

        if line_num == 2:
            middle_data = '"current_os_version": "'+line.strip().split('|')[1]+'",'
            system_list = FixedInfo.page_system_info + middle_data

        if line_num == 3:
            middle_data = '"current_os_kennel_version": "'+line.strip().split('|')[1]+'",'
            system_list = system_list + middle_data

        if line_num == 5:
            middle_data = '"var_cache_available_space": "'+line.strip().split('|')[1]+'",'
            system_list = system_list + middle_data

        if line_num == 6:
            middle_data = '"architecture": "'+line.strip().split('|')[1]+'",'
            system_list = system_list + middle_data

        if line_num == 9:
            middle_data = '"replaced_software_package_count": "'+line.strip().split('|')[1]+'",'
            system_list = system_list + middle_data

        if line_num == 12:
            middle_data = '"compatible_software_package_count": "'+line.strip().split('|')[1]+'",'
            system_list = system_list + middle_data

        if line_num == 13:
            middle_data = '"incompatible_software_package_count": "'+line.strip().split('|')[1]+'",'
            system_list = system_list + middle_data

        if line_num == 14:
            middle_data = '"software_package_count": "'+line.strip().split('|')[1]+'"},'
            system_list = system_list + middle_data
    #migration_log.info('Get the current system info:{}'.format(system_list))
    return system_list


def main():
    general_tabs()


if __name__ == "__main__":
    main()

