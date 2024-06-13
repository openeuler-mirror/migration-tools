import os
import sys
import rpm
import json

#for test
sys.path.append("../..")

from mig_merge.config import FixedPageInfo
from sysmig_agent.migrationTools.scanRPM.scan_rpm import get_current_pkg_list
from sysmig_agent.migrationTools.scanRPM.db_operates import DBOperate

def system_version_id():
    '''
        应用场景：获取系统版本标识,获取当前系统rpm包不同的方式
        功    能：centos8.*标识'8',centos7.*标识'7'
        输入参数：无
        返 回 值：系统标识8/7
    '''
    fp = open('/etc/os-release', 'r')
    for line in fp:
        if 'VERSION_ID' in line:
            break
    fp.close()
    return line.split('=',1)[1].replace('"','').replace('\n','')


