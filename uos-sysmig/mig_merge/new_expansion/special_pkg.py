#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import stat
import shutil

from config import FixedInfo
from repo_sqlite.utils import run_cmd
from migrationTools.scanRPM.scan_rpm import get_current_pkg_list
from logger import migration_log


def is_ELFfile(filepath):
    '''
        应用场景：ELF文件判断
        功    能：判断文件是否为ELF类型
        输入参数：filepath - 文件名
        返 回 值：False - 不是ELF类型
                  True - 是ELF类型
    '''

    if not os.path.exists(filepath):
        return False
    try:
        FileStates = os.stat(filepath)
        FileMode = FileStates[stat.ST_MODE]
        if not stat.S_ISREG(FileMode) or stat.S_ISLNK(FileMode):
            return False
        with open(filepath, 'rb') as f:
            header = (bytearray(f.read(4)[1:4])).decode(encoding="utf-8")
            if header in ["ELF"]:
                return True
    except UnicodeDecodeError as e:
        pass
    return False

def judge_rpmpkg_exitrepo(rpm_name):
    '''
        应用场景：rpm包一致性判断
        功    能：rpm包名是否存在repo源
        输入参数：rpm_name - rpm包名
        返 回 值：True - 存在；False - 不存在
    '''

    time_num = 0
    repo_rpmpkg = rpm_name.rsplit('-', 2)[0]

    cmd = 'yum list %s' %(repo_rpmpkg)
    _, data_list, _ = run_cmd(cmd)
    for data in data_list:
        if repo_rpmpkg in data:
            time_num += 1
    if time_num >= 1:
        return True
    else:
        return False

def judge_bin_ynrepo(bin_name):
    '''
        应用场景：二进制文件查找
        功    能：根据文件查找repo上rpm包
        输入参数：bin_name - 文件名 
        返 回 值：False - 不存在：
                  rpm_name - repo源上rpm包
    '''

    cmd = 'repoquery --info %s' %(bin_name)
    _, data, _ = run_cmd(cmd)
    if data == '':
        migration_log.inifo('the current system of repo not exit file: ' +bin_name)
        return False
    else:
        rpm_name = ''
        for element in data:
            if 'Name' in element:
                repo_rpm_name = element.split(':',1)[1].strip()
                rpm_name = repo_rpm_name
            if 'Version' in element:
                repo_rpm_version = element.split(':',1)[1].strip()
                rpm_name = rpm_name+'-'+repo_rpm_version
            if 'Release' in element:
                repo_rpm_release = element.split(':',1)[1].strip()
                rpm_name = rpm_name+'-'+repo_rpm_release+'.x86_64.rpm'

    return rpm_name


def rpmpkg_noexit_repo(rpm_name):
    '''
        应用场景：rpm包一致性判断
        功    能：rpm包名不存存在repo源,通过二进制文件关联rpm包名
        输入参数：rpm_name - rpm包名
        返 回 值：repo_rpm_name - repo源中rpm包名
                  False - bin文件没有关联上repo源中rpm包
    '''

    cmd = 'rpm -ql --noartifact %s' %(rpm_name)
    _, data, _ = run_cmd(cmd)

    #目前只判断rpm包中一个二进制文件是否能够关联repo上的rpm包
    for file_name in data:
        file_name = file_name.strip('\n')
        if not os.path.exists(file_name):
            continue
        if os.path.isdir(file_name):
            continue
        if '.' in file_name.rsplit('/', 1)[1]:
            if '.' + file_name.rsplit('.', 1)[1] in FixedInfo.suffix_list:
                continue

        if is_ELFfile(file_name):
            repo_rpm_name = judge_bin_ynrepo(file_name)
            if repo_rpm_name:
                return repo_rpm_name
            else:
                return False 

def gen_reporpm_list():
    '''
        应用场景：repo源特定软件包判断
        功    能：当前系统特有软件包，通过二进制文件关联repo源中rpm包
        输入参数：
        返 回 值：repo_pkg_list - 当前系统与repo源特定包列表
                  -1 - 不存在特定包列表
    '''

    #repo源不存在特定软件包
    repo_not = False
    repo_pkg_list = ''

    #1xxxa生成的当前系统特有rpm包中，存在包名不同二进制文件相同情况
    fpd = open(FixedInfo.diff_rpmpkg, 'w')

    #1xxxa生成的当前系统特有rpm列表文件，去除二进制相同包名不同的软件包
    #重新生成当前系统特有rpm列表文件                                                               
    fps = open(FixedInfo.same_rpmpkg, 'w')

    with open(FixedInfo.unique_pkgname, 'r') as fp:
        current_unique_list = fp.readlines()

    for element_name in current_unique_list:
        pkg =  element_name.replace('\n', '')
        if pkg == '':
            continue
        #rpm包名与repo源包名不一致,通过rpm包中文件关联
        repo_pkgname = rpmpkg_noexit_repo(pkg)
        if repo_pkgname:
            migration_log.info('current system rpm【'+pkg+'】VS repo of rpm 【'+repo_pkgname+'】')
            #repo_pkg_list.append(repo_pkgname.rsplit('-', 2)[0])
            repo_pkg_list = repo_pkg_list+' '+repo_pkgname.rsplit('-', 2)[0]

            diff_rpmpkg_name = pkg + '|' + repo_pkgname
            fpd.write(diff_rpmpkg_name+'\n')
            #repo源存在特定软件包
            repo_not = True
        else:
            migration_log.info('repo of rpm not exit: ' +pkg)
            fps.write(pkg+'\n')
            continue
    fpd.close()
    fps.close()

    if repo_not:
        migration_log.info('Specific software package list: ' +repo_pkg_list)
        return repo_pkg_list

    #拷贝当前系统特有软件包列表文件
    shutil.copy(FixedInfo.unique_pkgname, FixedInfo.same_rpmpkg)
    migration_log.info('Specific software package string same of current unique list')
    return '-1'

