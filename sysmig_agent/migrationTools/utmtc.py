#!/bin/python3
import argparse
import logging
import sys

from sysmig_agent.migrationTools.__init__ import __version__
from sysmig_agent.migrationTools.scanConf.scanconf import ScanConf
from sysmig_agent.migrationTools.scanHardware.scanhardware import \
    generate_comtatibility_list_js
from sysmig_agent.migrationTools.scanRPM.scan_rpm import generate_rpm_list_js
from sysmig_agent.migrationTools.utils.logger import Logger
from sysmig_agent.migrationTools.exportSysConf.exportSysConf import ExportSysConf
from sysmig_agent.migrationTools.exportSysConf.sysConfServer import start_server

logger = Logger(__name__)


## CLI arguments parser with subparsers
class Cli:
    def __init__(self) -> None:
        target_OS = "UnionTech OS Server 20"
        self.parser = argparse.ArgumentParser(
            formatter_class=argparse.RawTextHelpFormatter,
            description=
            f'''This tool is used to assist users in migrating operating systems to {target_OS} server operating systems.
The tool supports analysis of hardware compatibility, system configuration information differences, and installed rpm package difference information.
All scanning and analysis processes are performed locally and do not change the operating system configuration.
All scanning and analysis results are saved locally and not uploaded to external servers.
    ''')
        ## add subparsers
        self.subparsers = self.parser.add_subparsers(
            help='sub-command help',
            dest='subcommand',
        )
        ## add scan_hw parser
        self.scan_hw_parser = self.subparsers.add_parser(
            'scanhardware',
            help=
            f'Scan the hardware information of the currently system to evaluate whether the hardware is compatible with the {target_OS} operating system,'
            f' and output the difference comparison report.')
        ## add scan_sysconf parser
        self.scan_sysconf_parser = self.subparsers.add_parser(
            'scansysconf',
            help=
            f'Scan the system configuration and system service information of the current operating system,'
            f' compare it with the {target_OS} operating system, and output the difference comparison report.'
        )
        ## add scan_rpm parser
        self.scan_rpms_parser = self.subparsers.add_parser(
            'scanrpms',
            help=
            f'Scan the package and package availability information installed on the current operating system,'
            f' compare it with the {target_OS} operating system, and output a difference comparison report.'
        )
        self.export_sysconf_parser = self.subparsers.add_parser(
            'exportsysconf',
            help=
            'Exports the current system configuration changes for the operating system. '
            'After exporting the results you can run the `utmtc exportsysconfserver` command '
            'to view the exported results via a browser web page.')
        self.export_sysconf_server_parser = self.subparsers.add_parser(
            'exportsysconfserver',
            help="After running `utmtc exportsysconf` and generating "
            "the configuration results, view the exported system "
            "configuration via the browser web page")
        ## add extra arguments
        self.add_extra_args()
        ## add scan_hw arguments
        self.add_scan_hw_args()
        ## add scan_sysconf arguments
        self.add_scan_sysconf_args()
        ## add scan_rpm arguments
        self.add_scan_rpms_args()
        ## set default function
        self.set_func()

    def set_func(self) -> None:
        self.scan_hw_parser.set_defaults(func=self.scan_hw)
        self.scan_sysconf_parser.set_defaults(func=self.scan_sysconf)
        self.scan_rpms_parser.set_defaults(func=self.scan_rpms)
        self.export_sysconf_parser.set_defaults(func=self.export_sysconf)
        self.export_sysconf_server_parser.set_defaults(
            func=self.export_sysconf_server)

    def scan_hw(self, args) -> None:
        # TODO: 统一各个扫描功能的输出文件命名； 增加输出与之匹配的 HTML 功能
        # 或许输出文件名未必统一？因为反正 HTML 里面引用的资源文件名都随便写了。。。
        # 这样的话还方便用户识别
        generate_comtatibility_list_js()

    def scan_sysconf(self, args) -> None:
        ScanConf().run(args)

    def scan_rpms(self, args) -> None:
        generate_rpm_list_js()

    def export_sysconf(self, args) -> None:
        ExportSysConf().run(args)

    def export_sysconf_server(self, args) -> None:
        start_server()

    def add_scan_hw_args(self) -> None:
        pass

    def add_scan_sysconf_args(self) -> None:
        pass

    def add_scan_rpms_args(self) -> None:
        pass

    def add_extra_args(self) -> None:
        self.parser.add_argument(
            '-v',
            '--version',
            action='version',
            version=__version__,
        )

    def run(self) -> None:
        """
        Run the CLI
        """
        try:
            args = self.parser.parse_args()
        except Exception as e:
            logging.error(e)
            self.parser.print_help()
            sys.exit(1)

        if hasattr(args, 'func'):
            args.func(args)
        else:
            self.parser.print_help()
            sys.exit(1)


if __name__ == "__main__":
    cli = Cli()
    cli.run()
