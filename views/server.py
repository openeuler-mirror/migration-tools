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