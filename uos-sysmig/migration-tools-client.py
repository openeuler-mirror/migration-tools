from flask import Flask, render_template, url_for, request, Response
from logger import Logger
from miscellaneous import *
from sysmig_agent.share import getSysMigConf
from sysmig_agent.fork import post_task, check_info
import os
import json
from multiprocessing import Process
from sysmig_agent.agent_request import post_heartbeat


app = Flask(__name__)
os.chdir('/usr/lib/migration-tools-agent/uos-sysmig')
migration_log = Logger('/var/tmp/uos-migration/UOS_migration_log/migration.log', logging.DEBUG, logging.DEBUG)


mods = {
        'check_info': post_task,
        'check_repo': post_task,
        'check_kernel': post_task,
        'check_environment': post_task,
        'system_migration': post_task,
        'check_add_repo': post_task,
        'check_add_environment': post_task
        }


def check_methods():
    if request.method == 'POST':
        data = request.get_data()
        migration_log.info(data)
        json_data = json.loads(data)
        mod = mods.get(json_data['mod'])
        if mod:
            response_str = mod(data)
            return response_str


@app.route('/check_info', methods=['GET', 'POST'])
def mt_check_info():
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/check_repo', methods=['GET', 'POST'])
def mt_check_repo():
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/check_kernel', methods=['GET', 'POST'])
def mt_check_kernel():
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/check_environment', methods=['GET', 'POST'])
def mt_check_environment():
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/system_migration', methods=['GET', 'POST'])
def mt_system_migration():
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/check_add_repo', methods=['GET', 'POST'])
def check_add_repo():
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/check_add_environment', methods=['GET', 'POST'])
def check_add_environment():
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


if __name__ == '__main__':
    app.debug = True
    app.config["JSON_AS_ASCII"] = False
    t_heart = Process(target=post_heartbeat)
    t_heart.start()
    check_info()
    uos_sysmig_conf = json.loads(getSysMigConf())
    ip = json.loads(uos_sysmig_conf).get('agentip').strip()[1:-1]
    port = json.loads(uos_sysmig_conf).get('agentport').strip()[1:-1]
    if '"' in port:
        port = port.split('"', -1)[0]
    app.run(debug=True, host=ip, port=int(port), use_reloader=False)



