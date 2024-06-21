# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier:   MulanPubL-2.0-or-later
import threading
from multiprocessing import Process, Queue
from sysmig_agent.utils import DBwrite, selfDestruct
from apscheduler.schedulers.background import BackgroundScheduler
import time
from sysmig_agent.Abisystmcompchk import migrate_before_abi_chk
from mig_merge.stock_analysis import stock_replace_analysis
from mig_merge.stock_replace.confirm import migration_confirm
from sysmig_agent.short_task import *
from sysmig_agent.migration import *
from sysmig_agent.agent_request import post_server

q = Queue(maxsize=0)


# 定时任务
def up_to_date_sql_abi():
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
    task_id = str(task_id)
    p = time_task.add_job(up_to_date_sql_abi, 'interval', seconds=3)
    time_task.start()
    try:
        task_statue = '1'
        # 新增mig_type参数，mig_type为'A'存量替换迁移检查；mig_type为'E'新增扩容。
        p_abi = Process(target=migrate_before_abi_chk, args=(q, task_statue, 'A'))
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
            old_os = get_old_osnameversion()
            if '0' == state:
                sql_mig_statue('10')
                if ifnot_mig_kernel(kernel_version):
                    sql_mig_statue('18')
                t = Process(target=centos8_main, args=(old_os, task_id,))
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
                    stock_replace_analysis()
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
                time_task_m.shutdown()
                sql_abi_progress(100)
                if 80 > int(res):
                    sql_task_statue('3', task_id)
                    sql_mig_statue('08')
                    return 1
                    # data = ' 迁移失败。'
                else:
                    sql_task_statue('2', task_id)
                    sql_mig_statue('09')
                    selfDestruct(task_id)
                    return 0
                    # data = '迁移成功。'
            time.sleep(3)  # 其他任务是独立的线程执行
        return 0
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        time_task_m.shutdown()
        sql_task_statue('3', task_id)


def get_abi_info():
    if q.empty():
        return None
    #    print("Full :", q.full())
    #    print("Empty :", q.empty())
    #    print("QSize:", q.qsize())
    size = int(q.qsize())
    i = 0
    msg = ''
    while i < size:
        i += 1
        msg = q.get()
    return msg


def process_time_task_abi(task_id):
    # 定时任务启动并更新进度
    timed_task_abi(task_id)
    # 系统兼容性检测的html存入数据库
    db_write = DBwrite(get_local_ip())
    db_write.write_analysis_html()
    # abi结果接入数据库内
    # abi_file_sql(abi_file)
    # p_timed_task = Process(target=timed_task_abi, args=(task_id,))
    # p_timed_task.start()
    # p_timed_task.join()


# ABI对比结果文件，存放数据库内
def abi_file_sql(path):
    with open(path, 'r') as p:
        ret = p.readlines()
        p.close()
    for i in range(len(ret)):
        info = ret[i].split(',', 5)
        info_str = ''
        for n in range(len(info)):
            if n < 9:
                sinfo = ''
                if info[n].strip().strip('\n'):
                    sinfo = info[n].strip().strip('\n')
                    info_str = info_str + "'{}'".format(sinfo)
                else:
                    sinfo = 'NULL'
                    info_str = info_str + "{}".format(sinfo)
            if n != (len(info) - 1):
                info_str = info_str + ','
        abi_file_connect(info_str)


def check_environment(data):
    """
    存量替换 系统兼容性检测
    Args:
        data:
        json 数据传入
    Returns:

    """
    task_id = json.loads(data).get('task_id')
    # 更新SQL任务状态
    sql_task_statue('1', task_id)
    # 发送消息给Server更新任务流状态
    post_server('task_start', task_id)
    process_time_task_abi(task_id)
    # tar.gz types abi report
    # targz_mig_dir_abi()
    # 系统兼容性检测的html存入数据库
    db_write = DBwrite(get_local_ip())
    db_write.write_analysis_html()
    sql_task_statue('2', task_id)
    post_server('task_close', task_id)


