#!/usr/bin/env python3
# coding=utf-8

#############################     公关投标需求     #############################
#
#需求描述：对用户环境数据进行收集并生成json格式文件保存到指定用户的文件加中，
#供迁移分析，收集信息包括：板卡信息、内核启动参数、内核选项配置参数、
#系统配置参数、环境变量、系统服务、进程、端口、命令接口、系统调用接口、设备驱动接口等。
#
#############################     公关投标需求     #############################


import os
import json
import socket
import datetime

from mig_merge.config import FixedInfo
from mig_merge.stock_replace.system_mark import gen_system_mark
from mig_merge.migrationTools.scanConf import utils
from mig_merge.migrationTools.scanConf.conent_parser import ContentParser
from mig_merge.migrationTools.scanConf.gen_report import gen_conf_data
from mig_merge.migrationTools.utils.config import PathConf

def collecting_system_info():
    """
    收集当前系统上的相关信息
    """

    #检查存储数据目录是否存在，不存在则创建
    if not os.path.exists(FixedInfo.pr_json_path):
        os.makedirs(FixedInfo.pr_json_path)

    if not os.path.exists(FixedInfo.pr_data_path):
        os.makedirs(FixedInfo.pr_data_path)

    #检查配置文件
    current_cfg_file = FixedInfo.pr_cfg_file
    if not os.path.exists(current_cfg_file):
        print("[%s] configure file not exit,please check!!" %(current_cfg_file))
        return '-1'

    #主机名称
    hostname = socket.gethostname()

    with open(current_cfg_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        #存放信息的json文件,供用户迁移参考
        json_file_name = FixedInfo.pr_json_path + '/' +item["confGroupItems"]+'.json'

        conf_group = ""
        parse = False
        for conf in item["confList"]:
            #存放信息的临时文件,兼容性对比使用
            data_file_name = FixedInfo.pr_data_path + '/' +conf["items"]

            #当前时间
            current_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

            status, data, error = utils.run_cmd(conf["path"])
            if status == 0:
                parse = True

            fp = open(data_file_name, 'w')
            for line in data:
                fp.write(line+'\n')
            fp.close()

            conf_group = conf_group + "'"+conf["items"]+"':{'time':'"+current_time+"','hostname':'"+hostname+"','path':'"+conf["path"]+"','parse':True,'result':"+str(data)+"},"
        json.dump(eval('{'+conf_group.rsplit(',', 1)[0]+'}'), open(json_file_name, "w"), indent=4)

    return '0'

if __name__ == "__main__":
    collecting_system_info()
