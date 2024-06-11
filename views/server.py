import json
import os
import re
import paramiko
from datetime import datetime

from connect_sql import DBHelper
from sysmig_agent.share import getSysMigConf
from views import reports
from logger import *


os.chdir('/usr/lib/uos-sysmig-server')
migration_log = Logger('/var/tmp/uos-migration/migration.log', logging.DEBUG, logging.DEBUG)


def agent_rpm_issued(data):
    """
    agent安装rpm软件包
    :return:
    """
    agent = os.system("sshpass -p %s ssh %s@%s yum install -y uos-sysmig-agent" % (str(data[2], encoding="utf-8"), data[1], data[0]))
    cp_uos_sysmig_conf = os.system("sshpass -p %s scp -r /etc/uos-sysmig/uos-sysmig.conf %s@%s:/etc/uos-sysmig/uos-sysmig.conf" %
                                   (str(data[2], encoding="utf-8"), data[1], data[0]))
    restart_server = os.system("sshpass -p %s ssh %s@%s systemctl restart uos-sysmig-agent" % (str(data[2], encoding="utf-8"), data[1], data[0]))
    if agent == 0 and restart_server == 0 and cp_uos_sysmig_conf == 0:
        return 'success'
    else:
        return 'faild'


def close_tool(data):
    """
    关闭迁移软件
    :param data:
    :return:
    """
    os.system('kill -9 `ps -ef | grep "start_webview.py" | grep -v grep | awk \'{print $2}\'`')
    data = {"data": "success"}
    data_json = json.dumps(data)
    return data_json


def check_user():
    """
    检测账户权限
    :return:
    """
    sql = "select agent_ip, agent_username, AES_DECRYPT(agent_passwd, 'coco') from agent_info where agent_online_status='0';"
    data = DBHelper().execute(sql).fetchall()
    success_num = 0
    port = 22
    for value in data:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(value[0], username=value[1], password=str(value[2], encoding="utf-8"), port=port)
            if value[1] != "root":
                stdin, stdout, stderr = ssh.exec_command('sudo -v')
                flag = True
                ret = stderr.read().decode()
                ret = ret.split('\n')[:-1]
                for i in range(len(ret)):
                    if re.match('sudo', ret[i].strip()[0:4]):
                        flag = False
                if flag:
                    if ret != 'sudo':
                        update_agent_online_status(value[0])

            ssh.close()
            data = agent_rpm_issued(value)
            if data == 'success':
                success_num += 1
            else:
                update_agent_online_status(value[0])
        except:
            migration_log.error("error:" + value[0] + value[1] + str(value[2], encoding="utf-8") + str(port))
            update_agent_online_status(value[0])

    res = {"data": "success", "num": success_num}
    if success_num == 0:
        res = {"data": "faild"}
    del success_num 
    return res


def import_host_info(data):
    """
    导入agent主机信息
    :param data:
    :return:
    """
    agent_info = json.loads(data).get("data")
    if not agent_info:
        data = {"data": "faild"}
        json_data = json.dumps(data)
        return json_data


    sql = "insert into agent_info(agent_ip, agent_username, agent_passwd) values (%s, %s, AES_ENCRYPT(%s, 'coco'));"
    for i in agent_info:
        agent_ip = i.get('agent_ip')
        agent_username = i.get('agent_hostname')
        agent_passwd = i.get('agent_password')
        val = ((agent_ip, agent_username, agent_passwd),)
        DBHelper().insert(sql, val)
        create_task_stream(agent_ip)

    time = datetime.now().strftime('%Y-%-m-%d %H:%M:%S')
    uos_sysmig_conf = json.loads(getSysMigConf())
    ip = json.loads(uos_sysmig_conf).get('serverip').strip()[1:-1]
    host_report_sql = "insert into report_info(agent_ip,create_time,report_name,report_type) values (%s, %s, %s, %s);"
    host_report_sql_val = ((ip, time, '迁移主机列表_%s' % time, '主机列表'),)
    DBHelper().insert(host_report_sql, host_report_sql_val)
    data = check_user()
    data_json = json.dumps(data)
    return data_json


def get_agent_id(agent_ip):
    """
    获取agent_id
    :param agent_ip:
    :return:
    """
    sql = "select agent_id from agent_info where agent_ip='%s'" % agent_ip
    get_agent_id = DBHelper().execute(sql).fetchall()
    return get_agent_id[0][0]


