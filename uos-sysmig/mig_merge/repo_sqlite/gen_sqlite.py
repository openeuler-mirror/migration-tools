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


def gen_repo_sqlite(Flag):
    '''
        应用场景：获取sqlite文件
        功    能：从指定repo源下载primary.sqlite文件
        输入参数：Flag - A：获取1xxxa repo源sqlite
                         E：获取1xxxe repo源sqlite
        返 回 值：sqlite文件列表
    '''

    repomd_name = 'repodata/repomd.xml'
    specific_str = 'os'

    sqlite_list = []
    arch = platform.machine()
    if Flag == 'A':
        sqlite_path = os.path.join(FixedInfo.sqlite_dir, 'uos-1020a', arch)
    elif Flag == 'E':
        sqlite_path = os.path.join(FixedInfo.sqlite_dir, 'uos-1020a', arch)
    else:
        print('The migration type is incorrectly identified')
        return '-1'

    pwd_dir = os.getcwd()
    os.chdir('/etc/yum.repos.d')

    #生成baseurl列表,下载repomd.xml
    cmd = 'grep -nr "^baseurl" *.repo'
    _, data, _ = run_cmd(cmd)
    for line in data:
        if line == '':
            continue

        baseurl = line.split('baseurl')[1].split('=',1)[1].strip()
        if arch in baseurl:
            if baseurl[-1] == '/':
                cmd = 'wget %s%s' %(baseurl, repomd_name)
            else:
                cmd = 'wget %s/%s' %(baseurl, repomd_name)
        elif 'Source' in baseurl:
            if baseurl[-1] == '/':
                cmd = 'wget %s' %(baseurl.replace('Source/', repomd_name))
            else:
                cmd = 'wget %s' %(baseurl.replace('Source', repomd_name))
        else:
            if baseurl[-1] == '/':
                cmd = 'wget %s%s/%s/%s' %(baseurl, arch, specific_str, repomd_name)
            else:
                cmd = 'wget %s/%s/%s/%s' %(baseurl, arch, specific_str, repomd_name)

        #下载repomd.xml
        code, data, error = run_cmd(cmd)

        #获取sqlite.bz2
        cmd = 'grep primary.sqlite* repomd.xml*'
        code, data, error = run_cmd(cmd)
        for line in data:
            if line == '':
                continue

            sqlite_name_bz = line.split('"/>', 1)[0].rsplit('/',1)[1]
            sqlite_name = sqlite_name_bz.rsplit('.', 1)[0]
            suffix = sqlite_name_bz.rsplit('.', 1)[1]

            #下载sqlite.bz2 , xz
            cmd = 'wget -P %s %s%s/%s/repodata/%s' %(sqlite_path, baseurl, arch, specific_str, sqlite_name_bz)
            code, data, error = run_cmd(cmd)

            #解压sqlite.bx2
            if suffix == 'xz':
                unpack_cmd = 'xz -d'
            elif suffix == 'bz':
                unpack_cmd = 'bzip2 -d'
            else:
                print('add file suffix %s deal!!!' %(unpack_cmd))

            cmd = '%s %s/%s' %(unpack_cmd, sqlite_path, sqlite_name_bz)
            code, data, error = run_cmd(cmd)

        sqlite_list.append(FixedInfo.sqlite_dir+'/'+sqlite_name)

        cmd = 'rm -f repomd.xml'
        code, data, error = run_cmd(cmd)
        
    os.chdir(pwd_dir)
    return sqlite_list 
