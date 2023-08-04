# -*- coding: utf-8 -*-
# !/usr/bin/python
import os
import sys
import json
from func import share
from views import migration

from flask import Flask, render_template, url_for, request, redirect, make_response, session, Response
app = Flask(__name__)

mods = {
        'check_storage' : migration.check_storage,
        'check_os': migration.check_os,
        'close_tool': migration.close_tool,
        'check_user': migration.check_user,
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

if __name__ == '__main__':
    app.config["JSON_AS_ASCII"] = False
    uos_sysmig_conf = json.loads(share.getSysMigConf())
    ip = json.loads(uos_sysmig_conf).get('serverip').strip()[1:-1]
    port = int(json.loads(uos_sysmig_conf).get('serverport').strip()[1:-1])
    app.run(debug=True, host=ip, port=port)
