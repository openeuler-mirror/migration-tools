# -*- coding: utf-8 -*-
# !/usr/bin/python
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier:   MulanPubL-2.0-or-later

import os
import sys
import json
from func import share
from views import migration

from flask import Flask, render_template, url_for, request, redirect, make_response, session, Response
app = Flask(__name__)

mods = {
        'check_environment': migration.check_environment,
        'check_storage' : migration.check_storage,
        'check_os': migration.check_os,
        'check_os_kernel': migration.check_os_kernel,
        'check_migration_progress': migration.check_migration_progress,
        'check_progress': migration.check_progress,
        'check_repo': migration.check_repo,
        'check_repo_kernel': migration.check_repo_kernel,
        'check_user': migration.check_user,
        'close_tool': migration.close_tool,
        'export_migration_reports': migration.export_migration_reports,
        'system_migration':migration.system_migration,
        'migration_details': migration.migration_details,
        }


def check_methods():
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data)
        mod = mods.get(json_data['mod'])
        if mod:
            response_str = mod(data)
            return response_str


@app.route('/', methods=['GET', 'POST'])
def MT_index():
    """
    跳转起始界面
    :return:
    """
    return render_template('MT_agreement.html')


@app.route('/MT_agreement', methods=['GET', 'POST'])
def MT_agreement():
    """
    跳转协议许可界面
    :return:
    """
    return render_template('MT_agreement.html')


@app.route('/MT_note', methods=['GET', 'POST'])
def MT_note():
    """
    跳转用户需知界面
    :return:
    """
    return render_template('MT_note.html')


@app.route('/MT_check_env', methods=['GET', 'POST'])
def MT_check_env():
    """
    跳转系统环境检查界面
    :return:
    """
    return render_template('MT_check_evn.html')


@app.route('/MT_check_os', methods=['GET', 'POST'])
def MT_check_os():
    """
    检测系统版本
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')

    return render_template('MT_check_evn.html')


@app.route('/MT_check_storage', methods=['GET', 'POST'])
def MT_check_storage():
    """
    检测/var/cache空间大小
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')

    return render_template('MT_check_evn.html')


@app.route('/MT_close_tool', methods=['GET', 'POST'])
def MT_close_tool():
    """
    关闭迁移工具
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/MT_check_user', methods=['GET', 'POST'])
def MT_check_user():
    """
    检测用户账户
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')
    
    return render_template('MT_check_root.html')


@app.route('/MT_repo', methods=['GET', 'POST'])
def MT_repo():
    """
    跳转软件仓库界面
    :return:
    """
    return render_template('MT_repo.html')


@app.route('/MT_check_repo', methods=['GET', 'POST'])
def MT_check_repo():
    """
    检测软件仓库
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/MT_kernel', methods=['GET', 'POST'])
def MT_kernel():
    """
    跳转检测内核界面
    :return:
    """
    return render_template('MT_kernel.html') 


@app.route('/MT_check_os_kernel', methods=['GET', 'POST'])
def MT_check_os_kernel():
    """
    检测系统内核版本
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')

    return render_template('MT_kernel.html')


@app.route('/MT_repo_kernel', methods=['GET', 'POST'])
def MT_repo_kernel():
    """
    检测软件仓库内核版本
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')

    return render_template('MT_kernel.html')


@app.route('/Mt_environment', methods=['GET', 'POST'])
def Mt_environment():
    """
    跳转迁移前环境检测界面
    :return:
    """
    return render_template('MT_check_environment.html')


@app.route('/MT_check_environment', methods=['GET', 'POST'])
def MT_check_environment():
    """
    迁移前系统环境检查
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')
    return render_template('MT_check_environment.html')


@app.route('/MT_check_progress', methods=['GET', 'POST'])
def MT_check_progress():
    """
    环境检测进度检测
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')

    return render_template('MT_check_environment.html')


@app.route('/MT_export_migration_reports', methods=['GET', 'POST'])
def MT_export_migration_reports():
    """
    导出迁移检测报告
    :return:
    """
    mod = check_methods()
    f = open("/usr/lib/migration-tools-server/.passwd.txt","r")
    password = f.read()
    f.close()
    if mod:
        data = request.get_data()
        json_data = json.loads(data)
        mkdir_log_pwd = "/var/uos-migration/"
        isExists=os.path.exists(mkdir_log_pwd)
        if not isExists:
            try:
                os.makedirs(mkdir_log_pwd)
                print(mkdir_log_pwd)
            except:
                print("export report mkdir error:%s" % mkdir_log_pwd)

        info = mod.split(',')
        scp_log = "sshpass -p '%s'" % password + " scp -r %s" % json_data.get('info').split("|")[0] + "@%s" % info[1] \
                  + ":/var/tmp/uos-migration/UOS*.tar.gz /var/uos-migration/"
        try:
            os.system(scp_log)
            print(scp_log)
        except:
            print('export report scp error:%s' % scp_log)
        return Response(mod, content_type='application/json')


@app.route('/MT_migration', methods=['GET', 'POST'])
def MT_migration():
    """
    跳转迁移中界面
    :return:
    """
    return render_template('MT_migration.html')


@app.route('/MT_migration_progress', methods=['GET', 'POST'])
def MT_migration_progress():
    """
    迁移进度
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')

    return render_template('MT_migration.html')


@app.route('/MT_system_migration', methods=['GET', 'POST'])
def MT_system_migration():
    """
    迁移状态
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')

    return render_template('MT_migration.html')


@app.route('/MT_migration_results', methods=['GET', 'POST'])
def MT_migration_results():
    """
    跳转迁移完成界面
    :return:
    """
    return render_template('MT_migration_results.html')


@app.route('/MT_system_migration_info', methods=['GET', 'POST'])
def MT_system_migration_info():
    """
    迁移日志
    :return:
    """
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')

    return render_template('MT_migration.html')


if __name__ == '__main__':
    app.config["JSON_AS_ASCII"] = False
    uos_sysmig_conf = json.loads(share.getSysMigConf())
    ip = json.loads(uos_sysmig_conf).get('serverip').strip()[1:-1]
    port = int(json.loads(uos_sysmig_conf).get('serverport').strip()[1:-1])
    app.run(debug=True, host=ip, port=port)
