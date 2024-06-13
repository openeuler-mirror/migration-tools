# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier:   MulanPubL-2.0-or-later
import pymysql,os
from connect_sql import DBHelper
from logger import migration_log
from sysmig_agent.migration import get_mig_state
from sysmig_agent.share import run_subprocess, get_local_ip


class DBupload(object):
    """
    Put reports into database based on folder contents.
    """

    def __init__(self, htmlpath):
        super().__init__()
        self.html_path = htmlpath

    def read_html(self):
        if not os.path.exists(self.html_path):
            migration_log.error('Please check you report')
            return False
        with open(self.html_path, 'r') as ht:
            print(self.html_path)
            html = pymysql.escape_string(ht.read())
            ht.close()
        return html

    def upload_html(self):
        html = self.read_html()
        if not html:
            return False
        report_type = self.html_path.split('.', -1)[len(self.html_path.split('.', -1)) - 1]
        sql = "INSERT INTO report_info  ( agent_ip , report_type , report_name ,create_time, report_contect) VALUES(" \
              "'{}','{}','{}',NOW(),'{}');".format(get_local_ip(), report_type, os.path.basename(self.html_path), html)
        try:
            ret = DBHelper().execute(sql)
        except:
            pass


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
