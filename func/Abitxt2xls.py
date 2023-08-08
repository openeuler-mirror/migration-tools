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

txtFileName = '/var/tmp/uos-migration/data/exp-rst/abi-compat-pkg.txt'
txtFileName1 = '/var/tmp/uos-migration/data/exp-rst/abi-incompat-pkg.txt'
SysInfoFile = '/var/tmp/uos-migration/data/exp-rst/systeminfo.txt'
SysInfoFile_after = '/var/tmp/uos-migration/data/exp-rst/trans-end-sysinfo.txt'
PkgCompFile1= '/var/tmp/uos-migration/data/exp-rst/pkginfo_1.txt'
PkgCompFile2= '/var/tmp/uos-migration/data/exp-rst/pkginfo_2.txt'
PkgCompFile3= '/var/tmp/uos-migration/data/exp-rst/pkginfo_3.txt'
PkgCompFile4= '/var/tmp/uos-migration/data/exp-rst/pkginfo_4.txt'


def get_host_ip():
    """
    查询本机ip地址
    :return:
    """
    uos_sysmig_conf = json.loads(getSysMigConf())
    ip = json.loads(uos_sysmig_conf).get('agentip').strip()[1:-1]
    return ip


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

def system_info(check_file):
    #新建一个sheet
    sheet_sysinfo = check_file.add_sheet("系统基本信息")
    accord_line_write(SysInfoFile, sheet_sysinfo, 0, 0)


#sheet1-系统基本信息
def system_info_after(sys):
    #新建一个sheet
    sheet_sysinfo = sys.add_sheet("系统基本信息")
    accord_line_write(SysInfoFile_after, sheet_sysinfo, 0, 0)


#sheet2-软件包对比
def pkg_comp(pkg):
    #新建一个sheet
    sheet_pkgcomp = pkg.add_sheet("软件包对比")
    accord_line_write(PkgCompFile1, sheet_pkgcomp, 0, 0)
    accord_colu_write(PkgCompFile2, sheet_pkgcomp, 3, 0)
    accord_colu_write(PkgCompFile4, sheet_pkgcomp, 3, 1)


#sheet4-ABI兼容
def abi_incomp_info(file_incomp):
    #新建一个sheet
    sheet_comp = file_incomp.add_sheet("ABI兼容")
    accord_line_write(txtFileName, sheet_comp, 0, 0)

#sheet5-ABI不兼容
def abi_comp_pkg(file_comp):
    #新建一个sheet
    sheet_incomp = file_comp.add_sheet("ABI不兼容")

    accord_line_write(txtFileName1, sheet_incomp, 0, 0)

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
    abi_incomp_info(check_file)
    abi_comp_pkg(check_file)

    check_file.save(report_name_check)


def abi_txt2xls_after_mig():

    hostip = get_host_ip()
    hostname = socket.gethostname()
    excelFileName_after = "UOS_migration_log_"+hostip+"_"+hostname+"_"+datetime.datetime.now().strftime('%Y%m%d%H%M')+".xls"

    report_name_after=report_path_ago+excelFileName_after

    if os.path.exists(report_name_after):
        os.remove(report_name_after)

    #新建一个excel文件
    after_mig_xls = xlwt.Workbook(encoding='utf-8',style_compression=0)

    system_info_after(after_mig_xls)
    pkg_comp(after_mig_xls)
    abi_incomp_info(after_mig_xls)
    abi_comp_pkg(after_mig_xls)

    after_mig_xls.save(report_name_after)