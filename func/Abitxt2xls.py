# coding=utf-8
'''''
main function：主要实现把txt中的每行数据写入到excel中
'''
#################
import json

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

