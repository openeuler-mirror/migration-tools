#!/usr/bin/env python3
# coding=utf-8

import os

from mig_merge.migrationTools.scanConf.utils import run_cmd
from mig_merge.merge.utils import is_number

def gen_system_mark():
    """
        应用场景：repo源标志
        功    能：指定repo源标志，如1000c/1020a/1051a
                  目前只支持1001c和1020a repo源
        输入参数：
        返 回 值：mark - repo源标志
    """


    flag = False
    mark_name = 'uos-release'
    mark_path = './tmp'
    mark_list = ['1020a','1021a','1050a','1051a']

    cur_dir = os.getcwd()
    if os.path.isdir(mark_path):
        os.system('rm -rf %s' %(mark_path))
    os.makedirs(mark_path)

    #os.system('yumdownloader --destdir=%s %s --skip-broken' %(mark_path, mark_name))
    cmd = 'yumdownloader --destdir=%s %s --skip-broken' %(mark_path, mark_name)
    code, data, error = run_cmd(cmd)
    os.chdir(mark_path)

    for element in os.popen('ls *x86_64.rpm'):

        if mark_name in element:
            if is_number(element.split(mark_name)[1][1]):
                os.system('rpm2cpio %s*|cpio -idmv' %(mark_name))
                issue_name = './etc/issue'
                with open(issue_name, 'r') as fp:
                    mark = 'uos-' + str(fp.read())[23:28]
        
                if mark in mark_list:
                    flag = True
                    break
                else:
                    issue_name = './etc/productinfo'
                    with open(issue_name, 'r') as fp:
                        mark = 'uos-' + str(fp.read())[23:28]
                    if mark in mark_list:
                        flag = True
                    break
            elif element.split(mark_name)[1][1:7] == 'server':
                flag = True
                mark = 'uos-1001c'
                break
            else:
                continue
    #Repo sources not exit uos-release or uos-release-server
    if not flag:
        mark = 'uos-1020a'
        
    os.chdir(cur_dir)
    os.system('rm -rf %s' %(mark_path))

    return mark

if __name__ == "__main__":
    repo_mark = gen_system_mark()
    print(repo_mark)

