#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import json
import platform

from logger import migration_log
from mig_merge.migrationTools.scanRPM.scan_rpm import parsed_pkg_to_json,get_current_pkg_list
from mig_merge.migrationTools.scanRPM.scan_rpm import ParsedPkgInfo

def rpmscan_tabs():
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

    for pkg_name in installed_pkgs:
        tmp_pkg_info = ParsedPkgInfo(pkg_name, add_tags)
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
    json_str = target_OS + '"data": ' + parsed_pkg_to_json(parsed_pkgs) + '}'

    return json_str

def main():
    rpmscan_tabs()


if __name__ == "__main__":
    main()

