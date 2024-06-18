#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import json
import platform

from config import FixedInfo
from migrationTools.scanHardware import utils

def sysconffile_tabs():
    '''硬件兼容性分析
        按照前后端接口，生成json格式数据，对应html报告tab页
    '''

    json_str = '"sysconffile_tabs": {"confGroupName": "文件系统配置","confList": []}}'
    return json_str

def main():
    sysconffile_tabs()


if __name__ == "__main__":
    main()

