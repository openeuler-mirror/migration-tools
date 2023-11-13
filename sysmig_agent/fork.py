# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier:   MulanPubL-2.0-or-later

import platform
import threading
from multiprocessing import Process, Queue
from apscheduler.schedulers.background import BackgroundScheduler
import time
import os
import sys
from sysmig_agent.abi_weight import *
from sysmig_agent.Abisystmcompchk import migrate_before_abi_chk, migrate_behind_abi_chk
import socket
#from share import *
from sysmig_agent.short_task import *

from sysmig_agent.migration import *
#sys.path.append("..")
#from connect_sql import DBHelper
from sysmig_agent.agent_request import post_server

# create message query
q = Queue(maxsize=0)


# 定时任务
def up_to_date_sql_abi():
    # 获得sql的任务ID
    # ret_task = get_sql_message()
    # print('Get message query : ' + str(ret_task[0]))
    # 获得ABI消息队列信息tuple
    ret_abi_info = get_abi_info()
    if ret_abi_info:
        abi_process = ret_abi_info[0]
        abi_task = ret_abi_info[1]
    else:
        return 1
    # 获取abi progress 更新数据库内
    sql_abi_progress(abi_process)
    return 0


# ABI系统检测
def timed_task_abi(task_id):
    time_task = BackgroundScheduler(timezone='Asia/Shanghai')
    task_id=str(task_id)
    p = time_task.add_job(up_to_date_sql_abi, 'interval', seconds=3)
    time_task.start()
    try:
        task_statue='1'
        p_abi = Process(target=migrate_before_abi_chk, args=(q,task_statue,))
        p_abi.start()
        p_abi.join()
        # Determine whether the message queue is dead or empty to end the timer
        while not q.empty():
            continue
        time_task.shutdown()
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        time_task.shutdown()
        print('Exit The Job!')


# 系统迁移 定时任务更新进度
def timed_task_migrate(task_id, kernel_version):
    time_task_m = BackgroundScheduler(timezone='Asia/Shanghai')
    p = time_task_m.add_job(up_to_date_sql_migrate, 'interval', seconds=3)
    migInit_porgress()
    time_task_m.start()
    try:
        while 8 > int(str(get_mig_state(task_id))[1]):
            state = str(get_mig_state(task_id))[1]
            if str(get_mig_state(task_id))[0] == '1':
                ##
                ## error , too many request systen migration
                time_task_m.shutdown()
                return 'error'
            old_os_name = get_old_osname()
            if '0' == state:
                sql_mig_statue('10')
                if ifnot_mig_kernel(kernel_version):
                    sql_mig_statue('18')
                t = Process(target=centos8_main, args=(old_os_name, task_id,))
                t.start()
                t.join()
            elif '2' == state:
                sql_mig_statue('12')
                ## skip broken
                skip = 0
                t = Process(target=mig_distro_sync, args=(skip, task_id,))
                t.start()
                t.join()
            elif '3' == state:
                # Breakpoint
                sql_mig_statue('05')
            elif '4' == state:
                sql_mig_statue('14')
                mig_kernel(kernel_version)
                main_conf(old_os_name)
                # Migration report
                try:
                    migrate_behind_abi_chk()
                except:
                    # Generate analysis report error
                    pass
                sql_mig_statue('05')
            elif '5' == state:
                sql_mig_statue('15')
                # Migration state weight : 90
                res = mig_whether_success()

                # new system regen sql
                get_new_osversion()
                # tar.gz type
                targz_mig_dir_log()
                targz_mig_dir_report()
                sql_abi_progress(100)
                if 80 > int(res):
                    sql_task_statue('3', task_id)
                    sql_mig_statue('08')
                    return 1
                    # data = ' 迁移失败。'
                else:
                    sql_task_statue('2', task_id)
                    sql_mig_statue('09')
                    time_task_m.shutdown()
                    return 0
                    # data = '迁移成功。'
            time.sleep(3)  # 其他任务是独立的线程执行
        time_task_m.shutdown()
        return 0
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        time_task_m.shutdown()
        sql_task_statue('3', task_id)

