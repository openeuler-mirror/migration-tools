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
