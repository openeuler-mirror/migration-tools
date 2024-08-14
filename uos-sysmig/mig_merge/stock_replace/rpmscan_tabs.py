#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import json
import platform

from mig_merge.migrationTools.scanRPM.scan_rpm import parsed_pkg_to_json,get_current_pkg_list
from mig_merge.migrationTools.scanRPM.scan_rpm import ParsedPkgInfoAdd
from mig_merge.merge.gen_sqlite import gen_sqlite

def rpmscan_tabs(logger):
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

    sqlite_list = gen_sqlite(logger)
    if sqlite_list == '-1':
        return '-1'

    for pkg_name in installed_pkgs:
        for sqlite in sqlite_list:
            tmp_pkg_info = ParsedPkgInfoAdd(pkg_name, sqlite, add_tags)
            parsed_pkgs.append(tmp_pkg_info)

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

