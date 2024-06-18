#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import json
import platform

from config import FixedInfo
from migrationTools.scanHardware import utils

def hardware_tabs():
    '''硬件兼容性分析
        按照前后端接口，生成json格式数据，对应html报告tab页
    '''

    FixedInfo.hardware_tabs_head
    compatability_list = utils.get_compatability_list(
        utils.get_pci_list(), utils.get_supported_device_list(), False)
    json_str = FixedInfo.hardware_tabs_head + json.dumps(compatability_list)+'},'

    return json_str

def main():
    hardware_tabs()


if __name__ == "__main__":
    main()

