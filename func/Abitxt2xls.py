# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier:   MulanPubL-2.0-or-later
# coding=utf-8
import datetime
import json
import socket
import xlwt
from func.share import *
from settings import (report_path_bef, report_path_ago, txtFileName, txtFileName1, SysInfoFile, SysInfoFile_after,
                      PkgCompFile1, PkgCompFile2, PkgCompFile3, PkgCompFile4, PkgCompFile1_after)


def get_host_ip():
    """
    查询本机ip地址
    :return:
    """
    uos_sysmig_conf = json.loads(get_sysmig_conf())
    ip = json.loads(uos_sysmig_conf).get('agentip').strip()[1:-1]
    return ip


def accord_line_write(txt_line_file, sheet_line, line_num, column_num):
    with open(txt_line_file, 'r') as line_f:
        x = line_num 
        y = column_num
        sys_lines = line_f.readlines()
        for line in sys_lines:
            for value in line.strip().split("|"):
                sheet_line.write(x, y, value)
                y += 1
            x += 1
            y = 0
    line_f.close()


def accord_column_write(txt_column_file, sheet_column, line_num, column_num):
    with open(txt_column_file, 'r') as column_f:
        x = line_num 
        y = column_num
        sys_columns = column_f.readlines()
        for line in sys_columns:
            for value in line.strip().split("|"):
                sheet_column.write(x, y, value)
                x += 1
    column_f.close()


def system_info(check_file):
    sheet_sysinfo = check_file.add_sheet("系统基本信息")
    accord_line_write(SysInfoFile, sheet_sysinfo, 0, 0)


def system_info_after(sys):
    sheet_sysinfo = sys.add_sheet("系统基本信息")
    accord_line_write(SysInfoFile_after, sheet_sysinfo, 0, 0)


def pkg_comp(pkg):
    sheet_pkgcomp = pkg.add_sheet("软件包对比")
    accord_line_write(PkgCompFile1, sheet_pkgcomp, 0, 0)
    accord_column_write(PkgCompFile2, sheet_pkgcomp, 3, 0)
    accord_column_write(PkgCompFile4, sheet_pkgcomp, 3, 1)


def pkg_comp_after(pkg):
    sheet_pkgcomp = pkg.add_sheet("软件包对比")
    accord_line_write(PkgCompFile1_after, sheet_pkgcomp, 0, 0)
    accord_column_write(PkgCompFile2, sheet_pkgcomp, 3, 0)
    accord_column_write(PkgCompFile3, sheet_pkgcomp, 3, 1)
    accord_column_write(PkgCompFile4, sheet_pkgcomp, 3, 2)


def abi_incomp_info(file_incomp):
    sheet_comp = file_incomp.add_sheet("ABI兼容")
    accord_line_write(txtFileName, sheet_comp, 0, 0)


def abi_comp_pkg(file_comp):
    sheet_incomp = file_comp.add_sheet("ABI不兼容")
    accord_line_write(txtFileName1, sheet_incomp, 0, 0)


def abi_txt2xls():
    host_ip = get_host_ip()
    hostname = socket.gethostname()
    excel_file_name = "UOS_migration_log_"+host_ip+"_"+hostname+"_"+datetime.datetime.now().strftime('%Y%m%d%H%M')+".xls"
    report_name_check = report_path_bef + excel_file_name

    if os.path.exists(report_name_check):
        os.remove(report_name_check)
    check_file = xlwt.Workbook(encoding='utf-8', style_compression=0)
    system_info(check_file)
    pkg_comp(check_file)
    abi_incomp_info(check_file)
    abi_comp_pkg(check_file)
    check_file.save(report_name_check)


def abi_txt2xls_after_mig():
    host_ip = get_host_ip()
    hostname = socket.gethostname()
    excel_file_name_after = ("UOS_migration_log_"+host_ip+"_"+hostname+"_"+datetime.datetime.now()
                             .strftime('%Y%m%d%H%M')+".xls")
    report_name_after = report_path_ago+excel_file_name_after

    if os.path.exists(report_name_after):
        os.remove(report_name_after)
    after_mig_xls = xlwt.Workbook(encoding='utf-8', style_compression=0)
    system_info_after(after_mig_xls)
    pkg_comp_after(after_mig_xls)
    abi_incomp_info(after_mig_xls)
    abi_comp_pkg(after_mig_xls)
    after_mig_xls.save(report_name_after)
