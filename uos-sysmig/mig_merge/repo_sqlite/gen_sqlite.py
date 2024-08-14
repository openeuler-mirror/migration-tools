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


def gen_baseurl_list():
    '''
        应用场景：repo源baseurl列表
        功    能：获取repo源所有baseurl
        输入参数：无
        返 回 值：baseurl列表
    '''

    baseurl_list = []

    cmd = 'grep -r "^baseurl" /etc/yum.repos.d/*.repo'
    stat, baseurl_data, error = run_cmd(cmd)
    if stat != 0:
        print('error = %s' %(error))
        return '-1'

    cmd = 'grep -r "^enabled" /etc/yum.repos.d/*.repo'
    stat, enabled_data, error = run_cmd(cmd)
    if stat != 0:
        print('error = %s' %(error))
        return '-1'

    num = 0
    for line in enabled_data:
        if line == '':
            continue
        if line.split('=')[1].strip() == '1':
            baseurl_list.append(baseurl_data[num])
        num += 1

    return baseurl_list

def gen_sqlite(baseurl_list):
    '''
        应用场景：下载repo源sqlite文件
        功    能：从指定repo源下载sqlite压缩文件，解压生成sqlite文件列表
        输入参数：无
        返 回 值：sqlite列表
    '''

    sqlite_list = []
    #os.system('yum clean all & yum makecache')
    cmd = 'grep -r primary.sqlite %s' %(FixedInfo.repo_cache)
    stat, data, error = run_cmd(cmd)
    if stat == 0:
        for line in data:
            if '-primary.sqlite' in line:
                string = line.split('href="')[1].split('"')[0]
                suffix = string.rsplit('.', 1)[1]
                compression_sqlite = FixedInfo.sqlite_dir + '/' + string.split('/')[1]

                for baseurl in baseurl_list:
                    cmd = 'wget %s/%s -P %s' %(baseurl, string, FixedInfo.sqlite_dir)
                    stat, data, error = run_cmd(cmd)
                    if os.path.isfile(compression_sqlite):
                        print('file exit %s' %(compression_sqlite))

                        #解压sqlite.bx2
                        if suffix == 'xz':
                            unpack_cmd = 'xz -d'
                        elif suffix == 'bz':
                            unpack_cmd = 'bzip2 -d'
                        else:
                            print('add file suffix %s deal!!!' %(unpack_cmd))

                        cmd = '%s %s' %(unpack_cmd, compression_sqlite)
                        code, data, error = run_cmd(cmd)
                        if code == 0:
                            sqlite_list.append(compression_sqlite.rsplit('.', 1)[0])
                        
def main():
    #print(gen_repo_sqlite('A'))
    baseurl_list = gen_baseurl_list()
    print(gen_sqlite(baseurl_list))

if __name__ == "__main__":
    main()

