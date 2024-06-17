#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import json
import platform

from migrationTools.scanRPM.scan_rpm import parsed_pkg_to_json,get_current_pkg_list
from migrationTools.scanRPM.scan_rpm import ParsedPkgInfo

def scan_rpms():
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

    json_str = parsed_pkg_to_json(parsed_pkgs)
    print('json_str = %s' %(json_str))
    current_OS = platform.linux_distribution(
    )[0] + " " + platform.linux_distribution()[1]
    print('current_OS = %s' %(current_OS))

    target_OS = "UnionTech OS Server 20"
    print('target_OS = %s' %(target_OS))
    return json_str

def main():
    scan_rpms()


if __name__ == "__main__":
    main()