def create_task_stream(agent_ip):
    """
    创建任务流
    :return:
    """
    create_task_stream_sql = "insert into task_stream(agent_ip,agent_id,stream_status," \
                             "stream_CreateTime,stream_Updatetime) values (%s, %s, %s, %s, %s);"

    stream_status = 'None'
    agent_id = get_agent_id(agent_ip)
    time = datetime.now().strftime('%Y-%-m-%d %H:%M:%S')
    values = ((agent_ip, agent_id, stream_status, time, time),)
    DBHelper().insert(create_task_stream_sql, values)
    
    create_cur_task_sql = "insert into cur_task(task_status,stream_CreateTime,stream_Updatetime," \
                          "agent_ip) values (%s, %s, %s, %s);"
    values = (('None', time, time, agent_ip),)
    DBHelper().insert(create_cur_task_sql, values)

    get_task_id = "select max(task_id) task_id from cur_task"
    task_id = DBHelper().execute(get_task_id).fetchone()
    task_stream_id_sql = "select task_stream_id from task_stream where agent_ip='%s'" % agent_ip
    task_stream_id = DBHelper().execute(task_stream_id_sql).fetchone()
    values = ((agent_id, agent_ip, task_id[0], 0, 0, time, time, task_stream_id[0], "00"),)
    create_agent_task_sql = "insert into agent_task(agent_id,agent_ip,task_id,task_status,task_progress," \
                            "task_CreateTime,task_Updatetime,task_stream_id,task_data) values " \
                            "(%s, %s, %s, %s, %s, %s, %s, %s, %s);"
    DBHelper().insert(create_agent_task_sql, values)


def pagebreak(data, page, size):
    """
    页面数据分页
    :param data:
    :return:
    """
    page_start = (page - 1) * size
    page_end = page * size
    result = data[page_start:page_end]

    return result

def host_info_display(data):
    """
    显示主机信息
    agent_ip,hostname,agent_online_status,agent_os,agent_arch,
    agent_history_faild_reason,task_CreateTime,task_status
    :return:
    """
    page = json.loads(data).get('page')
    size = json.loads(data).get('size')
    sql = "select agent_ip,hostname,agent_online_status,agent_os,agent_arch," \
          "agent_history_faild_reason from agent_info;"
    data = DBHelper().execute(sql).fetchall()
    data = list(data)
    for i in range(0, len(data)):
        data[i] = list(data[i])
        agent_task = "select task_CreateTime,task_data from agent_task where agent_ip = '%s';" % data[i][0]
        get_agent_task = DBHelper().execute(agent_task).fetchall()
        get_agent_task = list(get_agent_task)

        if not get_agent_task:
            data[i] += ["", ""]
        else:
            task_CreateTime = get_agent_task[0][0].strftime('%Y-%-m-%d %H:%M:%S')
            task_status = get_agent_task[0][1]
            data[i].append(task_CreateTime)
            data[i].append(task_status)

    res = {}
    res['num'] = len(data)
    info_list = []
    info_dict_keys_list = ['agent_ip', 'hostname', 'agent_online_status', 'agent_os', 'agent_arch',
                           'failure_reasons', 'task_CreateTime', 'task_status']
    for i in data:
        info_list.append(dict(zip(info_dict_keys_list, i)))

    page_list = pagebreak(info_list, page, size)
    res['info'] = page_list
    res['page'] = page
    res['size'] = size

    json_res = json.dumps(res)
    return json_res


def modify_task_stream(data):
    """
    修改任务流状态
    :return:
    """
    task_id = json.loads(data).get('task_id')
    get_task_status_sql = "select task_status,task_stream_id from agent_task where task_id='%s';" % task_id
    info = DBHelper().execute(get_task_status_sql).fetchone()
    task_status = info[0]
    task_stream_id = info[1]
    if task_status == 0:
        task_status = 'None'
    elif task_status == 1:
        task_status = 'Doing'
    elif task_status == 2:
        task_status = 'Done'
    else:
        task_status = 'Cancel'
    time = datetime.now()
    modify_task_status_sql = "update cur_task set task_status='%s',stream_Updatetime='%s' " \
                             "where task_id ='%s';" % (task_status, time, task_id)
    DBHelper().execute(modify_task_status_sql)

    modify_task_stream_sql = "update task_stream set stream_status='%s',stream_Updatetime='%s' " \
                             "where task_stream_id='%s';" % (task_status, time, task_stream_id)
    DBHelper().execute(modify_task_stream_sql)
    return 'success'


