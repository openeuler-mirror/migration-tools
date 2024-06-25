import time
from connect_sql import *


def check_heartbeat(q):
    """
    定时获取队列
    :return:
    """
    while True:
        agent_ip_list = []
        print('qsize:' + str(q.qsize()))
        if q.empty():
            pass
        else:
            for i in range(q.qsize()):
                agent_ip_list.append(q.get())
            print('check_heartbeat:' + str(agent_ip_list))
        db_agent_ip = get_db_agent_ip()
        if agent_ip_list != []:
            for i in list(set(agent_ip_list)):
                if i in db_agent_ip:
                    sql = "update agent_info set agent_online_status=0 where agent_ip='%s'" % i
                    db_agent_ip.remove(i)
                    DBHelper().execute(sql)
        if db_agent_ip != []:
            for i in db_agent_ip:
                sql = "update agent_info set agent_online_status=1 where agent_ip='%s'" % i
                DBHelper().execute(sql)
        time.sleep(120)


def get_db_agent_ip():
    sql = "select agent_ip from agent_info;"
    agent_ip_list = []
    try:
        get_sql = DBHelper().execute(sql).fetchall()
    except:
        return agent_ip_list
    for i in get_sql:
        agent_ip_list.append(i[0])
    return agent_ip_list
