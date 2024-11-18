#r/tmp/'!/bin/python3
import json
import glob
import os
import shutil

from mig_merge.migrationTools.scanConf.utils import run_cmd
from mig_merge.migrationTools.utils.logger import Logger
from mig_merge.stock_replace.confirm import system_version_id
from mig_merge.config import FixedInfo

logger = Logger(__name__)


class public_relations():
    def __init__(self, config_file):
        self.rpm_set = set()
        self.cache_dir = "/var/tmp/uos-migration/data"
        ## json 配置文件读取
        self.data = self.read_json_config(config_file)
        self._gen_diff_content(self.cache_dir)
        self.return_data = self._gen_diff_config_file()

    def _gen_diff_config_file(self):
        data = list()
        for item in self.data:
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
                new_conf.update({"diffContent": conf["diffContent"]})
                if len(new_conf) > 0:
                    new_confList.append(new_conf)

            if len(new_confList) > 0:
                new_item = dict()
                new_item.update({"confGroupName": item["confGroupName"]})
                new_item.update({"confList": new_confList})
                data.append(new_item)
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

        if not os.path.exists(FixedInfo.pr_diff_path):
            os.makedirs(FixedInfo.pr_diff_path)

        logger.info("The diff file is being generated.")

        if system_version_id() == '8':
            std_path = FixedInfo.pr_cfg_path + '/1050a'
        else:
            std_path = FixedInfo.pr_cfg_path + '/1002a'

        for item in self.data:
            for conf in item["confList"]:
                returncode, stdout, stderr = run_cmd(conf["path"])
                data_file_name = FixedInfo.pr_data_path + '/' +conf["items"]
                fp = open(data_file_name, "w")
                for line in stdout:
                    fp.write(line+'\n')
                fp.close()
                os.chmod(data_file_name, 0o777)

                base_file_name = std_path + '/' +conf["items"]

                shutil.copy(base_file_name, b_full_dir+'/'+conf["items"])
                os.chmod(b_full_dir + "/" + conf["items"], 0o777)

                a_file = a_dir + '/' + conf["items"]
                b_file = b_dir + '/' + conf["items"]
                diff_file_name = FixedInfo.pr_diff_path + '/' + conf["items"] + ".diff"

                #cmd = f"diff -U -1 {data_file_name} {base_file_name} > {diff_file_name}"
                cmd = f"diff -U -1 {a_file} {b_file} > {diff_file_name}"
                pwd = os.getcwd()
                os.chdir(cache_dir)
                run_cmd(cmd)
                os.chdir(pwd)

                conf.update({"diff": diff_file_name})

                cmd1 = f"cat {diff_file_name}"
                returncode, stdout, stderr = run_cmd(cmd1)
                diff_tmp = ""
                for tmp in stdout:
                    tmp_01 = tmp+'\n'
                    diff_tmp = diff_tmp + tmp_01
                conf.update({"diffContent": diff_tmp})
        logger.info("The diff file has been generated.")

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
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                return []
        except json.decoder.JSONDecodeError as error:
            logger.error("read json config file error: %s" % error)
        return list(data)

def main():
    param_config_file = 'mig_merge/data/pr_conf/pr_confsysconf.json'
    param_data = public_relations(param_config_file)

if __name__ == "__main__":
    main()
