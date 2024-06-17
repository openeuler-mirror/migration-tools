#!/usr/bin/python3
# -*- coding: utf-8 -*-

# coding=utf-8

import json
import os

from mig_merge.migrationTools.scanConf import utils
from mig_merge.migrationTools.scanConf.conent_parser import ContentParser

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

def ScanConf():
    """
    收集当前系统上的信息配置信息
    """
    data = get_sysctl_a_data()
    print('data-01 = %s' %(data))

    data = get_system_service_data()
    print('data-02 = %s' %(data))

if __name__ == "__main__":
    scan_conf = ScanConf()

