from sysmig_agent.short_task import sql_task_statue, json
from sysmig_agent.migrationTools.scanRPM.scan_rpm import generate_rpm_list_js
from sysmig_agent.migrationTools.scanConf.scanconf import ScanConf
from sysmig_agent.migrationTools.scanHardware.scanhardware import generate_comtatibility_list_js


class Discover(object):
    def __init__(self):
        self.ret = 0

    def _check_scanhardware(self):
        """
        硬件信息检测
        Returns:
        """
        generate_comtatibility_list_js()

    def _check_scansysconf(self):
        """
        系统配置和系统服务检测,配置兼容性评估
        Returns:
        """
        ScanConf().run(0)

    def _check_scanrpms(self):
        """
        系统 rpm 对比检测
        Returns:
        """
        generate_rpm_list_js()

    def _check_exportsysconf(self):
        """
        系统配置文件，md5更改的文件检索，暂时保留，需要链接centos的源泉解压对比
        Returns:

        """
        pass

