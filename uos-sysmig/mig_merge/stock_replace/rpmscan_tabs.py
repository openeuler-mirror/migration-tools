#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import json
import platform

from mig_merge.migrationTools.scanRPM.scan_rpm import parsed_pkg_to_json,get_current_pkg_list
from mig_merge.migrationTools.scanRPM.scan_rpm import ParsedPkgInfoAdd
from mig_merge.repo_sqlite.gen_sqlite import gen_sqlite

def rpmscan_tabs(mig_flag, logger):
    exclude_fonts = True
    add_tags = True

    parsed_pkgs = []
    installed_pkgs = get_current_pkg_list()

    if exclude_fonts:
        filted_installed_pkgs = []
        for pkg in installed_pkgs:
            if 'fonts' in pkg:
                continue
            filted_installed_pkgs.append(pkg)
        installed_pkgs = filted_installed_pkgs

    exclude_kernel_modules = True
    if exclude_kernel_modules:
        filted_installed_pkgs = []
        for pkg in installed_pkgs:
            if 'kernel-modules' in pkg:
                continue
            filted_installed_pkgs.append(pkg)
        installed_pkgs = filted_installed_pkgs

    sqlite_list = gen_sqlite(logger, mig_flag)
    if sqlite_list == '-1':
        return '-1'

    for pkg_name in installed_pkgs:
        #多个sqlite查询，存在多个重复查询结果
        #需要对插叙结果格式化，只输出唯一结果
        #eg: gssproxy-0.8.0-15.el8.x86_64 在111.sqlite查询结果为空；在222.sqlite查询结果也为空，报告有两条结果
        i = 0
        tmp_pkg_info_list = []
        other_provided_list = []
        nothind_provided_list = []

        for sqlite in sqlite_list:
            tmp_pkg_info = ParsedPkgInfoAdd(pkg_name, sqlite, add_tags)
            tmp_pkg_info_list.append(tmp_pkg_info)
            tmp_info = str(tmp_pkg_info.tags)
            if 'Nothing provided' in tmp_info:
                nothind_provided_list.append(tmp_info+'|'+str(i))
            else:
                other_provided_list.append(tmp_info+'|'+str(i))
            i += 1
        #此时单个包对sqlite列表遍历结束，开始格式化输出结果
        if len(sqlite_list) == len(nothind_provided_list):
            #单个包对sqlite遍历，所有结果都为 'Nothing provided' 格式化输[0]
            parsed_pkgs.append(tmp_pkg_info_list[0])
        else:
            #单个包对sqlite遍历，所有结果非 'Nothing provided' 格式化输出[0]
            ele_num = other_provided_list[0].split('|')[1]
            parsed_pkgs.append(tmp_pkg_info_list[int(ele_num)])

    only_show_leap = True
    if only_show_leap:
        filted_pkgs = []
        for pkg in parsed_pkgs:
            if pkg.is_version_leaped:
                filted_pkgs.append(pkg)
        parsed_pkgs = filted_pkgs

    current_OS = '"rpmscan_tabs": {"current_os": ' + '"'+ platform.linux_distribution(
    )[0] + " " + platform.linux_distribution()[1] + '"'

    target_OS = current_OS + ',"target_os": "UnionTech OS Server 20",'
    rpmscan_tabs_json = target_OS + '"data": ' + parsed_pkg_to_json(parsed_pkgs) + '}'
    #logger.info('Get rpmscan tabs json data:' .format(rpmscan_tabs_json))

    return rpmscan_tabs_json

def main():
    rpmscan_tabs()


if __name__ == "__main__":
    main()

