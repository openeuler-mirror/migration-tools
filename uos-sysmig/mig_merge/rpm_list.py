#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import stat

from config import FixedInfo
from repo_sqlite.utils import run_cmd
from migrationTools.scanRPM.scan_rpm import get_current_pkg_list
from migrationTools.scanRPM.scan_rpm import ParsedPkgInfo


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
        应用场景：当前系统包名与repo一致性判断
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
    if time_num <= 1:
        return True
    else:
        return False

def judge_bin_ynrepo(bin_name):
    '''
        应用场景：查找repo源上rpm包
        功    能：根据文件查找repo上rpm包
        输入参数：bin_name - 文件名 
        返 回 值：False - 不存在：
                  repo_repmname - repo源上rpm包
    '''

    cmd = 'repoquery --info %s' %(bin_name)
    _, data, _ = run_cmd(cmd)
    if data == '':
        print('The Current System of Repo Not Exit file %s' %(bin_name))
        return False
    else:
        for element in data:
            #print('element = %s' %(element))
            if 'Name' in element:
                repo_rpm_name = element.split(':',1)[1].strip()
                rpm_name = repo_rpm_name
            if 'Version' in element:
                repo_rpm_version = element.split(':',1)[1].strip()
                rpm_name = rpm_name+'-'+repo_rpm_version
            if 'Release' in element:
                repo_rpm_release = element.split(':',1)[1].strip()
                rpm_name = rpm_name+'-'+repo_rpm_release+'.x86_64.rpm'
    print('rpm_name = %s' %(rpm_name))
    return rpm_name


def rpmpkg_noexit_repo(rpm_name):
    '''
        应用场景：当前系统包名与repo不一致性判断
        功    能：rpm包名不存存在repo源,通过文件关联
        输入参数：rpm_name - rpm包名
        返 回 值：repo_rpm_name - repo源中rpm包名
                  False - bin文件没有关联上repo源中rpm包
    '''

    repo_rpmpkg = rpm_name.rsplit('-', 2)[0]
    cmd = 'rpm -ql --noartifact %s' %(repo_rpmpkg)
    _, data, _ = run_cmd(cmd)

    #目前只判断rpm包中一个二进制文件是否能够关联repo上的rpm包
    for file_name in data:
        if is_ELFfile(file_name):
            repo_rpm_name = judge_bin_ynrepo(file_name)
            if repo_rpm_name:
                return repo_rpm_name
            else:
                return False 

def rpm_list():
    '''
        应用场景：获取repo源rpm包列表
        功    能：根据当前系统rpm包列表，获取repo源上rpm包列表
        输入参数：
        返 回 值：repo_pkg_list - 当前系统与repo源相同的rpm包列表
    '''

    repo_pkg_list = []
    current_pkgs_list = get_current_pkg_list()
    diff_rpmpkg_file = 'diff-rpmpkg-file.txt'
    fpd = open(diff_rpmpkg_file, 'w')
    for pkg in current_pkgs_list:
        #rpm包名与repo源包名一致,写入repo_pkg_list
        if judge_rpmpkg_exitrepo(pkg):
            repo_pkg = pkg.rsplit('-',2)[0]
            repo_pkg_list.append(repo_pkg)

        #rpm包名与repo源包名不一致,通过rpm包中文件关联
        else:
            repo_pkgname = rpmpkg_noexit_repo(pkg)
            if repo_pkgname:
                print('repo源上存在rpm包名')
                repo_pkg_list.append(repo_pkgname)
                diff_rpmpkg_name = pkg.rsplit('-',2)[0] + '|' + repo_pkgname
                fpd.write(diff_rpmpkg_name)
            else:
                print('repo源上不存在rpm包名')
                continue
    fpd.close()

    return repo_pkg_list

def main():
    #rpm_list()
    bin_name = '/usr/lib64/libgovirt.so.2'
    judge_bin_ynrepo(bin_name)
    
if __name__ == "__main__":
    main()

