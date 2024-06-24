#!/usr/bin/env python3
# coding=utf-8

import json
import os

from mig_merge.config import FixedInfo
from mig_merge.stock_replace.system_mark import gen_system_mark
from mig_merge.migrationTools.scanConf import utils
from mig_merge.migrationTools.scanConf.conent_parser import ContentParser
from mig_merge.migrationTools.scanConf.gen_report import gen_conf_data
from mig_merge.migrationTools.utils.config import PathConf


def get_all_data():
    data = get_sysctl_a_data()
    write_data_json(data, "sysctl_a")

    data = get_system_service_data()
    write_data_json(data, 'systemctl_a')

def get_sysctl_a_data():
    cmd = "sysctl -a"
    _, data, _ = utils.run_cmd(cmd)
    data = utils.get_valid_lines(data)

    data = ContentParser.parse_sysctl_content(data)
    return data

def get_system_service_data():
    cmd = "systemctl -a"
    _, data, _ = utils.run_cmd(cmd)
    data = utils.get_valid_lines(data)
    data = utils.systemd_escape_lines(data)
    data = ContentParser.parse_system_service_content(data)

    return data

def write_data_json(data, name):
    """
    write data to the file.
    """
    data_dir = PathConf.run_dir
    os.makedirs(data_dir, exist_ok=True)
    data_path = os.path.join(data_dir, name) + '.json'
    if os.path.exists(data_path):
        os.remove(data_path)
    with open(data_path, 'w', encoding='utf-8') as file:
        data_content = json.dumps(data)
        file.write(data_content)

def confscan_tabs(logger):
    """
    收集当前系统上的信息配置信息
    """

    conf_dir = PathConf.run_dir
    repo_mark = gen_system_mark()
    logger.info('Repo source of mark:{}'.format(repo_mark))
    new_conf_dir = FixedInfo.system_data_path+'/system-config/'+repo_mark+'/x86_64'

    get_all_data()
    gen_report = gen_conf_data
    confscan_tabs_json = '"confscan_tabs": ' + gen_report(conf_dir, new_conf_dir) + ','

    return confscan_tabs_json

if __name__ == "__main__":
    scan_conf = confscan_tabs()
