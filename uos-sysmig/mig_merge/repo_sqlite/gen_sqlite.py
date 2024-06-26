import os
import platform

from mig_merge.repo_sqlite.utils import run_cmd
from mig_merge.config import FixedInfo


def existence_sqlite(Flag):
    '''
        应用场景：指定路径下sqlite文件是否存在
                  支持固化sqlite文件
        功    能：判断sqlite文件是否存在？是-使用；否-退出
        输入参数：Flag - A：1xxxa repo源
                         E：1xxxe repo源
        返 回 值：0-存在；-1不存在
    '''
    arch = platform.machine()

    if Flag == 'A':
        sqlite_path = os.path.join(FixedInfo.sqlite_dir, 'uos-1020a', arch)
    elif Flag == 'E':
        sqlite_path = os.path.join(FixedInfo.sqlite_dir, 'uos-1020a', arch)
    else:
        print('The migration type is incorrectly identified')
        return '-1'
    cmd = 'ls %s/*-primary.sqlite' %(sqlite_path)
    _, data, _ = run_cmd(cmd)

    if data == '':
        return '-1'
    else:
        for line in data:
            if line == '':
                data.remove(line)
        return data

