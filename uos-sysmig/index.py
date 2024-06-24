# -*- coding: utf-8 -*-
# !/usr/bin/python
import os
import json
from flask import Flask, render_template, url_for, request, redirect, make_response, session, Response
os.chdir('/usr/lib/uos-sysmig-server/')
from connect_sql import *
from logger import *
from miscellaneous import *
from views.migration import *
from views.server import *
from flask_cors import CORS
from views.new_expansion import *
from multiprocessing import Queue, Process
from views.heartbeat import check_heartbeat


# import MySQLdb
os.chdir('/usr/lib/uos-sysmig-server/')
app = Flask(__name__, static_folder='../static', template_folder='../templates')
migration_log = Logger('/var/tmp/uos-migration/migration.log', logging.DEBUG, logging.DEBUG)
CORS(app, resources=r'/*')

@app.route('/')
def index():
    return render_template('index.html')

mods = {
        'import_host_info': import_host_info,
        'host_info_display': host_info_display,
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
        'close_tool': close_tool,
        'modify_task_status': modify_task_status,
        'check_add_repo': check_add_repo,
        'get_add_repo_data': get_add_repo_data,
        'check_add_environment': check_add_environment,
        'get_add_environment_data': get_add_environment_data,
        'modify_migration_type': modify_migration_type,
        }


def check_methods():
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data)
        mod = mods.get(json_data['mod'])
        if mod:
            response_str = mod(data)
            return response_str


@app.route('/modify_migration_type', methods=['GET', 'POST'])
def modify_migration_type():
    """
    修改迁移类型
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/check_add_repo', methods=['GET', 'POST'])
def check_add_repo():
    """
    下发新增扩容软件仓库检测
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/get_add_repo_data', methods=['GET', 'POST'])
def get_add_repo_data():
    """
    获取新增扩容软件仓库检测结果
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/check_add_environment', methods=['GET', 'POST'])
def check_add_environment():
    """
    下发新增扩容环境检测
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/get_add_environment_data', methods=['GET', 'POST'])
def get_add_environment_data():
    """
    获取新增扩容环境检测结果
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/modify_task_status', methods=['GET', 'POST'])
def modify_task_status():
    """
    修改任务状态
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


@app.route('/check_info', methods=['GET', 'POST'])
def check_info():
    """
    检测系统版本和空间大小
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


@app.route('/check_kernel', methods=['GET', 'POST'])
def check_kernel():
    """
    下发检测agent内核版本和软件仓库内核版本
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


@app.route('/export_reports', methods=['GET', 'POST'])
def export_reports():
    """
    导出迁移检测报告
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


@app.route('/close_tool', methods=['GET', 'POST'])
def close_tool():
    """
    关闭迁移软件
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


q = Queue()


@app.route('/heartbeat', methods=['GET', 'POST'])
def heartbeat():
    """
    写入队列
    :return:
    """
    if request.method == 'POST':
        data = request.get_data()
        agent_ip = json.loads(data).get("agent_ip")
        q.put(agent_ip)
        return 'success'


if __name__ == '__main__':
    app.debug = True
    app.config["JSON_AS_ASCII"] = False
    uos_sysmig_conf = json.loads(getSysMigConf('0.0.0.0'))
    ip = json.loads(uos_sysmig_conf).get('serverip').strip()[1:-1]
    port = int(json.loads(uos_sysmig_conf).get('serverport').strip()[1:-1])
    p = Process(target=check_heartbeat, args=(q,))
    p.start()
    app.run(debug=True, host=ip, port=port)