def delete_host_info(data):
    """
    删除主机信息
    :return:
    """
    data = json.loads(data)
    for i in data.get('agent_ip'):
        sql = "delete from agent_info where agent_ip='%s';" % i
        DBHelper().execute(sql)
        sql = "delete from agent_task where agent_ip='%s';" % i
        DBHelper().execute(sql)
        sql = "delete from task_stream where agent_ip='%s';" % i
        DBHelper().execute(sql)
        sql = "delete from cur_task where agent_ip='%s';" % i
        DBHelper().execute(sql)

    res = {'data': 'success'}
    json_res = json.dumps(res)
    return json_res


def get_kernel_data(data):
    """
    获取系统内核和仓库内核版本
    :return:
    """
    get_kernel_version_sql = 'select agent_ip,agent_kernel,agent_repo_kernel from agent_info where ' \
                             'agent_online_status=0 and repo_status=0 and agent_storage>=10 and ' \
                             'agent_migration_os is null;'
    data = DBHelper().execute(get_kernel_version_sql).fetchall()
    res = {}
    info_list = []
    info_dict_keys_list = ['agent_ip', 'agent_kernel', 'agent_repo_kernel']
    if len(data) != 0:
        for i in data:
            if i[1] and i[2]:
                kernel_arr = ('不迁移内核' + ',' + i[2]).split(',')
                kernel_list = list(i)
                kernel_list[2] = kernel_arr
            else:
                kernel_list = [list(i)[0], '', '']
            info_list.append(dict(zip(info_dict_keys_list, kernel_list)))

    res['info'] = info_list
    res['num'] = len(info_list)

    json_res = json.dumps(res)
    return json_res


def get_repo_data(data):
    """
    定时检查软件仓库检测结果
    :return:
    """
    task_status_sql = "select agent_id from agent_task where task_status=2"
    get_task_status = DBHelper().execute(task_status_sql).fetchall()
    if len(get_task_status) == 0:
        data = {"centos7_x86": "", "centos8_x86": "", "centos7_aarch64": "", "centos8_aarch64": ""}
        json_data = json.dumps(data)
        return json_data
    else:
        centos7_x86_sql = "select agent_ip from agent_info where (agent_os='centos7' or agent_os='redhat7') " \
                          "and agent_arch='x86_64' and repo_status=1;"

        centos8_x86_sql = "select agent_ip from agent_info where (agent_os='centos8' or agent_os='redhat8') " \
                          "and agent_arch='x86_64' and repo_status=1;"

        centos7_aarch64_sql = "select agent_ip from agent_info where (agent_os='centos7' or agent_os='redhat7') " \
                              "and agent_arch='aarch64' and repo_status=1;"

        centos8_aarch64_sql = "select agent_ip from agent_info where (agent_os='centos8' or agent_os='redhat8') " \
                              "and agent_arch='aarch64' and repo_status=1;"

        data = {}
        get_centos7_x86_status = DBHelper().execute(centos7_x86_sql).fetchall()
        if len(get_centos7_x86_status) == 0:
            data['centos7_x86'] = 'success'
        else:
            data['centos7_x86'] = 'faild'

        get_centos8_x86_status = DBHelper().execute(centos8_x86_sql).fetchall()
        if len(get_centos8_x86_status) == 0:
            data['centos8_x86'] = 'success'
        else:
            data['centos8_x86'] = 'faild'

        get_centos7_aarch64_status = DBHelper().execute(centos7_aarch64_sql).fetchall()
        if len(get_centos7_aarch64_status) == 0:
            data['centos7_aarch64'] = 'success'
        else:
            data['centos7_aarch64'] = 'faild'

        get_centos8_aarch64_status = DBHelper().execute(centos8_aarch64_sql).fetchall()
        if len(get_centos8_aarch64_status) == 0:
            data['centos8_aarch64'] = 'success'
        else:
            data['centos8_aarch64'] = 'faild'

        json_data = json.dumps(data)
        return json_data


