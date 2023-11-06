import pymysql

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
            print('connectDatabase failed')
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
