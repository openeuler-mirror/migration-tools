#!/usr/bin/python3
# -*- coding: utf-8 -*-

from sqlite3.dbapi2 import Cursor
import sys
import sqlite3

class DBOperate(object):
    ''' 操作sqlite数据库，sql语句执行失败，自动回滚

    example:
        with DBOperate("./centos7-primary.sqlite") as db:
            db.execute_sql("select * from conflicts")
            print(db.cursor.fetchall())
    '''
    
    # new 是负责实例化的静态方法，会被最先调用并返回该实例，是静态方法
    # __init__ 在类的实例返回后（也就是 new 执行完之后）被调用，进行各种类本身相关的初始化，是实例方法
    # new 的返回值（实例）将被作为 init 的第一个参数传给对象的 init
    # cls 代表当前类
    # 一顿操作猛如虎，又是 new、又是 enter、exit 的，是为了可以像打开文件一样，用 with 操作 sql
    def __new__(cls = None, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(DBOperate, cls).__new__(cls)
        return cls._instance

    
    def __init__(self, db_name):
        self.db_name = db_name
        self.connect = sqlite3.connect(self.db_name)
        self.cursor = self.connect.cursor()

    
    def __enter__(self):
        return self

    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connect.close()

    def select(self, sql):
        return self.cursor.execute(sql)
    
    def execute_sql(self, sql):
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception:
            self.connect.rollback()

    
    def executemany_sql(self, sql, data_list):
        ''' 使用 executemany 进行批量操作，（据说）在万条插入时，相比一条条执行的速度会有上百倍的提升
        Example:
        sql = 'insert into filelist (pkgKey, dirname, filenames, filetypes) values (?, ?, ?, ?);'
        data_list = [(1, '...', '...', 'f'), (2, '...', '...', 'd')]
        '''
        try:
            self.cursor.executemany(sql, data_list)
            self.connect.commit()
        except Exception:
            self.connect.rollback()
            print('error: executemany failed')
            sys.exit(1)
