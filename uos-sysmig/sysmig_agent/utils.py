# -*- coding: utf-8 -*-
import os
import pymysql
from connect_sql import DBHelper
from logger import migration_log
from sysmig_agent.migration import get_mig_state
from sysmig_agent.share import run_subprocess, get_local_ip


class DBupload(object):
    """
    Put reports into database based on folder contents.
    """
    types = {'UOS_analysis_report_add': '迁移检测报告-新增扩容', 'UOS_analysis_report': '迁移检测报告-存量替换',
             'UOS_migration_completed_report': '迁移分析报告', 'UOS_migration_log': '日志'}

    def __init__(self, htmlpath):
        super().__init__()
        self.html_path = htmlpath

    def read_html(self):
        if not os.path.exists(self.html_path):
            migration_log.error('Please check you report')
            return False
        with open(self.html_path, 'r') as ht:
            html = pymysql.escape_string(ht.read())
            ht.close()
        return html

    def upload_html(self):
        html = self.read_html()
        if not html:
            migration_log.error('Please check you report')
            return False
        # report_type = self.html_path.split('.', -1)[len(self.html_path.split('.', -1)) - 1]
        if not os.path.exists(self.html_path):
            migration_log.error('Can not found report..')
            return False
        if not self.types[os.path.basename(os.path.dirname(self.html_path))]:
            migration_log.error('Can not found report..')
        sql = "INSERT INTO report_info  ( agent_ip , report_type , report_name ,create_time, report_content) VALUES(" \
              "'{}','{}','{}',NOW(),'{}');".format(get_local_ip(),
                                                   self.types[os.path.basename(os.path.dirname(self.html_path))],
                                                   os.path.basename(self.html_path), html)
        try:
            ret = DBHelper().execute(sql)
        except:
            pass


class DBwrite(DBHelper):
    """
    Export the Html file of MySql to /var/uos-migration.
    """

    def __init__(self, getip, path='/var/uos-migration/'):
        super().__init__()
        self.getip = getip
        self.path = path.strip('\n') + getip.strip('\n') + '/'

    def write_file(self, sql):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        try:
            ret = self.execute(sql).fetchall()
            if len(ret) < 1:
                migration_log.error('MySql does not store html report.')
                return 1
            for i in range(len(ret)):
                filename = self.path.strip('\n') + ret[i][0]
                print(filename)
                content = str(ret[i][1])
                if os.path.exists(filename):
                    filename = filename.strip('\n') + '.new'
                with open(filename, 'w+') as f:
                    f.write(content)
                    f.close()
            return True
        except Exception as e:
            migration_log.error(e)
            return False

    def write_analysis_html(self):
        sql = "SELECT report_name,report_content FROM report_info WHERE agent_ip='{}' and report_type LIKE " \
              "'%存量替换%';".format(self.getip)
        self.write_file(sql)

    def write_analysis_add_html(self):
        sql = "SELECT report_name,report_content FROM report_info WHERE agent_ip='{}' and report_type LIKE " \
              "'%新增扩容%';".format(self.getip)
        self.write_file(sql)

    def write_completed_html(self):
        sql = "SELECT report_name,report_content FROM report_info WHERE agent_ip='{}' and report_type LIKE " \
              "'%迁移分析%';".format(self.getip)
        self.write_file(sql)

    def write_completed_log(self):
        sql = "SELECT report_name,report_content FROM report_info WHERE agent_ip='{}' and report_type LIKE " \
              "'%日志%';".format(self.getip)
        self.write_file(sql)


def selfDestruct(task_id):
    """
    destroy agent system migration rpm.
    Args:
        task_id:

    Returns:

    """
    if '9' == int(str(get_mig_state(task_id))[1]):
        cmd = 'yum remove -y uos-sysmig-agent uos-sysmig-data'
        _, code = run_subprocess(cmd)
        if code != 0:
            migration_log.error("Migration is complete，Agent[{}]:Uninstall failed".format(get_local_ip()))
        else:
            migration_log.info("Migration is complete，Agent[{}]:Uninstall has been successful".format(get_local_ip()))
    migration_log.info("migration statues is not satisfied，Agent[{}]:It is not uninstalled for the time being. Please "
                       "check the task_info.task-data table and uninstall it after the migration is "
                       "successful.".format(get_local_ip()))