def get_environment_data(data):
    """
    获取环境检查进度
    :return:
    """
    get_environment_pro_sql = "select agent_ip,task_progress,task_status from agent_task;"
    progress = DBHelper().execute(get_environment_pro_sql).fetchall()
    res = {}
    info_list = []
    finall_progress = []
    for i in progress:
        sql = "select agent_id from agent_info where agent_ip='%s' and agent_online_status=0 and repo_status=0 " \
              "and agent_storage>=10 and agent_migration_os is null;" % i[0]
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


def get_repo_arch_info(data):
    """
    获取软件仓库架构和系统信息
    :param data:
    :return:
    """
    sql = "select agent_os,agent_arch from agent_info where agent_online_status='0' and agent_storage>='10' " \
          "and agent_migration_os is null;"
    get_info = DBHelper().execute(sql).fetchall()
    get_info_list = []
    for i in get_info:
        get_info_list.append(list(i))
    
    for i in get_info_list :
        if i[0] == 'redhat7':
            i[0] = 'centos7'
        if i[0] == 'redhat8':
            i[0] = 'centos8'

    info_list = []
    info_dict_keys_list = ['agent_os', 'agent_arch']
    for i in get_info_list:
        info_list.append(dict(zip(info_dict_keys_list, i)))

    res = {}
    res['info'] = info_list
    json_res = json.dumps(res)
    return json_res


def get_storage_num(data):
    """
    获取可用空间足够和不足数量
    :param data:
    :return:
    """
    success_num_sql = "select agent_ip from agent_info where agent_online_status='0' and agent_storage>='10' " \
                      "and agent_migration_os is null;"
    get_success_num = DBHelper().execute(success_num_sql).fetchall()

    faild_num_sql = "select agent_ip from agent_info where agent_online_status='0' and agent_storage<'10' " \
                    "and agent_migration_os is null;"
    get_faild_num = DBHelper().execute(faild_num_sql).fetchall()

    success = len(get_success_num)
    faild = len(get_faild_num)
    data = {'success': success, 'faild': faild}
    json_data = json.dumps(data)
    return json_data


reports_type = {
    "migration_detection": reports.migration_detection,
    "migration_logs": reports.migration_logs,
}

def export_reports(data):
    """
    导出各种报告
    :param data:
    :return:
    """
    data = json.loads(data)
    report_type = reports_type.get(data.get('reports_type'))
    if report_type:
        mkdir_log_pwd = "/var/uos-migration/"
        isExists = os.path.exists(mkdir_log_pwd)
        if not isExists:
            try:
                os.makedirs(mkdir_log_pwd)
                migration_log.info(mkdir_log_pwd)
            except:
                migration_log.war("export report mkdir war:%s" % mkdir_log_pwd)

        report_type(data)
    return 'success'


def get_page_data(data):
    """
    定时获取可用空间页面数据
    agent_ip,hostname,agent_online_status,agent_os,agent_storage,agent_arch,task_CreateTime
    :return:
    """
    sql = "select agent_ip,hostname,agent_online_status,agent_os,agent_storage,agent_arch,agent_id from " \
          "agent_info where agent_online_status = 0 and agent_migration_os is null;"
    data = DBHelper().execute(sql).fetchall()
    data = list(data)
    for i in range(0, len(data)):
        data[i] = list(data[i])
        data[i][4] = str(data[i][4]) + 'GB'
        task_CreateTime = "select task_CreateTime from agent_task where agent_ip = '%s';" % data[i][0]
        get_task_CreateTime = DBHelper().execute(task_CreateTime).fetchall()
        get_task_CreateTime = list(get_task_CreateTime)
        if get_task_CreateTime == []:
            data[i] += [""]
        else:
            task_Createtime = get_task_CreateTime[0][0].strftime('%Y-%-m-%d %H:%M:%S')
            data[i].append(task_Createtime)

    res = {}
    res['num'] = len(data)
    info_list = []
    info_dict_keys_list = ['agent_ip', 'hostname', 'agent_online_status', 'agent_os', 'agent_storage',
                           'agent_arch', 'agent_id', 'task_CreateTime']
    for i in data:
        info_list.append(dict(zip(info_dict_keys_list, i)))

    res['info'] = info_list

    json_res = json.dumps(res)
    return json_res


