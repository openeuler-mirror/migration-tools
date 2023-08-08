# coding=utf-8
'''''
main function：主要实现把txt中的每行数据写入到excel中
'''
#################
import datetime
import json
import socket
import xlwt

from func.share import *


#检测报告导出绝对路径
report_path_bef="/var/tmp/uos-migration/UOS_analysis_report/"
report_path_ago='/var/tmp/uos-migration/UOS_migration_log/'

SysInfoFile = '/var/tmp/uos-migration/data/exp-rst/systeminfo.txt'

def get_host_ip():
    """
    查询本机ip地址
    :return:
    """
    uos_sysmig_conf = json.loads(getSysMigConf())
    ip = json.loads(uos_sysmig_conf).get('agentip').strip()[1:-1]
    return ip


def system_info(check_file):
    #新建一个sheet
    sheet_sysinfo = check_file.add_sheet("系统基本信息")
    accord_line_write(SysInfoFile, sheet_sysinfo, 0, 0)


#sheet2-软件包对比
def pkg_comp(pkg):
    #新建一个sheet
    sheet_pkgcomp = pkg.add_sheet("软件包对比")
    accord_line_write(PkgCompFile1, sheet_pkgcomp, 0, 0)
    accord_colu_write(PkgCompFile2, sheet_pkgcomp, 3, 0)
    accord_colu_write(PkgCompFile4, sheet_pkgcomp, 3, 1)


def accord_line_write(txtLineFile, sheet_line, line_num, colu_num):
    # 通过列的形式写入文件
    with open(txtLineFile,'r') as line_f:
        x = line_num 
        y = colu_num 
        sys_lines = line_f.readlines()
        for line in sys_lines:
            for value in line.strip().split("|"):
                sheet_line.write(x,y,value)
                y += 1
            x += 1
            y = 0
    line_f.close()


def accord_colu_write(txtColuFile,sheet_colu, line_num, colu_num):
    # 通过行的形式写入文件
    with open(txtColuFile,'r') as colu_f:
        x = line_num 
        y = colu_num 
        sys_colus = colu_f.readlines()
        for line in sys_colus:
            for value in line.strip().split("|"):
                sheet_colu.write(x,y,value)
                x += 1
    colu_f.close()

def abi_txt2xls():
    #兼容性检查报告名规则：UOS_migration_log_10.0.2.3_cy.server_202110192140.xls
    hostip = get_host_ip()
    hostname = socket.gethostname()
    excelFileName = "UOS_migration_log_"+hostip+"_"+hostname+"_"+datetime.datetime.now().strftime('%Y%m%d%H%M')+".xls"

    report_name_check=report_path_bef+excelFileName

    if os.path.exists(report_name_check):
        os.remove(report_name_check)

    #新建一个excel文件
    check_file = xlwt.Workbook(encoding='utf-8',style_compression=0)

    system_info(check_file)
    pkg_comp(check_file)
    