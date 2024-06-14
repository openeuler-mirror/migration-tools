import sys
import json
import platform

#for test 
sys.path.append("..")

from mig_merge.config import FixedPageInfo
from mig_merge.new_expansion.scan_rpms import scan_rpms
from sysmig_agent.migrationTools.scanHardware import utils
from sysmig_agent.migrationTools.utils.config import PathConf
from sysmig_agent.migrationTools.scanConf.scanconf import ScanConf
from sysmig_agent.migrationTools.exportSysConf.paramdata import ParamData

class MigrationMerge:

    def __init__(self) -> None:
        self.template_dir = FixedPageInfo.report_template_dir
        self.report_dir = FixedPageInfo.report_dir

        data = self.hardware_analysis()
        data = data + self.conf_scan()
        data = data + self.rpms_scan()
        data = data + self.sysconf_diff()

    def hardware_analysis(self):
        '''硬件兼容性分析
            按照前后端接口，生成json格式数据，对应html报告tab页
        '''
        compatability_list = utils.get_compatability_list(
            utils.get_pci_list(), utils.get_supported_device_list(), False)
        jsonstr = json.dumps(compatability_list)
        return jsonstr