def process_time_task_abi_e(task_id):
    # 定时任务启动并更新进度
    # TODO:
    time_task = BackgroundScheduler(timezone='Asia/Shanghai')
    task_id = str(task_id)
    p = time_task.add_job(up_to_date_sql_abi, 'interval', seconds=3)
    time_task.start()
    try:
        task_statue = '1'
        # 新增mig_type参数，mig_type为'A'存量替换迁移检查；mig_type为'E'新增扩容。
        p_abi = Process(target=migrate_before_abi_chk, args=(q, task_statue, 'E'))
        p_abi.start()
        p_abi.join()
        # Determine whether the message queue is dead or empty to end the timer
        while not q.empty():
            continue
        time_task.shutdown()
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        time_task.shutdown()
        migration_log('Exit The Job!')


def check_add_environment(data):
    """
    新增扩容 兼容性检测
    Args:
        data:
    Returns:

    """
    task_id = json.loads(data).get('task_id')
    # 更新SQL任务状态
    sql_task_statue('1', task_id)
    # 发送消息给Server更新任务流状态
    post_server('task_start', task_id)
    process_time_task_abi_e(task_id)
    # tar.gz types abi report
    # targz_mig_dir_abi()
    # 系统兼容性检测的html存入数据库
    db_write = DBwrite(get_local_ip())
    db_write.write_analysis_add_html()
    sql_task_statue('2', task_id)
    post_server('task_close', task_id)


# 初始化进度阶段
def mig_modify_statue(task_id):
    if not get_mig_state(task_id):
        sql_mig_statue('00')
        '''
    else:
        # Too many migration requests
        # If you need to continue the migration, please change the task_data of the Mysql
        return 1
        ret = get_mig_state(task_id)
        ret = re.sub('[0-9]', '0', ret[0]) + ret[1]
        sql_mig_statue(ret)
    # loggea
    '''


def get_info_version(data):
    info = json.loads(data).get('info')
    for i in range(len(info)):
        agent_info = json.dumps(info[i])
        ip = json.loads(agent_info).get('agent_ip')
        agent_ip = get_local_ip()
        if ip == agent_ip:
            version = json.loads(agent_info).get('kernel_version')
            return version


def system_migration(data):
    kernel_version = get_info_version(data)
    if not kernel_version:
        kernel_version = '0'
    task_id = json.loads(data).get('task_id')
    # 更新SQL任务状态
    sql_task_statue('1', task_id)
    # 发送消息给Server更新任务流状态
    post_server('task_start', task_id)
    # The migration status is modified, and the breakpoint continues
    mig_modify_statue(task_id)
    # sql_mig_statue('00')
    # 迁移分析确认
    migration_confirm()
    # MIGRATION MAIN
    timed_task_migrate(task_id, kernel_version)
    post_server('task_close', task_id)


def if_env_check(data):
    agent_ips = list(json.loads(data).get('agent_ip'))
    for n in range(len(agent_ips)):
        ip = str(agent_ips[n])
        if ip == get_local_ip():
            return True
    return False


def post_task(data):
    task_mod = json.loads(data).get('mod')
    if not if_env_check(data):
        return 'success'
    if 'check_info' == task_mod:
        t = threading.Thread(target=check_info, args=[data])
    elif 'check_repo' == task_mod:
        t = threading.Thread(target=check_repo, args=[data])
    elif 'check_add_repo' == task_mod:
        add_repo = RepoFileAdd(data)
        t = threading.Thread(target=add_repo.run)
    elif 'check_kernel' == task_mod:
        t = threading.Thread(target=check_kernel, args=[data])
    elif 'check_environment' == task_mod:
        t = threading.Thread(target=check_environment, args=[data])
    elif 'check_add_environment' == task_mod:
        t = threading.Thread(target=check_add_environment, args=[data])
    elif 'system_migration' == task_mod:
        t = threading.Thread(target=system_migration, args=[data])
    t.start()
    return 'y'

# ABI 权重比
# abi_check_priority()