def get_system_migration_data(data):
    """
    获取agent迁移进度
    :return:
    """
    get_migration_pro_sql = "select agent_ip,task_progress,task_status from agent_task;"
    progress = DBHelper().execute(get_migration_pro_sql).fetchall()
    res = {}
    info_list = []
    finall_progress = []
    for i in progress:
        sql = "select agent_id from agent_info where agent_ip='%s' and agent_online_status=0 " \
              "and repo_status=0 and agent_storage>=10;" % i[0]
        get_sql = DBHelper().execute(sql).fetchall()
        if get_sql:
            finall_progress.append(i)

    info_dict_keys_list = ['agent_ip', 'task_progress', 'task_status']
    for i in finall_progress:
        info_list.append(dict(zip(info_dict_keys_list, list(i))))

    res['info'] = info_list
    res['num'] = len(finall_progress)

    json_res = json.dumps(res)
    return json_res


def get_download_center_data(data):
    """
    获取下载中心数据
    :return:
    """
    page = json.loads(data).get('page')
    size = json.loads(data).get('size')
    download_center_data_sql = "select * from report_info;"
    info = DBHelper().execute(download_center_data_sql).fetchall()
    info = list(info)
    res = {}
    res['num'] = len(info)
    info_list = []
    info_dict_keys_list = ['report_generation_time', 'report_name', 'report_type', 'agent_ip',
                           'hostname', 'agent_os', 'agent_arch']
    for i in range(0, len(info)):
        info[i] = list(info[i])
        info[i][0] = info[i][0].strftime('%Y-%-m-%d %H:%M:%S')
        agent_ip = info[i][3]
        agent_info_sql = "select hostname,agent_os,agent_arch from agent_info where agent_ip='%s';" % agent_ip
        agent_info = DBHelper().execute(agent_info_sql).fetchall()
        if not agent_info:
            info[i] += ["", "", ""]
        else:
            agent_info = list(agent_info[0])
            info[i] += agent_info
    for i in info:
        info_list.append(dict(zip(info_dict_keys_list, i)))

    page_list = pagebreak(info_list, page, size)
    res['info'] = page_list
    res['page'] = page
    res['size'] = size

    json_res = json.dumps(res)
    return json_res


def migration_records(data):
    """
    获取迁移成功记录数据
    :return:
    """
    page = json.loads(data).get('page')
    size = json.loads(data).get('size')
    sql = "select agent_ip,hostname,agent_os,agent_migration_os,agent_arch from agent_info " \
          "where agent_migration_os is not null;"
    data = DBHelper().execute(sql).fetchall()
    data = list(data)
    for i in range(0, len(data)):
        data[i] = list(data[i])
        task_update_time_sql = "select task_Updatetime from agent_task where agent_ip='%s'" % data[i][0]
        get_task_update_time = DBHelper().execute(task_update_time_sql).fetchall()
        get_task_update_time = list(get_task_update_time)
        if get_task_update_time == []:
            data[i] += [""]
        else:
            get_task_update_time = get_task_update_time[0][0].strftime('%Y-%-m-%d %H:%M:%S')
            data[i].append(get_task_update_time)

    res = {}
    res['num'] = len(data)
    info_list = []
    info_dict_keys_list = ['agent_ip', 'hostname', 'agent_os', 'agent_migration_os', 'agent_arch', 'create_time']
    for i in data:
        info_list.append(dict(zip(info_dict_keys_list, i)))

    page_list = pagebreak(info_list, page, size)
    res['info'] = page_list
    res['page'] = page
    res['size'] = size

    json_res = json.dumps(res)
    return json_res


def get_migrated_hosts(data):
    """
    获取迁移主机列表数据
    :param data:
    :return:
    """
    page = json.loads(data).get('page')
    size = json.loads(data).get('size')
    sql = "select agent_ip,agent_id,hostname,agent_online_status,agent_os,agent_arch," \
          "agent_history_faild_reason from agent_info where agent_online_status='0' and agent_migration_os is null;"
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

    page_list = pagebreak(info_list, page, size)
    res['info'] = page_list
    res['page'] = page
    res['size'] = size

    json_res = json.dumps(res)
    return json_res


def update_agent_online_status(data):
    """
    修改agent状态
    :param data:
    :return:
    """
    sql = "update agent_info set agent_online_status = 1 where agent_ip = '%s';" % data
    DBHelper().execute(sql)