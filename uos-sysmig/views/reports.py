import os
import json
from logger import *
from connect_sql import DBHelper
import pandas as pd
from datetime import datetime
from sysmig_agent.utils import *
from sysmig_agent.share import getSysMigConf
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
    data = {'report_pwd': report_pwd, 'report_name': report_name}
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
    data = {'report_pwd': report_pwd, 'report_name': report_name}
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
    data = {'report_pwd': report_pwd, 'report_name': report_name}
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
    data = {'report_pwd': report_pwd, 'report_name': report_name}
    return data


def export_host_info(data):
    """
    主机列表
    :return:
    """
    agent_online_status_tmp = (0, 1)
    agent_ip = data.get('agent_ip')
    if agent_ip == '':
        sql = "select agent_ip,hostname,agent_online_status,agent_os,agent_arch," \
              "agent_history_faild_reason from agent_info where agent_online_status in {};".format(agent_online_status_tmp)
    elif len(agent_ip) == 1:
        sql = "select agent_ip,hostname,agent_online_status,agent_os,agent_arch," \
              "agent_history_faild_reason from agent_info where agent_ip='{}' and agent_online_status in {};"\
            .format(agent_ip[0], agent_online_status_tmp)
    else:
        sql = "select agent_ip,hostname,agent_online_status,agent_os,agent_arch," \
              "agent_history_faild_reason from agent_info where agent_ip in {} and agent_online_status in {};"\
            .format(tuple(agent_ip), agent_online_status_tmp)
    data = DBHelper().execute(sql).fetchall()
    data = list(data)
    for i in range(0, len(data)):
        agent_task = "select task_CreateTime,task_data from agent_task where agent_ip='%s';" % data[i][0]
        get_agent_task = DBHelper().execute(agent_task)
        data[i] = list(data[i])
        if data[i][2] == 0:
            data[i][2] = '在线'
        else:
            data[i][2] = '离线'
        get_agent_task = list(get_agent_task)
        if get_agent_task == []:
            data[i] += ["", ""]
        else:
            task_CreateTime = get_agent_task[0][0].strftime('%Y-%-m-%d %H:%M:%S')
            task_status = get_agent_task[0][1]
            if task_status == '00':
                task_status = '未迁移'
            elif task_status == '09':
                task_status = "迁移成功"
            elif task_status[1] == "8":
                task_status = "迁移失败"
            else:
                task_status = "迁移中"
            data[i].append(task_CreateTime)
            data[i].append(task_status)
    df = pd.DataFrame(data)
    df.columns = ['主机IP', '主机名', '在线状态', '操作系统类型', '架构',  '历史失败原因', '迁移时间', '迁移状态']
    time = datetime.now().strftime('%Y-%-m-%d-%H-%M-%S')
    uos_sysmig_conf = json.loads(getSysMigConf())
    ip = json.loads(uos_sysmig_conf).get('serverip').strip()[1:-1]
    insert_report_sql = "insert into report_info(create_time, report_name, report_type, agent_ip) values (%s, %s, %s, %s);"
    val = ((time, "host_info_%s.xls" % time, "主机列表", ip),)
    DBHelper().insert(insert_report_sql, val)
    xls = "/var/uos-migration/host_info_%s.xls" % time
    df.to_excel(xls, index=False)

    report_pwd = "/var/uos-migration/"
    report_name = "host_info_%s.xls" % time
    data = {'report_pwd': report_pwd, 'report_name': report_name}
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
    df.to_excel(xls, index=False)
    report_pwd = "/var/uos-migration/"
    report_name = "migration_success_host_info_%s.xls" % time
    data = {'report_pwd': report_pwd, 'report_name': report_name}
    return data

