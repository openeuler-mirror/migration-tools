import json
from datetime import datetime

from connect_sql import DBHelper
from sysmig_agent.share import getSysMigConf

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
    # TODO: 用户权限检测
    
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