#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import rpm
import stat

from config import FixedInfo
from repo_sqlite.utils import run_cmd
from migrationTools.utils.logger import Logger
from migrationTools.scanRPM.scan_rpm import get_current_pkg_list

logger = Logger(__name__)

# Check whether it is an ELF file
def is_ELFfile(filepath):
    if not os.path.exists(filepath):
        return False
    try:
        FileStates = os.stat(filepath)
        FileMode = FileStates[stat.ST_MODE]
        if not stat.S_ISREG(FileMode) or stat.S_ISLNK(FileMode):
            return False
        with open(filepath, 'rb') as f:
            header = (bytearray(f.read(4)[1:4])).decode(encoding="utf-8")
            if header in ["ELF"]:
                return True
    except UnicodeDecodeError as e:
        pass
    return False


def binary_type(file_name):
    cmd = 'rpm -ql %s' %(file_name)
    _, data, _ = run_cmd(cmd)
    for line in data:
        if '.build-id' in line:
            continue

        if line == '':
            continue
        
        if '.' in line.rsplit('/', 1)[1]:
            current_suffix = '.' + line.rsplit('.', 1)[1]
            if current_suffix in FixedInfo.suffix_list:
                continue
        if not is_ELFfile(line):
            continue
        else:
            #查找连接文件

def rpm_trans():
    '''
        应用场景：
        功    能：
        输入参数：无
        返 回 值：
    '''
    #rpm_list = ['dos2unix-7.4.0-3.el8.x86_64','librepo-1.11.0-2.el8.x86_64', 'python3-hawkey-0.39.1-5.el8.x86_64']
    rpm_list = ['dos2unix-7.4.0-3.el8.x86_64']
    #for rpm_pkg in get_current_pkg_list():
    for rpm_pkg in rpm_list:
        binary_type(rpm_pkg)



    
def main():
    rpm_trans()

if __name__ == "__main__":
    main()

