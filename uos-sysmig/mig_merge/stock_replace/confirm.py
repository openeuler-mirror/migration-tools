import os
import sys
import rpm
import json

from logger import migration_log
from mig_merge.migrationTools.scanRPM.scan_rpm import get_current_pkg_list
from mig_merge.migrationTools.scanRPM.db_operates import DBOperate
from mig_merge.config import FixedInfo

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

def get_cur_sys_version():
    '''
        应用场景：系统说明信息
        功    能：获取系统说明，如 CentOS Linux 8 (Core)
        输入参数：无
        返 回 值：CentOS Linux 8 (Core)
    '''
    fp = open('/etc/os-release', 'r')
    for line in fp:
        if 'PRETTY_NAME' in line:
            break
    fp.close()
    return line.split('=',1)[1].replace('"','').replace('\n','')


def gen_migration_behind_rpms():
    '''
        应用场景：系统迁移成功后，rpm包列表
        功    能：获取当前系统release为【uelc20】的rpm包列表
        输入参数：无
        返 回 值：rpm包名列表
    '''

    dist='.uelc20'
    ts = rpm.TransactionSet()
    mi = ts.dbMatch()

    behind_rpms_list = []
    for rpm_pkg in mi:
        print(rpm_pkg['release'].decode())
        if dist in rpm_pkg['release'].decode():
            behind_rpms_list.append(rpm_pkg['name'].decode()+'\n')
    return json.dumps(behind_rpms_list)


def gen_migration_info():
    '''
        应用场景：生成存量替换迁移分析后台数据
        功    能：读取rpm包数据文件，获取迁移后系统rpm包列表
                  按照前后端接口生成json格式数据
        输入参数：无
        返 回 值：
    '''

    newline = "\\n'"
    single_quotes = "'"

    with open(FixedInfo.sys_version, mode='r') as fsp:
        sys_version = fsp.read().replace('\n', '')

    head_data = FixedInfo.head_info + FixedInfo.current_info + sys_version + '",'

    with open(FixedInfo.migration_eln, mode='r') as fbp:
        current_data = '"data":' + str(fbp.readlines()).replace(newline, '"').replace(single_quotes, '"')
    analysis_data = head_data + current_data + '},'


    data_info = analysis_data + FixedInfo.future_info + get_cur_sys_version() + '",'
    current_data = '"data":' + gen_migration_behind_rpms()
    future_data = data_info + current_data + '},'

    data_info = future_data + FixedInfo.total_info + get_cur_sys_version() + '",'
    with open(FixedInfo.migration_uelc, mode='r') as fup:
        current_data = '"data":' + str(fup.readlines()).replace(newline, '"').replace(single_quotes, '"')
    total_data = data_info + current_data + '}}}'

    return total_data

def gen_uelc_rpms(uelc_name):
    '''
        应用场景：跳过存量替换迁移检查，获取系统所有rpm包
        功    能：从.sqlite中获取所有rpm包名，作为存量替换迁移分析报告中数据
        输入参数：无
        返 回 值：True-生成全量rpm包文成功件
    '''

    if os.path.isfile(uelc_name):
        os.remove(uelc_name)
    if not os.path.exists(os.path.dirname(uelc_name)):
        os.makedirs(os.path.dirname(uelc_name))
    all_rpms = ''
    fp = open(uelc_name, mode='w')
    with DBOperate(FixedInfo.sqlite_name) as db:
        db.execute_sql("select * from packages")
        for row in db.cursor:
            fp.write(row[2]+'\n')
            all_rpms = all_rpms + row[2]+','
    fp.close()
    return all_rpms.rsplit(',', 1)[0]

def gen_eln_rpms(eln_name, uos_rpms_list):
    '''
        应用场景：系统迁移前，当前系统特有rpm包
        功    能：当前系统存在，uos源不存在的rpm包
        输入参数：eln_name当前系统特有rpm包文件名
                  uos_rpms_list uos源中rpm包列表
        返 回 值：True-成功；False-失败
    '''

    dist='.uelc20'
    ts = rpm.TransactionSet()
    mi = ts.dbMatch()

    fp = open(eln_name, mode='w')
    for rpm_pkg in mi:
        #迁移前获取rpm包信息，过滤掉release为uelc20的包
        if dist not in rpm_pkg['release'].decode():
            if rpm_pkg['name'] not in uos_rpms_list:
                fp.write(rpm_pkg['name'].decode() + '\n')
    fp.close()

    return True

def migration_confirm():
    '''
        应用场景：存量替换迁移分析操作之前，rpm包信息存在性判断
        功    能：确认是否存在rpm包信息文件，有-成功；无-生成
        输入参数：无
        返 回 值：0-存在rpm包信息文件；'1'-生成rpm包信息文件成功
    '''

    file_eln = FixedInfo.migration_eln
    file_uelc = FixedInfo.migration_uelc

    if os.path.isfile(file_eln) and os.path.isfile(file_uelc): 
        migration_log.info('migration before the current system rpms files exist!!!')
        return '0'

    uelc_list = gen_uelc_rpms(file_uelc)
    if uelc_list:
        migration_log.info('get uos repo source rpms list success')

    if gen_eln_rpms(file_eln,uelc_list):
        migration_log.info('get eln unique rpms file success')

    return '1'

