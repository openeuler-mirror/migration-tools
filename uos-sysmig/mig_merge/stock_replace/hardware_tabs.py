#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import json
import platform

from mig_merge.config import FixedInfo
from mig_merge.migrationTools.scanHardware import utils

def hardware_tabs(logger):
    '''硬件兼容性分析
        按照前后端接口，生成json格式数据，对应html报告tab页
    '''
    return '{},'
    FixedInfo.hardware_tabs_head
    compatability_list = utils.get_compatability_list(
        utils.get_pci_list(), utils.get_supported_device_list(), False)
    hardware_tabs_json = FixedInfo.hardware_tabs_head + json.dumps(compatability_list)+'},'
    #logger.info('Get hardware tabs json data:' .format(hardware_tabs_json))
    return hardware_tabs_json

def main():
    hardware_tabs()


if __name__ == "__main__":
    main()

