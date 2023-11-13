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



def init_remove_oldrepo():
    backup_comment = '#This is a yum repository file that was disabled . <Migration to UiniontechOS> \
            \n'
    path = '/etc/yum.repos.d/'
    repos = os.listdir(path)
    for repo in repos:
        path_file = path+'/'+repo
        if not os.path.isfile(path_file):
            continue
        if not re.search('repo$',repo):
            continue
        with open(path_file, 'r') as fsrc:
            content = fsrc.read()
            with open(path_file+'.disabled','w') as fdst:
                fdst.write(repo+'\n'+backup_comment+content)
                fdst.close()
            fsrc.close()
        os.remove(path_file)


#初始化repo文件
def initRepoFile(baseurl):
    os_version_ret = platform.dist()
    version = os_version_ret[1].split('.',-1)
    reposdir = '/etc/yum.repos.d/'
    h = 0
    if re.match('file:',baseurl):
        str0, path = baseurl.split('://',1)
        path = '/' + path.strip('/') + '/'
    else:
       h = 1
    if re.fullmatch('8',version[0]):
        path_appstream = baseurl+'/AppStream'
        path_baseos = baseurl+'/BaseOS'
        path_310 = baseurl+'/kernel-3.10'
        path_419 = baseurl+'/kernel419'
        path_510 = baseurl+'/kernel510'

        repostr_uos = '''[UniontechOS-AppStream]\nname = UniontechOS AppStream\nbaseurl = '''+path_appstream.strip('\n')+'''\nenabled = 1\ngpgcheck = 0\n\n[UniontechOS-BaseOS]\nname = UniontechOS BaseOS\nbaseurl = '''+path_baseos.strip('\n')+'''\nenabled = 1\ngpgcheck = 0\n\n[UniontechOS-kernel-4.19.0]\nname = UniontechOS Kernel-4.19.0\nbaseurl = '''+path_419.strip('\n')+'''\nenabled = 0\ngpgcheck = 0\nskip_if_unavailable = 1\n\n[UniontechOS-kernel-5.10.0]\nname = UniontechOS Kernel-5.10.0\nbaseurl = '''+path_510.strip('\n')+'''\nenabled = 0\ngpgcheck = 0\nskip_if_unavailable = 1\n\n
'''
    else:
        path_310 = baseurl+'/kernel-3.10'
        repostr_uos = '''[UniontechOS-AppStream]\nname = UniontechOS AppStream\nbaseurl = '''+baseurl.strip('\n')+'''\nenabled = 1\ngpgcheck = 0\n\n[UniontechOS-kernel-3.10.0]\nname = UniontechOS Kernel-3.10.0\nbaseurl = '''+path_310.strip('\n')+'''\nenabled = 0\ngpgcheck = 0\nskip_if_unavailable = 1\n
        '''
    repofile = os.path.join(reposdir, 'switch-to-uos.repo')
    with open(repofile,'w') as f_repo:
        f_repo.write(repostr_uos)
        f_repo.close()


#检测repo文件创建缓存
def checkRepoMakeCache():
    os.system('yum clean all')
    os.system('yum makecache')
    os_version_ret = platform.dist()
    os_arch = platform.machine()
    version = os_version_ret[1].split('.',-1)
    ret = os.path.exists('/var/cache/dnf/UniontechOS-AppStream.solv')
    if ret:
        ret = os.path.exists('/var/cache/dnf/UniontechOS-BaseOS.solv')
        if ret or re.fullmatch('7',version[0]):
            return 0
        else:
            return 1
    else:
        if re.fullmatch('7',version[0]):
            ret = os.path.exists('/var/cache/yum/%s/7/UniontechOS-AppStream/repomd.xml' % os_arch)
            if ret:
                return 0
        return 1


# 检测centos 8 系统上的 repo文件联通
def checkRepoFileHttp(baseurl):
    try:
        with request.urlopen(baseurl) as file:
            # print(file.status)
            # print(file.reason)
            if re.match('OK', file.reason):
                return 0
    except Exception as e:
        if re.match('HTTP Error 404|[Errno 2]', str(e)):
            return 1
        elif re.match('[Errno 21]', str(e)):
            return 0
        else:
            return 1


def repoFileCheck(baseurl):
    if re.match('file\:\/\/', baseurl):
        path = re.sub('file://', '', baseurl)
        if os.path.exists(path):
            return 0
        else:
            return 1
    try:
        dst_status = urllib.request.urlopen(baseurl, timeout=5).code
        return 0
    except Exception as err:
        return 1
        pass

def check_repo(data):
    agent_os = get_agent_os()
    if '7' in agent_os:
        agent_os = 'centos7'
    elif '8' in agent_os:
        agent_os = 'centos8'
    os_type = agent_os + '_' + platform.machine().strip('')
    baseurl = json.loads(data).get(os_type)
    if not baseurl:
        baseurl = '1'
    task_id = json.loads(data).get('task_id')
    # 更新SQL任务状态
    statue = 1
    sql_task_statue(statue, task_id)
    # 发送消息给Server更新任务流状态
    post_server('task_start', task_id)
    # 初始化去除旧的repo文件
    init_remove_oldrepo()
    # 传递baseurl，配置repo文件
    initRepoFile(baseurl)
    # 建立软件源缓存，判断软件源是否可用
    state = checkRepoMakeCache()
    sql = ''
    repo_state = -1
    if state == 0:
        repo_state = repoFileCheck(baseurl)
    else:
        repo_state = 1

    sql = "UPDATE agent_info SET repo_status = {} WHERE agent_ip = '{}';".format(repo_state, get_local_ip())
    try:
        ret = DBHelper().execute(sql)
        statue = 2
    except:
        statue = 2
        sql_task_statue(statue, task_id)
    sql_task_statue(statue, task_id)
    post_server('task_close', task_id)
    return 'success'
