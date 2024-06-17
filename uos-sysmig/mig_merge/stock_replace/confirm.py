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

def read_migration_before_info(before_name):
    newline = "\\n'"
    single_quotes = "'"

    migration_behind_name = 
    with open(before_name, mode='r') as fbp:
        return str(fbp.readlines()).replace(newline, '"').replace(single_quotes, '"')


def migration_confirm():
    '''
        应用场景：存量替换迁移分析操作之前，系统rpm包信息获取
        功    能：是否存在rpm包信息文件？有-返回成功；无-生成
        输入参数：无
        返 回 值：0-存在rpm包信息文件；1-生成rpm包信息文件成功
    '''
    migration_file_name = FixedPageInfo.inventory_data_dir + '/migration-before-eln-rpm-tmp.csv'

    if os.path.isfile(migration_file_name): 
        read_migration_before_info(migration_file_name)
        return '0'
     
    dist='.uelc20'
    ts = rpm.TransactionSet()
    mi = ts.dbMatch()

    fp = open(migration_file_name, mode='w')
    if system_version_id()== '7':
        for rpm_pkg in mi:
            #迁移前获取rpm包信息，过滤掉release为uelc20的包
            if dist not in rpm_pkg['release'].decode():
                fp.write(rpm_pkg['name'].decode()+'\n')
    else:
        for rpm_pkg in mi:
            if dist not in rpm_pkg['release']:
                fp.write(rpm_pkg['name']+'\n')
    fp.close()
    get_rpms_from_sqlite()
    return '1'

