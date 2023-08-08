# coding=utf-8
'''''
main function：主要实现把txt中的每行数据写入到excel中
'''
#################
import json
import socket
import datetime

from func.share import *


#检测报告导出绝对路径
report_path_bef="/var/tmp/uos-migration/UOS_analysis_report/"
report_path_ago='/var/tmp/uos-migration/UOS_migration_log/'


def get_host_ip():
    """
    查询本机ip地址
    :return:
    """

    uos_sysmig_conf = json.loads(getSysMigConf())
    ip = json.loads(uos_sysmig_conf).get('agentip').strip()[1:-1]

    return ip


def abi_txt2xls():

    #兼容性检查报告名规则：UOS_migration_log_10.0.2.3_cy.server_202110192140.xls
    hostip = get_host_ip()
    hostname = socket.gethostname()
    excelFileName = "UOS_migration_log_"+hostip+"_"+hostname+"_"+datetime.datetime.now().strftime('%Y%m%d%H%M')+".xls"

    report_name_check=report_path_bef+excelFileName

    if os.path.exists(report_name_check):
        os.remove(report_name_check)