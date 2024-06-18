# -*- coding: utf-8 -*-
# !/usr/bin/python
import json
from connect_sql import *
from datetime import datetime


def get_analysis_migrated_hosts(data):
    """
    获取迁移分析主机列表数据
    :param data:
    :return:
    """
    agent_ip_list = json.loads(data).get('agent_ip')
    if agent_ip_list == []:
        sql = "select agent_ip,agent_id,hostname,agent_online_status,agent_os,agent_arch,agent_history_faild_reason " \
              "from agent_info where agent_online_status='0' and agent_migration_os is null" \
              " and migration_type='new_expansion';"
    else:
        sql = "select agent_ip,agent_id,hostname,agent_online_status,agent_os,agent_arch,agent_history_faild_reason " \
              "from agent_info where agent_ip in %s and agent_online_status='0' and agent_migration_os is " \
              "null and migration_type='new_expansion';" % tuple(agent_ip_list)

    data = DBHelper().execute(sql).fetchall()
    data = list(data)
    finall_data = []
    for i in range(0, len(data)):
        data[i] = list(data[i])
        agent_task = "select task_CreateTime,task_data from agent_task where agent_ip='%s';" % data[i][0]
        get_agent_task = DBHelper().execute(agent_task).fetchall()
        get_agent_task = list(get_agent_task)
        if get_agent_task == []:
            pass
        else:
            task_CreateTime = get_agent_task[0][0].strftime('%Y-%-m-%d %H:%M:%S')
            task_status = get_agent_task[0][1]
            data[i].append(task_CreateTime)
            data[i].append(task_status)
            finall_data.append(data[i])
    res = {}
    res['num'] = len(finall_data)
    info_list = []
    info_dict_keys_list = ['agent_ip', 'agent_id', 'hostname', 'agent_online_status', 'agent_os', 'agent_arch',
                           'failure_reasons', 'task_CreateTime', 'task_status']
    for i in finall_data:
        info_list.append(dict(zip(info_dict_keys_list, i)))

    res['info'] = info_list
    json_res = json.dumps(res)


