#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import platform

from config import FixedInfo
from new_expansion.scan_rpms import scan_rpms
from migrationTools.scanHardware import utils
from migrationTools.utils.config import PathConf
from migrationTools.scanConf.scanconf import ScanConf
from migrationTools.exportSysConf.paramdata import ParamData

class MigrationMerge:

    def __init__(self) -> None:
        self.template_dir = FixedInfo.template_dir
        self.report_expansion_dir = FixedInfo.report_expansion_dir

        #data = self.sysconf_diff()
        #data = self.hardware_analysis()
        data = self.conf_scan()
        #data = data + self.rpms_scan()
        print('data = %s' %(data))

    def sysconf_diff(self):
        '''系统配置差异导出
            按照前后端接口，生成json格式数据，对应html报告tab页
        '''
        #PARAM_CONFIG_DIR = os.path.join(PathConf.data_path, "export-config")
        #param_config_file = os.path.join(PARAM_CONFIG_DIR, "param_config.json")
        #param_data = ParamData(param_config_file)
        #param_data = FixedInfo.expansion_page_head + '{"confGroupName": "文件系统配置","confList": [{'
        with open('json.txt', mode='r') as fp:
            param_data = str(fp.readlines()).replace('\\\\n', '\\n')

        print('param_data = %s' %(param_data))
        return param_data

    def hardware_analysis(self):
        '''硬件兼容性分析
            按照前后端接口，生成json格式数据，对应html报告tab页
        '''

        FixedInfo.hardware_tabs_head
        compatability_list = utils.get_compatability_list(
            utils.get_pci_list(), utils.get_supported_device_list(), False)
        jsonstr = FixedInfo.hardware_tabs_head + json.dumps(compatability_list)+'},'
        return jsonstr

    def conf_scan(self):
        '''收集当前系统上的信息配置信息
            按照前后端接口，生成json格式数据，对应html报告tab页
        '''
        data_01 = ScanConf.get_sysctl_a_data(self)
        data_02 = ScanConf.get_system_service_data(self)
        print('data_01 = %s' %(data_01))
        print('data_02 = %s' %(data_02))

        return str(data_01) + str(data_02)

    def rpms_scan(self):
        '''rpms包provide文件版本对比
            按照前后端接口，生成json格式数据，对应html报告tab页
        '''
        return scan_rpms()

def main():
    MigrationMerge()

if __name__ == "__main__":
    main()

