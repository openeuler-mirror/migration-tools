# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier:   MulanPubL-2.0-or-later

# import os
# import platform
# from share import list_to_json
# import sys
# import re
# import subprocess
# import json
from sysmig_agent.share import *
from flask import Flask, render_template, url_for, redirect, make_response, session, Response
import urllib.request
from sysmig_agent.agent_request import post_server

sys.path.append("..")
from connect_sql import DBHelper


def os_kernel():
    platformInfo = platform.platform()
    systemKernelVersion = platformInfo.split('-', -1)
    agent_kernel = systemKernelVersion[1]
    return agent_kernel



def os_repo_kernel():
    version_list = []
    os_version_ret = platform.dist()
    version = os_version_ret[1].split('.', -1)
    AGENT_OS = os_version_ret[0] + version[0]
    try:
        ret = os.popen("yum repolist all|awk '{print $1}'")
    except:
        ret = os.popen("yum repolist --all|awk '{print $1}'")
    kernel_repo = kernel_repo_name = []
    str_kernel = ''
    for r in ret.readlines():
        if not r:
            continue
        if 'UniontechOS' in r:
            kernel_repo.append(r.strip('\n'))
    if '8' == version[0]:
        for i in range(len(kernel_repo)):
            # cmd = 'yum repoquery  --nvr kernel --enablerepo ' + kernel_repo[i]
            cmd = 'yum repoquery --repo ' + kernel_repo[i] + ' kernel'
            ret = str(subprocess.check_output(cmd, shell=True), 'utf-8')[:-1]
            # except Exception:
            ret = ret.split('\n', -1)
            for i in range(len(ret)):
                if re.match('kernel', ret[i]):
                    kernel_version = re.sub('kernel-.*:', '', ret[i])
                    kernel_version = re.sub('-.*$', '', kernel_version)
                    version_list.append(kernel_version.strip())
                    if not str_kernel:
                        str_kernel = kernel_version.strip()
                    else:
                        str_kernel = str_kernel + ',' + kernel_version.strip()
                    # print(version_list)
    elif '7' == version[0]:
        for i in range(len(kernel_repo)):
            cmd = 'yum list --enablerepo {} kernel'.format(kernel_repo[i])
            if '3.10.0' in kernel_repo[i]:
                cmd = 'yum list --enablerepo {} --disablerepo UniontechOS-AppStream  kernel'.format(kernel_repo[i])
            ret = str(subprocess.check_output(cmd, shell=True), 'utf-8')[:-1]
            ret = ret.split('\n', -1)
            for n in range(len(ret)):
                if 'uelc' in ret[n]:
                    # kernel_version = re.sub('kernel-.* ', '', ret[n])
                    kernel_version = re.sub('-.*$', '', ret[n])
                    kernel_version = kernel_version.split(' ',-1)
                    kernel_version = kernel_version[len(kernel_version)-1]
                    version_list.append(kernel_version.strip())
                    if not str_kernel:
                        str_kernel = kernel_version.strip()
                    else:
                        str_kernel = str_kernel + ',' + kernel_version.strip()
    return str_kernel



def check_kernel(data):
    task_id = json.loads(data).get('task_id')
    # 更新SQL任务开始状态
    sql_task_statue('1', task_id)
    # 发送消息给Server更新任务流状态
    post_server('task_start', task_id )
    # agent kernel
    agent_kernel = os_kernel()
    # agent repo kernel
    agent_repo_kernel = os_repo_kernel()
    agent_ip = get_local_ip()
    statue = 1
    sql = "UPDATE agent_info SET agent_kernel = '{}',agent_repo_kernel = '{}' WHERE agent_ip = '{}';".format(
        agent_kernel, agent_repo_kernel, agent_ip)
    try:
        DBHelper().execute(sql)
        statue = 2
    except:
        statue = 3
        sql_task_statue(statue, task_id)
    sql_task_statue(statue, task_id)
    post_server('task_close', task_id)
    return 's'



def check_info(data):
    task_id = json.loads(data).get('task_id')
    # 更新SQL任务状态
    statue = 1
    sql_task_statue(statue, task_id)
    # 发送消息给Server更新任务流状态
    post_server('task_start', task_id)
    # 获取agent系统类型
    agent_os = get_agent_os()
    # agent storage
    agent_storage = os_storage()
    agent_ip = get_local_ip()
    sql = "UPDATE agent_info SET hostname = '{}', agent_os ='{}', agent_arch = '{}' ,agent_storage = {} ," \
          "agent_online_status = {} WHERE agent_ip = '{}';".format(platform.node(), agent_os, platform.machine(),
                                                                   agent_storage, 0, agent_ip)
    try:
        DBHelper().execute(sql)
        statue = 2
    except:
        statue = 3
        sql_task_statue(statue, task_id)
    # 更新SQL任务状态
    sql_task_statue(statue, task_id)
    post_server('task_close', task_id)
    return 'success'

def get_agent_os():
    os_version_ret = platform.dist()
    version = os_version_ret[1].split('.', -1)
    AGENT_OS = os_version_ret[0] + version[0]
    return AGENT_OS

