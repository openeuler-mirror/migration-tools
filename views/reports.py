import os
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