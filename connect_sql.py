import pymysql
import json
import os
#os.chdir('/usr/lib/uos-sysmig-server')
from logger import *
from miscellaneous import getSysMigConf


migration_log = Logger('/var/tmp/uos-migration/migration.log', logging.DEBUG, logging.DEBUG)
uos_sysmig_conf = json.loads(getSysMigConf('0.0.0.0'))
db_host = json.loads(uos_sysmig_conf).get('serverip').strip()[1:-1]
db_name = json.loads(uos_sysmig_conf).get('db_name').strip()[1:-1]
db_password = json.loads(uos_sysmig_conf).get('db_password').strip()[1:-1]
db_user = json.loads(uos_sysmig_conf).get('db_user').strip()[1:-1]


class DBHelper:
    # 构造函数
    def __init__(self, host=db_host, user=db_user, pwd=db_password, db=db_name):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.connect = None
        self.cursor = None

    # 连接数据库
    def connectDatabase(self):
        try:
            self.connect = pymysql.connect(host=self.host, user=self.user, password=self.pwd, db=self.db,
                                           charset='utf8')
        except:
            migration_log.error('connectDatabase failed')
            return False
        self.cursor = self.connect.cursor()
        return True

    # 关闭数据库
    def close(self):
        # 如果数据打开，则关闭；否则没有操作
        if self.connect and self.cursor:
            self.cursor.close()
            self.connect.close()
        return True

    def execute(self, sql):
        """
        传入查询 修改 删除sql语句
        :param sql:
        :return:self.cursor
        """
        self.connectDatabase()
        # 处理显示的数据
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            migration_log.error('%s执行失败：%s' % (sql, e))
        else:
            self.close()
            migration_log.info('%s 执行成功' % sql)
            data = self.cursor
            return data

    def insert(self, sql, val):
        """
        传入sql语句
        :param sql:
        :return:self.cursor
        如果想获取查询数据需要fetchall()
        """
        self.connectDatabase()
        # 处理显示的数据
        try:
            self.cursor.executemany(sql, val)
            self.connect.commit()
        except Exception as e:
            migration_log.error('%s执行失败：%s' % (sql, e))
        else:
            self.close()
            migration_log.info('%s 执行成功' % sql)
            data = self.cursor
            return data
