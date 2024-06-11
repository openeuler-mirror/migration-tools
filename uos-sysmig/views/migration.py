# -*- coding: utf-8 -*-
# !/usr/bin/python
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier:   MulanPubL-2.0-or-later

from connect_sql import *
from logger import *
from interaction import *
import json

os.chdir('/usr/lib/uos-sysmig-server')
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

def check_kernel(data):
    """
    检测agent内核版本和软件仓库内核版本
    :param data:
    :return:
    """
    sql = "select agent_ip from agent_info where agent_online_status=0 and agent_storage>=10 and repo_status=0;"
    get_agent_ip(data, sql, '/check_kernel')
    return 'success'

def check_environment(data):
    """
    agent迁移前环境检查任务
    :param data:
    :return:
    """
    agent_ip_list = json.loads(data).get('agent_ip')
    data = json.loads(data)
    url = '/check_environment'
    for i in agent_ip_list:
        get_task_id_sql = "select task_id from cur_task where agent_ip='%s'" % i
        task_id = DBHelper().execute(get_task_id_sql).fetchall()
        data['task_id'] = task_id[0][0]
        json_data = json.dumps(data)
        send_task_to_agent(json_data, url, i)
    return 'success'

def system_migration(data):
    """
    agent系统迁移
    :param data:
    :return:
    """
    agent_ip_list = json.loads(data).get('info')
    data = json.loads(data)
    url = '/system_migration'
    for i in agent_ip_list:
        get_task_id_sql = "select task_id from cur_task where agent_ip='%s'" % i.get('agent_ip')
        task_id = DBHelper().execute(get_task_id_sql).fetchall()
        data['task_id'] = task_id[0][0]
        json_data = json.dumps(data)
        send_task_to_agent(json_data, url, i.get('agent_ip'))
    return 'success'
