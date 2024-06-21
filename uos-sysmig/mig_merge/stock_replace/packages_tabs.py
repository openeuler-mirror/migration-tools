import os
import sys
import json
import socket
from shutil import copyfile

from logger import migration_log
from mig_merge.migrationTools.scanHardware import utils
from mig_merge.stock_replace.confirm import get_cur_sys_version
from mig_merge.config import FixedInfo

def rpmpkg_formatting(file_name):
    '''格式化输出存量json格式数据
    '''
    format_info = []
    for line in open(file_name, 'r'):
        format_info.append(line.replace('\n', ''))
    return json.dumps(format_info)


def packages_tabs():
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
def main():
    packages_tabs()


if __name__ == "__main__":
    main()
