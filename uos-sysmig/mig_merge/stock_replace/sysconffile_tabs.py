#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import json

from mig_merge.config import FixedInfo
from mig_merge.migrationTools.scanHardware import utils

def sysconffile_tabs():
    '''硬件兼容性分析
        按照前后端接口，生成json格式数据，对应html报告tab页
    '''

    sysconffile_tabs_json = '"sysconffile_tabs": {"name": "SysSconf","data": '

    PARAM_CONFIG_DIR = os.path.join(PathConf.data_path, "export-config")
    param_config_file = os.path.join(PARAM_CONFIG_DIR, "param_config.json")
    param_data = ParamData(param_config_file)

    sysconf_str = sysconffile_tabs_json + str(json.dumps(param_data.return_data)) + '}'
    return sysconf_str

def main():
    sysconffile_tabs()


if __name__ == "__main__":
    main()

