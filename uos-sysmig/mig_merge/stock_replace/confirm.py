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

def get_rpms_from_sqlite():
    '''
        应用场景：跳过存量替换迁移检查，获取系统所有rpm包
        功    能：从.sqlite中获取所有rpm包名，作为存量替换迁移分析报告中数据
        输入参数：无
        返 回 值：0-生成全量rpm包文成功件
    '''

    migration_file_name = FixedPageInfo.inventory_data_dir + '/migration-before-uelc20-rpm-tmp.csv'
    if os.path.isfile(migration_file_name):
        os.remove(migration_file_name)
    fp = open(migration_file_name, mode='w')

    with DBOperate(FixedPageInfo.sqlite_name) as db:
        db.execute_sql("select * from packages")
        for row in db.cursor:
            fp.write(row[2]+'\n')
    fp.close()
    return 'success'


