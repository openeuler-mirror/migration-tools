#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import os

import migrationTools.utils.html as html
from migrationTools.scanHardware import utils
from migrationTools.utils.config import PathConf
from migrationTools.utils.logger import Logger

logger = Logger(__name__)


def generate_comtatibility_list_js():
    report_dir = PathConf.report_dir

    report_name = f"hardware_info_report_{PathConf.timestamp}"

    html.copy_html_resource()
    datafiledir = os.path.join(report_dir, "datafile")
    if not os.path.exists(datafiledir):
        os.makedirs(datafiledir)

    # js
    jsfile_path = os.path.join(report_dir, 'datafile', f"{report_name}.js")
    # 对应的入口 html
    html_path = os.path.join(report_dir, f"{report_name}.html")

    html_document = html.gen_html_template(report_name)

    compatability_js_file = open(jsfile_path, 'w')
    compatability_html_file = open(html_path, 'w')

    compatability_list = utils.get_compatability_list(
        utils.get_pci_list(), utils.get_supported_device_list(), False)
    jsonstr = json.dumps(compatability_list)

    with compatability_js_file:
        compatability_js_file.write(
            'utmt_report_mode="scanhardware";\nutmt_report_data=`' + jsonstr +
            '`')

    with compatability_html_file:
        compatability_html_file.write(html_document)
        logger.info(f"report has been generated: {html_path}.")


def main():
    generate_comtatibility_list_js()


if __name__ == "__main__":
    main()
