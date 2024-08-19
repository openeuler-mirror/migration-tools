#!/bin/python3
import json
import glob
import os
import shutil

from sysmig_agent.migrationTools.scanConf.utils import run_cmd
from sysmig_agent.migrationTools.utils.logger import Logger

logger = Logger(__name__)


class ParamData():
    def __init__(self, config_file):
        self.rpm_set = set()
        self.cache_dir = "/var/tmp/utmtc/exportsysconf"
        ## json 配置文件读取
        self.data = self.read_json_config(config_file)
        ## 配置精简, 有些配置文件在当前系统不存在
        self._get_valid_config_data()
        self._get_rpm_name()
        self._download_rpm_pkgs(self.cache_dir)
        self._get_origin_config_file(self.cache_dir)
        self._gen_diff_content(self.cache_dir)
        self.return_data = self._gen_diff_config_file()

    ## write data to a json file
    def write_json_config(self):
        file_path = os.path.join(self.cache_dir, "exportsysconf.json")
        with open(file_path, 'w') as f:
            json.dump(self.return_data, f)

        logger.info(
            "The current system configuration files  has been generated.")
        logger.info(f"The path where the data is saved is {self.cache_dir}")
        logger.info("You can view the export results via a browser web page "
                    "by running the `utmtc exportsysconfserver` command.")
        return

    def _gen_diff_config_file(self):
        data = list()
        for item in self.data:
            #logger.info("confgroupName is %s" % item["confGroupName"])
            new_confList = list()
            for conf in item["confList"]:
                new_conf = dict()
                if "diff" not in conf.keys():
                    continue
                if os.path.getsize(conf['diff']) == 0:
                    ## remove empty diff file
                    if os.path.exists(conf['diff']):
                        os.remove(conf['diff'])
                    continue
                new_conf.update({"confName": conf["confName"]})
                new_conf.update({"desc": conf["desc"]})
                new_conf.update({"diff": conf["diff"]})
                if len(new_conf) > 0:
                    new_confList.append(new_conf)

            if len(new_confList) > 0:
                new_item = dict()
                new_item.update({"confGroupName": item["confGroupName"]})
                new_item.update({"confList": new_confList})
                data.append(new_item)
        # logger.info("data: %s" % data)
        return data

    def _gen_diff_content(self, cache_dir):

        a_dir = ".a"
        b_dir = ".b"
        a_full_dir = cache_dir + "/" + a_dir
        b_full_dir = cache_dir + "/" + b_dir
        diff_dir = cache_dir + "/.diff"
        for dir in [a_full_dir, b_full_dir, diff_dir]:
            if not os.path.exists(dir):
                os.makedirs(dir)

        logger.info("The diff file is being generated.")
        for item in self.data:
            for conf in item["confList"]:
                if "confName" not in conf.keys():
                    continue
                ## 原始配置文件找不到，生成同名空文件
                if "originConfName" not in conf.keys():
                    if os.path.exists(conf["confName"]):
                        basename = os.path.basename(conf["confName"])
                        dirname = os.path.dirname(conf["confName"])

                        a_conf_dirname = a_full_dir + dirname
                        b_conf_dirname = b_full_dir + dirname
                        if not os.path.exists(a_conf_dirname):
                            os.makedirs(a_conf_dirname)
                        if not os.path.exists(b_conf_dirname):
                            os.makedirs(b_conf_dirname)
                        shutil.copy(conf["confName"], a_conf_dirname)
                        ## add read permission
                        os.chmod(a_conf_dirname + "/" + basename, 0o777)
                        ## 清空 a 下的文件
                        with open(os.path.join(a_conf_dirname, basename),
                                  'w') as f:
                            pass
                        shutil.copy(conf["confName"], b_conf_dirname)
                        os.chmod(b_conf_dirname + "/" + basename, 0o777)
                else:
                    ## originConfName 存在
                    basename = os.path.basename(conf["confName"])
                    dirname = os.path.dirname(conf["confName"])
                    a_conf_dirname = a_full_dir + dirname
                    b_conf_dirname = b_full_dir + dirname
                    if not os.path.exists(a_conf_dirname):
                        os.makedirs(a_conf_dirname)
                    if not os.path.exists(b_conf_dirname):
                        os.makedirs(b_conf_dirname)

                    shutil.copy(conf["originConfName"], a_conf_dirname)
                    os.chmod(a_conf_dirname + "/" + basename, 0o777)
                    shutil.copy(conf["confName"], b_conf_dirname)
                    os.chmod(b_conf_dirname + "/" + basename, 0o777)

                a_file = a_dir + conf["confName"]
                b_file = b_dir + conf["confName"]
                diff_basename = conf["confName"].replace("/", "_") + ".diff"
                cmd = f"diff -U -1 {a_file} {b_file} > {diff_dir}/{diff_basename}"
                pwd = os.getcwd()
                os.chdir(cache_dir)
                # logger.info(f"run cmd: {cmd}")
                run_cmd(cmd)
                os.chdir(pwd)
                conf.update({"diff": diff_dir + "/" + diff_basename})
        logger.info("The diff file has been generated.")
        # logger.info("data: %s" % self.data)

    def _get_valid_config_data(self):
        """
        去除配置文件中不存在的配置文件, 和空的配置文件
        """
        for item in self.data:
            ## enumerate 有点问题
            i = 0
            for conf in item["confList"]:
                # logger.info(f"conf: {conf}")
                file = conf["confName"]
                if os.path.isfile(file):
                    if os.path.getsize(file) >= 0:
                        logger.info(f"found config file: {file}")
                    else:
                        logger.info(f"config file {file} is empty.")
                        conf.clear()
                else:
                    logger.info(f"config file {file} not exists")
                    conf.clear()
                i += 1
        # logger.info(f"data: {self.data}")

    def _get_origin_config_file(self, dl_dir):
        dl_dir = os.path.join(dl_dir, "packages")

        dst_dir = os.path.join(dl_dir, "cpiodir")
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        ## Unzip the rpm-terminated files in the dl_dir directory to the /tmp directory
        for dirpath, _, filenames in os.walk(dl_dir):
            filenames[:] = [f for f in filenames if f.endswith('.rpm')]
            # pushd dest dir
            cwd = os.getcwd()
            os.chdir(dst_dir)
            for filename in filenames:
                filename = os.path.join(dirpath, filename)
                cmd = f'rpm2cpio {filename} | cpio -idm'
                run_cmd(cmd)
                # logger.info(f"file: {filename}")
            # popd
            os.chdir(cwd)
        ## file of downloaded
        for item in self.data:
            for conf in item["confList"]:
                if "rpmName" not in conf.keys():
                    continue
                originConfName = dst_dir + conf["confName"]
                if os.path.exists(originConfName):
                    conf.update({"originConfName": originConfName})

        logger.debug(f"data: {self.data}")

    def _download_rpm_pkgs(self, dl_dir):
        dl_dir = os.path.join(dl_dir, "packages")
        if not os.path.exists(dl_dir):
            os.makedirs(dl_dir)
        for item in self.data:
            for conf in item["confList"]:
                if "rpmName" not in conf.keys():
                    continue
                rpm_name = conf["rpmName"]
                if rpm_name not in self.rpm_set:
                    self.rpm_set.add(rpm_name)
        dl_rpms = self.rpm_set
        logger.info(
            f"The following package will be downloaded, but will not be installed: {dl_rpms}"
        )
        for rpm in dl_rpms:
            cmd = f'yumdownloader --destdir={dl_dir} {rpm}'
            logger.info(f"running: {cmd}")
            returncode, stdout, stderr = run_cmd(cmd)

            if returncode != 0:
                ## package changed
                #if rpm.split('.')[-2] == "centos-release":
                if (rpm.split('.')[-2] == "centos-release") or (rpm.split('.')[-2] == "centos-linux-release"):
                    rpm = "uos-release"
                    cmd = f'yumdownloader --destdir={dl_dir} {rpm}'
                    logger.info(f"running: {cmd}")
                    returncode, stdout, stderr = run_cmd(cmd)
            if returncode != 0:
                raise Exception(
                    f"download rpm {rpm} error: {stderr} {stdout}"
                    "\nPlease check system network or yum repository settings and try again."
                )
                continue
            logger.info(f"download rpm {rpm} success.")

    def _get_rpm_name(self):
        """
        get rpm name from data.
        """
        def get_rpm_name_of_file(file):
            '''
            get rpm name from file
            :param file: file path
            :return: None or str
            '''
            if file is None:
                return None
            ## rpm 包名称只过滤name
            # cmd = r'rpm -qf --qf "%{name}-%{version}" ' + file
            cmd = r'rpm -qf --qf "%{name}.%{arch}\n" ' + file
            returncode, rpm_name, error = run_cmd(cmd)
            if returncode != 0:
                logger.debug(f"error: {error}")
                return None
            ## /etc/rc.local belongs to systemd and initscript， choose first
            return rpm_name[0]

        for item in self.data:
            for conf in item["confList"]:
                if "confName" not in conf.keys():
                    continue
                file = conf["confName"]
                ## get rpm name of file
                rpm_name = get_rpm_name_of_file(file)
                if rpm_name is None:
                    logger.info(f"{file} does not match any rpm package.")
                    continue
                conf.update({"rpmName": rpm_name})
        logger.debug("data: %s" % self.data)
        return

    def get_param_config_data(self):
        param_config_data = self.read_json_config(self.config_file)
        if param_config_data is None:
            logger.error("param config data is None.")
            return
        data = {"kind": []}
        for item in param_config_data["kind"]:

            file_list = []
            for glob_line in item["file"]:
                files = glob.glob(glob_line)
                for file in files:
                    if file not in file_list and os.path.isfile(file):
                        file_list.append(file)
            logger.info("file_list: %s" % file_list)
            data['kind'].append({'name': item['name'], 'file': file_list})
        self.data = data
        logger.debug("self.data: %s" % self.data)

    def read_json_config(self, config_file) -> list:
        """
        read json config file.
        :param config_file:
        :return:
        list/None
        """
        data = None
        if config_file is None:
            logger.error("config file is None.")
            return data
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.decoder.JSONDecodeError as error:
            logger.error("read json config file error: %s" % error)
        return list(data)
