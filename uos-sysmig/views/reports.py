import os
import json
from logger import *
from connect_sql import DBHelper
import pandas as pd
from datetime import datetime
from sysmig_agent.utils import *
from flask import send_from_directory


os.chdir('/usr/lib/uos-sysmig-server')
migration_log = Logger('/var/tmp/uos-migration/migration.log', logging.DEBUG, logging.DEBUG)


def uos_migration_log(data):
    """
    存量替换迁移日志
    :return:
    """
    agent_ip = data.get('agent_ip')
    dbwrite = DBwrite(agent_ip)
    dbwrite.write_completed_log()
    report_pwd = "/var/uos-migration/%s" % agent_ip
    report_name = dbwrite.write_completed_log()
    data = {'report_pwd': report_pwd,'report_name': report_name}
    return data


def migration_completed_report(data):
    """
    存量替换迁移分析报告
    :return:
    """
    agent_ip = data.get('agent_ip')
    dbwrite = DBwrite(agent_ip)
    report_pwd = "/var/uos-migration/%s" % agent_ip
    report_name = dbwrite.write_completed_html()
    data = {'report_pwd': report_pwd,'report_name': report_name}
    return data


def analysis_report(data):
    """
    存量替换迁移检测报告
    :return:
    """
    agent_ip = data.get('agent_ip')
    dbwrite = DBwrite(agent_ip)
    report_pwd = "/var/uos-migration/%s" % agent_ip
    report_name = dbwrite.write_analysis_html()
    data = {'report_pwd': report_pwd,'report_name': report_name}
    return data


def analysis_report_add(data):
    """
    新增扩容迁移检测报告
    :return:
    """
    agent_ip = data.get('agent_ip')
    dbwrite = DBwrite(agent_ip)
    report_pwd = "/var/uos-migration/%s" % agent_ip
    report_name = dbwrite.write_analysis_add_html()

    return send_from_directory(directory=report_pwd, filename=report_name, as_attachment=True)


def export_host_info(data):
    """
    主机列表
    :return:
    """
    agent_ip = data.get('agent_ip')
    if agent_ip == '':
        sql = "select agent_ip,hostname,agent_online_status,agent_os,agent_arch," \
              "agent_history_faild_reason from agent_info;"
    else if len(agent_ip) == 1:
        sql = "select agent_ip,hostname,agent_online_status,agent_os,agent_arch," \
              "agent_history_faild_reason from agent_info where agent_ip='%s';" % agent_ip[0]
    else:
        sql = "select agent_ip,hostname,agent_online_status,agent_os,agent_arch," \
              "agent_history_faild_reason from agent_info where agent_ip in {};".format(tuple(agent_ip))
    data = DBHelper().execute(sql).fetchall()
    data = list(data)
    for i in range(0, len(data)):
        agent_task = "select task_CreateTime,task_status from agent_task where agent_ip='%s';" % data[i][0]
        get_agent_task = DBHelper().execute(agent_task)
        data[i] = list(data[i])
        get_agent_task = list(get_agent_task)
        if get_agent_task == []:
            data[i] += ["", ""]
        else:
            task_CreateTime = get_agent_task[0][0].strftime('%Y-%-m-%d %H:%M:%S')
            task_status = get_agent_task[0][1]
            data[i].append(task_CreateTime)
            data[i].append(task_status)
    df = pd.DataFrame(data)
    df.columns = ['主机IP', '主机名', '在线状态', '操作系统类型', '架构',  '历史失败原因', '迁移时间', '迁移状态']
    time = datetime.now().strftime('%Y-%-m-%d-%H-%M-%S')
    xls = "/var/uos-migration/host_info_%s.xls" % time
    df.to_excel(xls)

    report_pwd = "/var/uos-migration/"
    report_name = "host_info_%s.xls" % time
    data = {'report_pwd': report_pwd,'report_name': report_name}
    return data


def migration_success_list(data):
    """
    迁移成功主机列表
    :param data:
    :return:
    """
    sql = "select agent_ip,hostname,agent_os,agent_migration_os,agent_arch from agent_info " \
          "where agent_migration_os is not null;"
    data = DBHelper().execute(sql).fetchall()
    data = list(data)
    for i in range(0, len(data)):
        data[i] = list(data[i])
        task_update_time_sql = "select task_Updatetime from agent_task where agent_ip='%s'" % data[i][0]
        get_task_update_time = DBHelper().execute(task_update_time_sql).fetchall()
        get_task_update_time = list(get_task_update_time)
        if get_task_update_time == []:
            data[i] += [""]
        else:
            task_Updatetime = get_task_update_time[0][0].strftime('%Y-%-m-%d %H:%M:%S')
            data[i].append(task_Updatetime)
    df = pd.DataFrame(data)
    df.columns = ['主机ip', '主机名', '迁移前OS版本', '迁移后OS版本', '架构', '迁移时间']
    time = datetime.now().strftime('%Y-%-m-%d-%H-%M-%S')
    xls = "/var/uos-migration/migration_success_host_info_%s.xls" % time
    df.to_excel(xls)
    report_pwd = "/var/uos-migration/"
    report_name = "migration_success_host_info_%s.xls" % time
    data = {'report_pwd': report_pwd,'report_name': report_name}
    return data

