import os
import sys
import json
import socket
from shutil import copyfile

#for test
sys.path.append("../..")

from sysmig_agent.migrationTools.scanHardware import utils
from mig_merge.config import FixedPageInfo

def mycopyfile(template_name, dst_name):

    dst_dir = FixedPageInfo.report_dir
    report_template_name = FixedPageInfo.report_template_dir + '/' + template_name

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
    '''格式化输出存量json数据
    '''
    format_info = ''
    for line in open(file_name, 'r'):
        format_info = format_info+'"'+line.strip()+'",'
    return format_info.rsplit(',',1)[0]+"]},"

def get_system_info():
    '''
        应用场景：存量替换迁移检测-系统基本信息
        功    能：1xxxa版系统基本信息，按照前后端接口生成json格式系统基本信息
        输入参数：无
        返 回 值：json数据
    '''
    line_num = 0

    sysinfo_name = FixedPageInfo.inventory_data_dir + '/systeminfo.txt'
    for line in open(sysinfo_name, 'r'):
        line_num += 1

        if line_num == 2:
            middle_data = '"current_os_version": "'+line.strip().split('|')[1]+'",'
            system_list = FixedPageInfo.page_system_info + middle_data

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
    softpkg_page = FixedPageInfo.page_softpkg_first_column + \
            rpmpkg_formatting(FixedPageInfo.unique_pkgname)

    return softpkg_page + \
            FixedPageInfo.page_softpkg_third_column + \
            rpmpkg_formatting(FixedPageInfo.install_pkgname).rsplit(',', 1)[0]+"}," 

def get_rpm_chkinfo():
    '''
        应用场景：存量替换迁移检查-RPM兼容性对比
        功    能：1xxxa版RPM兼容性对比，按照前后端接口生成json格式的RPM兼容性检查数据
        输入参数：无
        返 回 值：json数据
    '''
    third_tab = ''
    rpm_file_name = FixedPageInfo.inventory_data_dir + '/abi-incomp-chk.csv'
    for line in open(rpm_file_name, 'r'):
        element_list = line.strip().split(',', 5)
        element = '{"name":"'+element_list[0]+\
                '","is_compatible": "'+element_list[3]+\
                '","current_version": "'+element_list[2]+\
                '","incompatibility_type": "'+element_list[4]+\
                '","incompatibility_sources": "'+element_list[1]+\
                '","description": "'+element_list[5]+'"},'
        third_tab = third_tab + element
    return FixedPageInfo.page_rpm_tabs +third_tab.rsplit(',',1)[0]+']},'

def xlsTohtml(hardware_json_info):
    '''
        应用场景：存量替换迁移评估检查，包括系统基本信息，软件包对比，RPM兼容性检测和硬件兼容性对比
        功    能：1xxxa版系统基本信息，软件包对比，RPM兼容性对比，按照前后端接口生成json格式数据
                  1xxxe版硬件兼容性对比，按照前后端接口生成json数据
        输出参数：hardware_json_info 硬件兼容性对比结果
        返 回 值：json数据
    '''
    return get_system_info()+\
            get_softpkg_compatibility()+\
            get_rpm_chkinfo()+\
            FixedPageInfo.page_hardware_tabs+\
            hardware_json_info+'}}'

