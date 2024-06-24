# -*- coding: utf-8 -*-
# !/usr/bin/python
import json
from connect_sql import *
from datetime import datetime


def get_add_repo_data(data):
    """
    获取新增扩容软件仓库检测结果
    :return:
    """
    agent_ip_list = json.loads(data).get('agent_ip')
    if agent_ip_list == []:
        task_status_sql = "select agent_id from agent_task where task_status=2"
    elif len(agent_ip_list) == 1:
        task_status_sql = "select agent_id from agent_task where task_status=2 and agent_ip='%s';" % agent_ip_list[0]
    else:
        task_status_sql = "select agent_id from agent_task where task_status=2 and " \
                          "agent_ip in {};".format(tuple(agent_ip_list))
    get_task_status = DBHelper().execute(task_status_sql).fetchall()
    if len(get_task_status) == 0:
        data = {"migration_before_x86_64": "", "migration_after_x86_64": "", "migration_before_aarch64": "",
                "migration_after_aarch64": ""}
        json_data = json.dumps(data)
        return json_data
    else:
        if agent_ip_list == []:
            repo_status_sql = "select repo_status from agent_info where agent_online_status='0' and " \
                              "agent_migration_os is null and migration_type='new_expansion';"
        elif len(agent_ip_list) == 1:
            repo_status_sql = "select repo_status from agent_info where agent_online_status='0' and " \
                              "agent_migration_os is null and migration_type='new_expansion' " \
                              "and agent_ip='%s';" % agent_ip_list[0]
        else:
            repo_status_sql = "select repo_status from agent_info where agent_online_status='0' " \
                              "agent_migration_os is null and agent_ip in {} and " \
                              "migration_type='new_expansion';".format(tuple(agent_ip_list))

        data = {"migration_before_x86_64": "success", "migration_after_x86_64": "success",
                "migration_before_aarch64": "success", "migration_after_aarch64": "success"}

        get_repo_status = DBHelper().execute(repo_status_sql).fetchall()
        for i in get_repo_status:
            if i[0][0] == 1:
                data["migration_before_x86_64"] = 'failed'
            if i[0][1] == 1:
                data["migration_after_x86_64"] = 'failed'
            if i[0][2] == 1:
                data["migration_before_aarch64"] = 'failed'
            if i[0][3] == 1:
                data["migration_after_aarch64"] = 'failed'

        json_data = json.dumps(data)
        return json_data


def get_add_environment_data(data):
    """
    获取新增扩容分析进度
    :return:
    """
    agent_ip_list = json.loads(data).get('agent_ip')
    if agent_ip_list == []:
        get_environment_pro_sql = "select agent_ip,task_progress,task_status from agent_task " \
                                  "and migration_type='new_expansion';"
    elif len(agent_ip_list) == 1:
        get_environment_pro_sql = "select agent_ip,task_progress,task_status from agent_task " \
                                  "and migration_type='new_expansion' and agent_ip='%s';" % agent_ip_list[0]
    else:
        get_environment_pro_sql = "select agent_ip,task_progress,task_status from agent_task where agent_ip in {} " \
                                  "and migration_type='new_expansion';".format(tuple(agent_ip_list))
    progress = DBHelper().execute(get_environment_pro_sql).fetchall()
    res = {}
    info_list = []
    finall_progress = []
    for i in progress:
        sql = "select agent_id from agent_info where agent_ip='%s' and agent_online_status=0 and repo_status='0' " \
              "and agent_migration_os is null;" % i[0]
        get_sql = DBHelper().execute(sql).fetchall()
        if get_sql:
            finall_progress.append(list(i))

    info_dict_keys_list = ['agent_ip', 'task_progress', 'task_status']
    for i in finall_progress:
        info_list.append(dict(zip(info_dict_keys_list, list(i))))

    res['info'] = info_list
    res['num'] = len(finall_progress)

    json_res = json.dumps(res)
    return json_res
