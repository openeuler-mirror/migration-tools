#!/bin/python3
import sys
import os
from sysmig_agent.migrationTools.utils.logger import Logger
from sysmig_agent.migrationTools.exportSysConf.paramdata import ParamData
from sysmig_agent.migrationTools.utils.config import PathConf

logger = Logger(__name__)


class ExportSysConf():
    def run(self, args):
        try:
            self.gen_diff_conf()
        except Exception as e:
            logger.error(e)
            sys.exit(1)

    def gen_diff_conf(self):
        ## get the path of the config file
        PARAM_CONFIG_DIR = os.path.join(PathConf.data_path, "export-config")
        param_config_file = os.path.join(PARAM_CONFIG_DIR, "param_config.json")
        param_data = ParamData(param_config_file)
        param_data.write_json_config()


if __name__ == "__main__":
    ExportSysConf().run(sys.argv)
