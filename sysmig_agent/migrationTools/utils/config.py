#!/bin/python3

import datetime
import os
import platform
import sys


class PathConf():
    ## 时间戳用于文件名区分
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    arch = platform.machine()
    ## ../../ 目录是项目目录
    __base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(__base_path, 'data')

    __curdir = os.path.dirname(os.path.realpath(sys.argv[0]))
    output_path = os.path.join(__curdir, 'utmtc-output')

    new_conf_dir = os.path.join(data_path, "system-config/uos-1020e", arch)
    ## public
    log_dir = os.path.join(output_path, "log")
    log_file = os.path.join(log_dir, f"{timestamp}.log")
    run_dir = os.path.join(output_path, "run", timestamp)
    report_dir = os.path.join(output_path, "report")
    report_template_file = os.path.join(data_path, "report-template",
                                        "index.html")
