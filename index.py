# -*- coding: utf-8 -*-
# !/usr/bin/python
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier:   MulanPubL-2.0-or-later

import os
import json
from flask import Flask, render_template, url_for, request, redirect, make_response, session, Response
os.chdir('/usr/lib/uos-sysmig-server')
from connect_sql import *
from logger import *
from sysmig_agent.share import getSysMigConf
from miscellaneous import *
from views.migration import *
from views.server import *
from flask_cors import CORS
# import MySQLdb

os.chdir('/usr/lib/uos-sysmig-server')
app = Flask(__name__)
migration_log = Logger('/var/tmp/uos-migration/migration.log', logging.DEBUG, logging.DEBUG)
CORS(app, resources=r'/*')
mods = {
        'import_host_info': import_host_info,
        'host_info_display': host_info_display,
        'delete_host_info': delete_host_info,
        'check_info': check_info,
        'get_page_data': get_page_data,
        'check_repo': check_repo,
        'get_repo_data': get_repo_data,
        'check_kernel': check_kernel,
        'get_kernel_data': get_kernel_data,
        'check_environment': check_environment,
        'get_environment_data': get_environment_data,
        'export_reports': export_reports,
        'system_migration': system_migration,
        'get_system_migration_data': get_system_migration_data,
        'sql_task': modify_task_stream,
        'get_download_center_data': get_download_center_data,
        'migration_records': migration_records,
        'get_migrated_hosts': get_migrated_hosts,
        'get_storage_num': get_storage_num,
        'get_repo_arch_info': get_repo_arch_info,
        'close_tool': close_tool,
        'modify_task_status': modify_task_status
        }


def check_methods():
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data)
        mod = mods.get(json_data['mod'])
        if mod:
            response_str = mod(data)
            return response_str

@app.route('/modify_task_status', methods=['GET', 'POST'])
def modify_task_status():
    """
    修改任务状态
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')

@app.route('/get_repo_arch_info', methods=['GET', 'POST'])
def get_repo_arch_info():
    """
    获取软件仓库架构和系统信息
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')

@app.route('/get_storage_num', methods=['GET', 'POST'])
def get_storage_num():
    """
    获取可用空间足够和不足数量
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')

@app.route('/export_migration_reports', methods=['GET', 'POST'])
def export_migration_reports():
    """
    导出报告
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')

@app.route('/import_host_info', methods=['GET', 'POST'])
def import_host_info():
    """
    导入主机信息
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/host_info_display', methods=['GET', 'POST'])
def host_info_display():
    """
    显示主机信息
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/sql_task', methods=['GET', 'POST'])
def modify_task_stream():
    """
    修改任务流
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/delete_host_info', methods=['GET', 'POST'])
def delete_host_info():
    """
    删除迁移主机
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/check_info', methods=['GET', 'POST'])
def check_info():
    """
    检测系统版本和空间大小
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/check_kernel', methods=['GET', 'POST'])
def check_kernel():
    """
    下发检测agent内核版本和软件仓库内核版本
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/get_kernel_data', methods=['GET', 'POST'])
def get_kernel_data():
    """
    获取系统内核和仓库内核版本
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/check_repo', methods=['GET', 'POST'])
def check_repo():
    """
    检测平台软件仓库
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/get_repo_data', methods=['GET', 'POST'])
def get_repo_data():
    """
    定时检查软件仓库检测结果
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')

@app.route('/get_kernel_data', methods=['GET', 'POST'])
def get_kernel_data():
    """
    获取系统内核和仓库内核版本
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')

@app.route('/check_environment', methods=['GET', 'POST'])
def check_environment():
    """
    agent迁移前环境检查任务
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/get_environment_data', methods=['GET', 'POST'])
def get_environment_data():
    """
    获取环境检查进度本
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/get_repo_arch_info', methods=['GET', 'POST'])
def get_repo_arch_info():
    """
    获取软件仓库架构和系统信息
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/get_storage_num', methods=['GET', 'POST'])
def get_storage_num():
    """
    获取可用空间足够和不足数量
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/export_reports', methods=['GET', 'POST'])
def export_reports():
    """
    导出迁移检测报告
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/get_page_data', methods=['GET', 'POST'])
def get_page_data():
    """
    定时获取可用空间页面数据
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/system_migration', methods=['GET', 'POST'])
def system_migration():
    """
    agent系统迁移
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/get_system_migration_data', methods=['GET', 'POST'])
def get_system_migration_data():
    """
    获取agent迁移进度
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/get_download_center_data', methods=['GET', 'POST'])
def get_download_center_data():
    """
    获取下载中心数据
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/migration_records', methods=['GET', 'POST'])
def migration_records():
    """
    获取迁移记录数据
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/get_migrated_hosts', methods=['GET', 'POST'])
def get_migrated_hosts():
    """
    获取迁移主机列表数据
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/', methods=['GET', 'POST'])
def MT_index():
    """
    跳转起始界面
    :return:
    """
    return render_template('MT_agreement.html')


@app.route('/close_tool', methods=['GET', 'POST'])
def close_tool():
    """
    关闭迁移软件
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


if __name__ == '__main__':
    app.debug = True
    app.config["JSON_AS_ASCII"] = False
    uos_sysmig_conf = json.loads(getSysMigConf())
    ip = json.loads(uos_sysmig_conf).get('serverip').strip()[1:-1]
    port = int(json.loads(uos_sysmig_conf).get('serverport').strip()[1:-1])
    info = "import Vue from 'vue'" + '\n' + "import axios from 'axios'" + '\n' + "axios.defaults.baseURL='http://%s:%s'" % (ip, port) + "\n" + "Vue.prototype.$http=axios"
    with open('template/src/plugins/axios.js', 'w+', encoding='utf-8') as f:
        f.write(info)
        f.close
    app.run(debug=True, host=ip, port=port, use_reloader=False)
