#!/usr/bin/env python3
# coding=utf-8

import json
import os

from sysmig_agent.migrationTools.scanConf import utils
from sysmig_agent.migrationTools.scanConf.conent_parser import ContentParser
from sysmig_agent.migrationTools.scanConf.gen_report import gen_compat_report
from sysmig_agent.migrationTools.utils.config import PathConf
from sysmig_agent.migrationTools.utils.logger import Logger

logger = Logger(__name__)


class ScanConf:
    """
    收集当前系统上的信息配置信息
    """
    def __init__(self) -> None:
        self.conf_dir = PathConf.run_dir
        self.new_conf_dir = PathConf.new_conf_dir

    def run(self, args):
        self.get_all_data()
        self.gen_report = gen_compat_report
        self.gen_report(self.conf_dir, self.new_conf_dir)

    def get_all_data(self):
        data = self.get_sysctl_a_data()
        self.write_data_json(data, "sysctl_a")

        data = self.get_system_service_data()
        self.write_data_json(data, 'systemctl_a')

    def get_sysctl_a_data(self):
        cmd = "sysctl -a"
        _, data, _ = utils.run_cmd(cmd)
        data = utils.get_valid_lines(data)

        data = ContentParser.parse_sysctl_content(data)
        return data

    def get_system_service_data(self):
        cmd = "systemctl -a"
        _, data, _ = utils.run_cmd(cmd)
        data = utils.get_valid_lines(data)
        data = utils.systemd_escape_lines(data)
        data = ContentParser.parse_system_service_content(data)

        return data

    def write_data_json(self, data, name):
        """
        write data to the file.
        """
        data_dir = self.conf_dir
        os.makedirs(data_dir, exist_ok=True)
        data_path = os.path.join(data_dir, name) + '.json'
        if os.path.exists(data_path):
            os.remove(data_path)
        with open(data_path, 'w', encoding='utf-8') as file:
            data_content = json.dumps(data)
            file.write(data_content)


if __name__ == "__main__":
    scan_conf = ScanConf()
