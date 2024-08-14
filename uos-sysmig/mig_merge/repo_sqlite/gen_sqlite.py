import os
import platform

from mig_merge.migrationTools.scanConf.utils import run_cmd
from mig_merge.config import FixedInfo
#from sysmig_agent.Abisystmcompchk import logger_init


def gen_baseurl_list(log, mig_flag):
    '''
        应用场景：repo源baseurl列表
        功    能：获取当前系统repo源baseurl列表
        输入参数：logger 日志文件
        返 回 值：baseurl列表,-1 获取baseurl列表失败
    '''

    baseurl_list = []
    baseurl_data = []

    repoxml_dir = FixedInfo.sqlite_dir + '/repoxml'
    if not os.path.exists(repoxml_dir):
        os.makedirs(repoxml_dir)

    items = os.listdir(repoxml_dir)
    for name in items:
        if os.path.isfile(repoxml_dir+'/'+name):
            os.remove(repoxml_dir+'/'+name)

    #baseurl list
    if mig_flag == 'A':
        cmd = 'grep -r "^baseurl" /etc/yum.repos.d/*.repo'
    elif mig_flag == 'E':
        cmd = 'grep -r "^baseurl" /var/tmp/uos-migration/migration_after.repo'
    else:
        log.error('migration flag error:' +mig_flag)

    stat, baseurl, error = run_cmd(cmd)
    if stat != 0:
        log.error('execute error:' +error)
        return '-1'

    for line in baseurl:
        if line == '':
            continue
        if '$baseurl' in line:
            arch = platform.machine()
            line = line.replace('$baseurl', arch)
        baseurl_data.append(line)
        
    #enable list
    if mig_flag == 'A':
        cmd = 'grep -r "^enabled" /etc/yum.repos.d/*.repo'
    elif mig_flag == 'E':
        cmd = 'grep -r "^enabled" /var/tmp/uos-migration/migration_after.repo'
    else:
        log.error('migration flag error:' +mig_flag)

    stat, enabled_data, error = run_cmd(cmd)
    if stat != 0:
        log.error('execute error:' +error)
        return '-1'

    #get enable = 1 of baseurl
    num = 0
    for line in enabled_data:
        if line == '':
            continue
        if line.split('=')[1].strip() == '1':

            if "http" in baseurl_data[num]:
                cmd = 'wget %s/repodata/repomd.xml -P %s' %(baseurl_data[num], repoxml_dir)
            else:
                cmd = 'cp -rf %s/repodata/repomd.xml %s' %(baseurl_data[num].split('/', 2)[2], repoxml_dir)
            stat, data, error = run_cmd(cmd)
            if stat != 0:
                log.error('get repomd.xml error:' +error)

            baseurl_list.append(baseurl_data[num])
        num += 1

    return baseurl_list

def gen_sqlite(logger,mig_flag):
    '''
        应用场景：下载repo源sqlite文件
        功    能：从指定repo源下载sqlite压缩文件，解压生成sqlite文件列表
        输入参数：logger 日志文件
        返 回 值：sqlite_list 列表,-1 获取sqlite文件列表失败
    '''

    sqlite_list = []

    if not os.path.exists(FixedInfo.sqlite_dir):
        os.makedirs(FixedInfo.sqlite_dir)

    items = os.listdir(FixedInfo.sqlite_dir)
    for name in items:
        if os.path.isfile(FixedInfo.sqlite_dir+'/'+name):
            if name.endswith(".sqlite"):
                os.remove(FixedInfo.sqlite_dir+'/'+name)

    baseurl_list = gen_baseurl_list(logger, mig_flag)
    if baseurl_list == '-1':
        logger.error('get baseurl of repo source failed!!!')
        return '-1'
    logger.info('get baseurl of repo source success:' +str(baseurl_list))

    repoxml_dir = FixedInfo.sqlite_dir + '/repoxml'
    cmd = 'grep -r primary.sqlite %s' %(repoxml_dir)
    stat, data, error = run_cmd(cmd)
    if stat == 0:
        for line in data:
            if '-primary.sqlite' in line:
                string = line.split('href="')[1].split('"')[0]
                suffix = string.rsplit('.', 1)[1]
                compression_sqlite = FixedInfo.sqlite_dir + '/' + string.split('/')[1]

                for baseurl in baseurl_list:
                    if "http" in baseurl:
                        cmd = 'wget %s/%s -P %s' %(baseurl, string, FixedInfo.sqlite_dir)
                    else:
                        cmd = 'cp -rf %s/%s -P %s' %(baseurl.split('/', 2)[2], string, FixedInfo.sqlite_dir)
                    stat, data, error = run_cmd(cmd)
                    if os.path.isfile(compression_sqlite):
                        logger.info('download file success:' +compression_sqlite)

                        #解压sqlite.bx2
                        if suffix == 'xz':
                            unpack_cmd = 'xz -d'
                        elif suffix == 'bz':
                            unpack_cmd = 'bzip2 -d'
                        elif suffix == 'bz2':
                            unpack_cmd = 'bzip2 -d'
                        else:
                            logger.error('add file suffix deal:' +suffix)

                        cmd = '%s %s' %(unpack_cmd, compression_sqlite)
                        code, data, error = run_cmd(cmd)
                        if code == 0:
                            logger.info('Unpack the sqlite success:' +compression_sqlite)
                            sqlite_list.append(compression_sqlite.rsplit('.', 1)[0])
                        else:
                            logger.info('Unpack the sqlite failure:' +compression_sqlite)
                            return '-1'

    else:
        logger.info('command execution failure:' +cmd)
        logger.error('error info:' +error)
        return '-1'

    logger.info('get sqlite list of repo source success:' +str(sqlite_list))

    return sqlite_list
    
#if __name__ == "__main__":
#    logger = logger_init()
#    gen_sqlite(logger,'E')

