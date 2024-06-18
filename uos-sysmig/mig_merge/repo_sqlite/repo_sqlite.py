import os
import platform

from utils import run_cmd

def repo_sqlite():
    '''
        应用场景：获取sqlite文件
        功    能：
        输入参数：无
        返 回 值：json数据
    '''


    repomd_name = 'repodata/repomd.xml'
    arch = platform.machine()

    pwd_dir = os.getcwd()

    os.chdir('/etc/yum.repos.d')

    cmd = 'grep -nr "^baseurl" *.repo'
    _, data, _ = run_cmd(cmd)
    baseurl_list = []
    for line in data:
        if line == '':
            continue

        baseurl = line.split('baseurl=')[1]
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
                cmd = 'wget %s%s' %(baseurl, repomd_name)
            else:
                cmd = 'wget %s/%s' %(baseurl, repomd_name)

        code, data, error = run_cmd(cmd)
            
    cmd = 'grep sqlite repomd.xml*'
    code, data, error = run_cmd(cmd)
    for line in data:
        sqlite_name_01 = line.split('"/>', 1)[0]

        sqlite_name = sqlite_name_01.rsplit('/', 1)[1]


def main():
    repo_sqlite()


if __name__ == "__main__":
    main()

