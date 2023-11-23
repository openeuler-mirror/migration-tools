import os
import pandas as pd

from logger import *
from connect_sql import DBHelper


os.chdir('/usr/lib/uos-sysmig-server')
migration_log = Logger('/var/tmp/uos-migration/migration.log', logging.DEBUG, logging.DEBUG)


def migration_detection(data):
    """
    迁移检测报告
    :return:
    """
    agent_ip = data.get('agent_ip')
    info_sql = "select AES_DECRYPT(agent_passwd, 'coco'),agent_username from agent_info where agent_ip='%s'" % agent_ip
    info = DBHelper().execute(info_sql).fetchall()
    scp_log = "sshpass -p %s scp -r %s@%s:/var/tmp/uos-migration/UOS_analysis_report*.tar.gz /var/uos-migration/" % \
              (str(info[0][0], encoding="utf-8"), info[0][1], agent_ip)
    try:
        os.system(scp_log)
        migration_log.info(scp_log)
    except:
        migration_log.error('export report scp error:%s' % scp_log)
    return 'success'


def migration_logs(data):
    """
    迁移日志
    :return:
    """
    agent_ip = data.get('agent_ip')
    info_sql = "select AES_DECRYPT(agent_passwd, 'coco'),agent_username from agent_info where agent_ip='%s'" % agent_ip
    info = DBHelper().execute(info_sql).fetchall()
    scp_log = "sshpass -p %s scp -r %s@%s:/var/tmp/uos-migration/UOS_migration_log*.tar.gz /var/uos-migration/" % \
              (str(info[0][0], encoding="utf-8"), info[0][1], agent_ip)
    try:
        os.system(scp_log)
        migration_log.info(scp_log)
    except:
        migration_log.error('export report scp error:%s' % scp_log)
    return 'success'


def migration_analysis_report(data):
    """
    迁移分析报告
    :return:
    """
    agent_ip = data.get('agent_ip')
    info_sql = "select AES_DECRYPT(agent_passwd, 'coco'),agent_username from agent_info where agent_ip='%s'" % agent_ip
    info = DBHelper().execute(info_sql).fetchall()
    scp_log = "sshpass -p %s scp -r %s@%s:/var/tmp/uos-migration/UOS_migration_completed_report*.tar.gz /var/uos-migration/" % \
              (str(info[0][0], encoding="utf-8"), info[0][1], agent_ip)
    try:
        os.system(scp_log)
        migration_log.info(scp_log)
    except:
        migration_log.error('export report scp error:%s' % scp_log)
    return 'success'


def export_host_info(data):
    """
    主机列表
    :return:
    """
    sql = "select agent_ip,hostname,agent_online_status,agent_os,agent_arch," \
          "agent_history_faild_reason from agent_info;"
    data = DBHelper().execute(sql).fetchall()
    data = list(data)
    for i in range(0, len(data)):
        agent_task = "select task_CreateTime,task_status from agent_task where agent_ip='%s';" % data[i][0]
        get_agent_task = DBHelper().execute(agent_task)
        data[i] = list(data[i])
        get_agent_task = list(get_agent_task)
        if get_agent_task == []:
            data[i] += ["", ""]
        else:
            task_CreateTime = get_agent_task[0][0].strftime('%Y-%-m-%d %H:%M:%S')
            task_status = get_agent_task[0][1]
            data[i].append(task_CreateTime)
            data[i].append(task_status)
    df = pd.DataFrame(data)
    df.columns = ['主机IP', '主机名', '在线状态', '操作系统类型', '架构',  '历史失败原因', '迁移时间', '迁移状态']
    time = datetime.now().strftime('%Y-%-m-%d %H:%M:%S')
    xls = "/var/uos-migration/主机列表_%s.xls" % time
    df.to_excel(xls)
    return 'success'