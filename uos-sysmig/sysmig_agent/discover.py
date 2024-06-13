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


class DetInformation(Discover):
    def __init__(self, data):
        """
        data 包含server传入json数据
        Args:
            data:
        """
        super().__init__()
        self.task_id = json.loads(data).get('task_id')
        self.data = data

    def check_scanhardware(self):
        """
        硬件信息检测
        Returns:"success"
        """
        # 更新SQL任务状态
        statue = 1
        sql_task_statue(statue, self.task_id)
        # 发送消息给Server更新任务流状态
        post_server('task_start', self.task_id)
        Discover._check_scanhardware(self)
        # 更新SQL任务状态
        sql_task_statue(statue, self.task_id)
        post_server('task_close', self.task_id)
        return 'success'

    def check_scansysconf(self):
        """
        配置兼容性评估
        Returns:"success"
        """
        # 更新SQL任务状态
        statue = 1
        sql_task_statue(statue, self.task_id)
        # 发送消息给Server更新任务流状态
        post_server('task_start', self.task_id)
        Discover._check_scansysconf(self)
        # 更新SQL任务状态
        sql_task_statue(statue, self.task_id)
        post_server('task_close', self.task_id)
        return 'success'

    def check_scanrpms(self):
        """
        系统 rpm对比检测
        Returns:"success"
        """
        # 更新SQL任务状态
        statue = 1
        sql_task_statue(statue, self.task_id)
        # 发送消息给Server更新任务流状态
        post_server('task_start', self.task_id)
        Discover._check_scanrpms(self)
        # 更新SQL任务状态
        sql_task_statue(statue, self.task_id)
        post_server('task_close', self.task_id)
        return 'success'

    def check_exportsysconf(self):
        """
        系统配置文件，md5更改的文件检索，暂时保留，需要链接centos的源泉解压对比
        Returns:
        """
        pass


discover = Discover()
