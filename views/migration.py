# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier:   MulanPubL-2.0-or-later
import os

from connect_sql import DBHelper
from logger import *

from flask import *
from client_requests import *
from sysmig_agent.utils import *
from interaction import splice_url


migration_log = Logger('/var/tmp/uos-migration/migration.log', logging.DEBUG, logging.DEBUG)

def send_task_to_agent(data, url, ip):
    """
    向agent下发任务
    :param data:
    :param url:
    :param ip:
    :return:
    """
    log_info = "post " + url + ":" + str(data)
    migration_log.info(log_info)
    info = splice_url(data, url, ip)
    if info.status_code == 200:
        migration_log.info(info.text)
    elif info is None or info.status_code == 404:
        sql = "update agent_info set agent_online_status=1 where agent_ip ='%s';" % ip
        DBHelper().execute(sql)
        migration_log.error("%s:请求失败,agent端没有启动" % ip)
    elif info.status_code != 404 and info.status_code != 200:
        sql = "update agent_info set agent_online_status=1 where agent_ip ='%s';" % ip
        DBHelper().execute(sql)
        migration_log.error("%s:请求失败，错误状态码为%s" % (ip, info.status_code))


def get_agent_ip(data, sql, url):
    """
    获取agent_ip地址
    :return:
    """
    agent_info = DBHelper().execute(sql).fetchall()
    data = json.loads(data)
    for i in agent_info:
        task_status_sql = "select task_status from agent_task where agent_ip='%s'" % list(i)[0]
        task_status = DBHelper().execute(task_status_sql).fetchall()[0][0]
        if task_status == 0 or task_status == 2:
            update_sql = "update agent_task set task_progress=0,task_status=1 where agent_ip='%s'" % list(i)[0]
            DBHelper().execute(update_sql)
            get_task_id_sql = "select task_id from cur_task where agent_ip='%s'" % list(i)[0]
            task_id = DBHelper().execute(get_task_id_sql).fetchall()
            data['task_id'] = task_id[0][0]
            json_data = json.dumps(data)
            send_task_to_agent(json_data, url, list(i)[0])


def check_info(data):
    """
    检测系统版本和空间大小
    :param data:
    :return:
    """
    sql = "select agent_ip from agent_info where agent_online_status = 0;"
    get_agent_ip(data, sql, '/check_info')
    return 'success'


def check_kernel(data):
    """
    检测agent内核版本和软件仓库内核版本
    :param data:
    :return:
    """
    sql = "select agent_ip from agent_info where agent_online_status=0 and agent_storage>=10 and repo_status=0;"
    get_agent_ip(data, sql, '/check_kernel')
    return 'success'


def check_services(data, url):
    info = post_client_data(data, url)
    if info is None or info.status_code != 200:
        print("请求失败,客户端没有启动")
        return list_to_json(['res', 'error'], ['1', '迁移客户端没有启动'])
    else:
        return info.text


def check_environment(data):
    services = check_services(data, '/check_environment')
    if services:
        return services


def check_os(data):
    services = check_services(data, '/check_os')
    if services:
        return services


def check_storage(data):
    services = check_services(data, '/check_storage')
    if services:
        return services


def close_tool(data):
    os.system('kill -9 `ps -ef | grep "start_webview.py" | grep -v grep | awk \'{print $2}\'`')
    data = {"ip": "0.0.0.0"}
    data_json = json.dumps(data)
    return data_json


def check_user(data):
    services = check_services(data, '/check_user')
    if services:
        json_data = json.loads(data)
        with open('/usr/lib/migration-tools-server/.passwd.txt', 'w', encoding='utf-8') as f:
            text = json_data['passwd']
            f.write(text)
        return services


def check_repo(data):
    """
    检测平台软件仓库
    :param data:
    :return:
    """
    sql = "select agent_ip from agent_info where agent_online_status = 0 and agent_storage >= 10;"
    agent_ip_list = DBHelper().execute(sql)
    for i in agent_ip_list:
        repo_status_sql = "update agent_info set repo_status='2' where agent_ip='%s'" % list(i)[0]
        DBHelper().execute(repo_status_sql)
    get_agent_ip(data, sql, '/check_repo')
    return 'success'


def check_os_kernel(data):
    services = check_services(data, '/check_os_kernel')
    if services:
        return services


def check_repo_kernel(data):
    services = check_services(data, '/check_repo_kernel')
    if services:
        return services


def check_progress(data):
    services = check_services(data, '/check_progress')
    if services:
        return services


def check_migration_progress(data):
    services = check_services(data, '/check_migration_progress')
    if services:
        return services


def export_migration_reports(data):
    services = check_services(data, '/export_migration_reports')
    if services:
        return services


def system_migration(data):
    services = check_services(data, '/system_migration')
    if services:
        return services


def migration_details(data):
    services = check_services(data, '/migration_details')
    if services:
        return services
