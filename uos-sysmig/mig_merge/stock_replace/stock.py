import os
import sys
import json
import socket
from shutil import copyfile

from migrationTools.scanHardware import utils
from stock_replace.confirm import get_cur_sys_version
from config import FixedInfo

def mycopyfile(template_name, dst_name):

    dst_dir = FixedInfo.report_dir
    report_template_name = FixedInfo.report_template_dir + '/' + template_name

    if not os.path.exists(report_template_name):
        print("Please check!!!! src file not exit: %s" +  report_template_name)
        return False
    else:
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        dstfile = dst_dir + '/' + dst_name
        copyfile(report_template_name, dstfile)

    return dstfile

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def rpmpkg_formatting(file_name): 
    '''格式化输出存量json格式数据
    '''
    format_info = []
    for line in open(file_name, 'r'):
        format_info.append(line.replace('\n', ''))
    return json.dumps(format_info)

def get_system_info():
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

    return system_list

def get_softpkg_compatibility():
    '''
        应用场景：存量替换迁移检查-软件包对比
        功    能：1xxxa版软件包对比，按照前后端接口生成json格式的软件包对比数据
        输入参数：无
        返 回 值：json数据
    '''
    softpkg_page = FixedInfo.current_head_info + \
            get_cur_sys_version() + '","data":' + \
            rpmpkg_formatting(FixedInfo.unique_pkgname) + '},'

    return softpkg_page + FixedInfo.total_head_info + ',"data":' + \
            rpmpkg_formatting(FixedInfo.total_pkgname)+"}}," 

def get_rpm_chkinfo():
    '''
        应用场景：存量替换迁移检查-RPM兼容性对比
        功    能：1xxxa版RPM兼容性对比，按照前后端接口生成json格式的RPM兼容性检查数据
        输入参数：无
        返 回 值：json数据
    '''
    third_tab = ''
    rpm_file_name = FixedInfo.inventory_dir + '/abi-incomp-chk.csv'
    for line in open(rpm_file_name, 'r'):
        element_list = line.strip().split(',', 6)
        if element_list[4] == 'N':
            compatible = 'false'
            element = '{"name":"'+element_list[0]+\
                    '","is_compatible": '+compatible+\
                    ',"current_version": "'+element_list[2]+\
                    '","future_version": "'+element_list[3]+\
                    '","incompatible_type": "'+element_list[5]+\
                    '","incompatible_source": "'+element_list[1]+\
                    '","description": "'+element_list[6]+'"},'
        else:
            compatible = 'true'
            element = '{"name":"'+element_list[0]+\
                    '","is_compatible": '+compatible+'},'
        third_tab = third_tab + element
    return FixedInfo.page_rpm_tabs +third_tab.rsplit(',',1)[0]+']}}'

def xlsTohtml():
    '''
        应用场景：存量替换迁移评估检查，包括系统基本信息，软件包对比，RPM兼容性检测
        功    能：1xxxa版系统基本信息，软件包对比，RPM兼容性对比，按照前后端接口生成json格式数据
        输入参数：无
        返 回 值：json数据
    '''
    return get_system_info()+\
            get_softpkg_compatibility()+\
            get_rpm_chkinfo()

