import os
import sys
import json
import socket
from shutil import copyfile

from logger import migration_log
from mig_merge.config import FixedInfo
from mig_merge.migrationTools.scanHardware import utils
from mig_merge.stock_replace.confirm import get_cur_sys_version

def general_tabs(sFlag, logger):
    '''
        应用场景：存量替换迁移检测-系统基本信息
        功    能：1xxxa版系统基本信息，按照前后端接口生成json格式系统基本信息
        输入参数：sFlag - A/E标识
        返 回 值：json数据
    '''

    line_num = 0
    layered_flag = False

    sysinfo_name = FixedInfo.inventory_dir + '/before-system-info.txt'
    for line in open(sysinfo_name, 'r'):
        line_num += 1

        if line_num == 1:
            middle_data = '"current_os_version": "'+line.strip().split('|')[2]+'",'
            if sFlag == 'A':
                system_list = FixedInfo.page_system_info + middle_data
            else:
                system_list = FixedInfo.expansion_gen_tabs + middle_data

        if line_num == 2:
            middle_data = '"current_os_kennel_version": "'+line.strip().split('|')[2]+'",'
            system_list = system_list + middle_data

        if line_num == 3:
            middle_data = '"var_cache_available_space": "'+line.strip().split('|')[2]+'",'
            system_list = system_list + middle_data

        if line_num == 4:
            middle_data = '"architecture": "'+line.strip().split('|')[2]+'",'
            system_list = system_list + middle_data

        if sFlag == 'A':
            if line_num == 5:
                middle_data = '"replaced_software_package_count": "'+line.strip().split('|')[2]+'",'
                system_list = system_list + middle_data

            if line_num == 6:
                middle_data = '"compatible_software_package_count": "'+line.strip().split('|')[2]+'",'
                system_list = system_list + middle_data

            if line_num == 7:
                middle_data = '"incompatible_software_package_count": "'+line.strip().split('|')[2]+'",'
                system_list = system_list + middle_data

            if line_num == 8:
                package_count = line.strip().split('|')[2]
        else: 
            if line_num == 5:
                middle_data = '"replaced_software_package_count": " ",'
                system_list = system_list + middle_data

            if line_num == 6:
                middle_data = '"compatible_software_package_count": " ",'
                system_list = system_list + middle_data

            if line_num == 7:
                middle_data = '"incompatible_software_package_count": " ",'
                system_list = system_list + middle_data

        if line_num == 9:
            layered_flag = True
            if sFlag == 'A':
                layered_grading = ',根据分层分级算法的兼容度为%s%%' %(line.strip())
                middle_data = '"software_package_count": "'+ package_count + layered_grading +'"},'
                system_list = system_list + middle_data
            else:
                middle_data = '"software_package_count": " "},'
                system_list = system_list + middle_data

    if not layered_flag:
        if sFlag == 'A':
            middle_data = '"software_package_count": "'+ package_count + '"},'
        else:
            middle_data = '"software_package_count": " "},'
        system_list = system_list + middle_data
        logger.info('Failed to write the compatibility of the hierarchical algorithm Procedure,Json data is not affected')
        logger.info('Please check whether to write file of the 9 number of line {}'.format(sysinfo_name))

    return system_list

def main():
    general_tabs()


if __name__ == "__main__":
    main()

