#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import os
import platform
import shutil
import subprocess as sup

from sysmig_agent.migrationTools.scanRPM.db_operates import DBOperate
from sysmig_agent.migrationTools.utils.config import PathConf
from sysmig_agent.migrationTools.utils.logger import Logger
import sysmig_agent.migrationTools.utils.html as html

logger = Logger(__name__)
'''
    TODO:
    - Provides 对比，最好可以筛选
    - 给出系统间包总数对比
    - 【部分完成，增加了 is_version_leaped 字段】版本跳跃展示（往牛逼了做可能可以做 abidiff）

    - 其实如果需要，应该也可以做个进度条。。。

'''


class ProvideMapItem(object):
    ''' 每个包中每一项 provide 的对比结构

    Attributes:
        origin_provide: dict， 包括当前系统上的 provide 的名称和版本
        uos_pkg_provide： dict， 与当前系统上的 provide 对应的， uos 提供的包的 provide 名称和版本
        uos_pkg_key: int， uos 中的包 pkgKey， 内部匹配用，无需输出
        uos_pkg_name: str, 提供该 provide 的 uos 上的包名
    '''
    def __init__(self):
        self.origin_provide = {'p': None, 'v': None}  # p: provide,  v: version
        self.uos_pkg_provide = {'p': None, 'v': None}
        self.uos_pkg_key = 0
        self.uos_pkg_name = None


class ParsedPkgInfo(object):
    ''' 解析后的每个包的信息

    Attributes:
        pkg_name: str， 当前系统（待迁移系统）上该包的包名
        is_version_leaped: bool, 标记该包在当前系统和 uos 中的版本变化是否较大。只要所有 provide 中有
                           任意一项的 provide 大版本（版本号第一位数字）不同，则为 True
        pkg_provides_map: list, 当前系统（待迁移系统）上该包每个 provide 到 uos 上的 provide 的映射关系 list 。
                          每个 provide 都将被描述，该 list 中的元素是 ProvideMapItem 实例
    '''
    def __init__(self, pkg_name: str, add_tags: bool = True):
        self.pkg_name = pkg_name
        self.is_version_leaped = True
        self.tags = []
        self.pkg_provides_map = []

        self.fill_provides_item()

    def fill_provides_item(self):
        ''' 填充当前包的信息（填充本类中的各个属性）
        '''
        provides_tuple_list = get_pkg_provides_by_name(self.pkg_name)

        if PathConf.arch == "aarch64":
            repodb_path = PathConf.data_path + "/repo-sqlite/uos-1020e/aarch64/63ab13615c7e35a77bfb0719b6c2af5c4298a609132950963f4a0ea99b341112-primary.sqlite"
        elif PathConf.arch == "x86_64":
            repodb_path = PathConf.data_path + "/repo-sqlite/uos-1020e/x86_64/2ad7cabc63634d5c75336929453bf9ff2054434547844df0c279c4759cd05409-primary.sqlite"

        with DBOperate(repodb_path) as db:
            for provide_tuple in provides_tuple_list:
                tmp_provide_map_item = ProvideMapItem()
                tmp_provide_map_item.origin_provide = provide_tuple

                db.execute_sql("select * from provides where name='" +
                               provide_tuple['p'] + "'")
                for row in db.cursor:  # 实际上，由于 provide 名是唯一的，若有结果也一定是 1 。若为 0 则直接重新开始循环
                    tmp_uos_pkg_provide_tuple = {}
                    # tmp_uos_pkg_provide_tuple['p'] = row[0]
                    if provide_tuple['p'] == row[0]:
                        tmp_uos_pkg_provide_tuple[
                            'p'] = 1  # 反正都存在了那么名字肯定完全相同，直接输出 1，否则 0
                    else:  # 语意化交给前端去做
                        tmp_uos_pkg_provide_tuple['p'] = 0
                    if provide_tuple['v'] != None and row[3] != None:
                        tmp_uos_pkg_provide_tuple['v'] = row[3]
                        if provide_tuple['v'][0] == tmp_uos_pkg_provide_tuple[
                                'v'][0]:
                            self.is_version_leaped = False
                    else:
                        tmp_uos_pkg_provide_tuple['v'] = None
                    tmp_provide_map_item.uos_pkg_provide = tmp_uos_pkg_provide_tuple
                    tmp_provide_map_item.uos_pkg_key = row[5]

                db.execute_sql("select * from packages where pkgKey=" +
                               str(tmp_provide_map_item.uos_pkg_key) + "")
                for row in db.cursor:
                    # 把版本信息添加了:  %{name}-%{version}.%{release}
                    tmp_provide_map_item.uos_pkg_name = row[2] + "-" + row[
                        4] + "." + row[6]

                self.pkg_provides_map.append(tmp_provide_map_item)

        provide_exist = False
        for provide_map_item in self.pkg_provides_map:  # 先过滤一遍，看 provide 列表中是否存在我们提供了的
            if provide_map_item.uos_pkg_provide['p'] == 1:
                provide_exist = True
                break
        if not provide_exist:  # 只要有一个就会为 True，如果 False 就是根本不存在 provide 的，即完全没提供
            self.tags.append("Nothing provided")
        else:  # 如果存在我们提供了的，再看一下是不是完全提供了
            provide_all = True
            for provide_map_item in self.pkg_provides_map:
                if provide_map_item.uos_pkg_provide[
                        'p'] == None or provide_map_item.uos_pkg_provide[
                            'p'] == 0:
                    provide_all = False
                    break
            if provide_all:
                self.tags.append("All provided")
            else:
                self.tags.append("Partially provided")
            if self.is_version_leaped:
                self.tags.append("Version leaped")


def get_current_pkg_list() -> list:
    ''' 获取当前（运行该程序的）系统上所有已安装的 rpm 包的列表

    列表通过 yum list installed 获取

    Returns:
        由本系统上已装包的组成的列表，每项是一个软件包名
        例如： ['yelp-libs', 'yelp-tools', 'yelp-xsl', 'yum', 'zenity', 'zip', 'zlib']
    '''
    current_pkgs = []
    get_pkgs_proc = sup.run('rpm -qa -q --qf "%{name}\n"',
                            shell=True,
                            stdout=sup.PIPE,
                            env={"LANG": "en_US.UTF-8"})
    output = get_pkgs_proc.stdout.decode("utf-8")[:-1]
    current_pkgs = output.split("\n")

    for i in range(0, len(current_pkgs)):
        get_full_name_proc = sup.run("rpm -q " + current_pkgs[i],
                                     shell=True,
                                     stdout=sup.PIPE,
                                     env={"LANG": "en_US.UTF-8"})
        output = get_full_name_proc.stdout.decode("utf-8")[0:-1]
        if "\n" in output:  # 如果同一个名字对应了超过一个包（常见于多个 kernel 相关包，一个包会有多个版本），要进入一个针对这些包进行分类的小循环
            same_name_pkgs = output.split("\n")
            for same_name_pkg in same_name_pkgs:
                current_pkgs[i] = same_name_pkg
                i += 1
            continue
        current_pkgs[i] = output  # 如果一个名字只对应了一个包，直接赋值即可

    return current_pkgs


def get_pkg_provides_by_name(pkg_name: str) -> list:
    ''' 根据包名 pkg_name 获取当前系统上该包的 provides

    Args:
        pkg_name: 当前系统上要获取 provides 列表的包名

    Returns：
        存储了 pkg_name 包的 provides 的列表， 列表中的每一项都是一个 tuple,
        例如： {'p': 'anaconda-core', 'v': '33.16.3.26'}
    '''
    provides_list_orig = []
    get_provides_proc = sup.run(["rpm", "-q", "--provides", pkg_name],
                                stdout=sup.PIPE,
                                env={"LANG": "en_US.UTF-8"})
    output = get_provides_proc.stdout.decode("utf-8")
    provides_list_orig = output[:-1].split("\n")

    provides_list = []
    # 所有的过滤都可以在这里进行
    for provide in provides_list_orig:
        # "(x86_64)" in provide or "(aarch-64)" in provide or \ 这两个考虑去掉。
        # 因为对于包 NetworkManager 而言，NetworkManager-dispatcher(aarch-64) 确实没提供，
        # 而且也确实没有名为 NetworkManager-dispatcher 的 provide
        if  "application()" in provide or \
            "metainfo()" in provide or \
            "mimehandler(" in provide:
            continue
        provides_list.append(provide)

    provides_tuple_list = []

    for provide in provides_list:
        provide_item = {}
        if " = " in provide:
            epoch_version_release = provide[provide.find(' = ') +
                                            3:len(provide)]
            version_release = epoch_version_release
            if ':' in epoch_version_release:
                version_release = epoch_version_release[
                    epoch_version_release.find(':') +
                    1:len(epoch_version_release)]
            if '-' in version_release:
                version = version_release[0:version_release.find('-')]
            else:
                version = version_release
            provide_item = {'p': provide[0:provide.find(' = ')], 'v': version}
        else:
            provide_item = {'p': provide, 'v': None}
        provides_tuple_list.append(provide_item)

    return provides_tuple_list


def parsed_pkg_to_json(parsed_pkgs: list) -> str:
    ''' 将解析后的包列表对象转为 json 字符串并返回

    由于嵌套结构中包含自定义类，所以只能手搓一个转换器
    '''
    json_str = '['
    for pkg in parsed_pkgs:
        logger.debug(pkg.pkg_name)
        json_str += '{'
        pn = '"pn": "' + pkg.pkg_name + '",'
        json_str += pn  # pn: pkg_name
        json_str += '"vl": '  # vl: is_version_leaped
        if pkg.is_version_leaped:
            json_str += 'true,'
        else:
            json_str += 'false,'
        json_str += '"tags": ' + json.dumps(pkg.tags) + ','
        json_str += '"ppm": '  # ppm: pkg_provides_map
        json_str += '['
        for provide_map_item in pkg.pkg_provides_map:
            json_str += '{'
            # upn: uos_pkg_name
            json_str += '"upn": "' + str(provide_map_item.uos_pkg_name) + '",'
            # op: origin_provide
            json_str += '"op": ' + json.dumps(
                provide_map_item.origin_provide) + ','
            # upp: uos_pkg_provide
            json_str += '"upp": ' + json.dumps(
                provide_map_item.uos_pkg_provide)
            json_str += '},'
        json_str = json_str.strip(',')
        json_str += ']},'
    json_str = json_str.strip(',')
    json_str += ']'
    return json_str


def scan_rpms(output_json_filename: str,
              only_show_leap=True,
              exclude_fonts=True,
              exclude_kernel_modules=True,
              add_tags=True):
    ''' 扫描 RPM 包，直接输出 json 文件

    Args:
        output_json_filename: 输出的文件名，包括目录
        only_show_leap： 是否只输出大版本变化的包
        exclude_fonts： 是否排除字体类包
        exclude_kernel_modules： 是否排除 kernel-modules 包
    '''
    parsed_pkgs = []
    installed_pkgs = get_current_pkg_list()

    if exclude_fonts:
        filted_installed_pkgs = []
        for pkg in installed_pkgs:
            if 'fonts' in pkg:
                continue
            filted_installed_pkgs.append(pkg)
        installed_pkgs = filted_installed_pkgs

    if exclude_kernel_modules:
        filted_installed_pkgs = []
        for pkg in installed_pkgs:
            if 'kernel-modules' in pkg:
                continue
            filted_installed_pkgs.append(pkg)
        installed_pkgs = filted_installed_pkgs

    for pkg_name in installed_pkgs:
        tmp_pkg_info = ParsedPkgInfo(pkg_name, add_tags)
        parsed_pkgs.append(tmp_pkg_info)

    if only_show_leap:
        filted_pkgs = []
        for pkg in parsed_pkgs:
            if pkg.is_version_leaped:
                filted_pkgs.append(pkg)
        parsed_pkgs = filted_pkgs

    json_str = parsed_pkg_to_json(parsed_pkgs)

    current_OS = platform.linux_distribution(
    )[0] + " " + platform.linux_distribution()[1]

    target_OS = "UnionTech OS Server 20"

    try:
        of = open(output_json_filename, mode='w')
        of.write('utmt_report_mode="rpmscan";\n')
        of.write('ut_current_system_info = { system: "' + current_OS + '", ' +
                 'targetOS: "' + target_OS + '"};\n')
        of.write('utmt_report_data=`' + json_str + '`')
    except OSError as e:
        print(e)
    finally:
        of.close()


def generate_rpm_list_js():
    report_dir = PathConf.report_dir

    report_name = f"rpm_info_report_{PathConf.timestamp}"
    ## 拷贝模板文件时， 会自动创建 report/datafile 目录
    html.copy_html_resource()
    datafiledir = os.path.join(report_dir, "datafile")
    if not os.path.exists(datafiledir):
        os.makedirs(datafiledir)

    # js
    jsfile_path = os.path.join(report_dir, 'datafile', f"{report_name}.js")
    # 对应的入口 html
    html_path = os.path.join(report_dir, f"{report_name}.html")

    html_document = html.gen_html_template(report_name)

    scan_rpms(jsfile_path,
              only_show_leap=False,
              exclude_fonts=False,
              exclude_kernel_modules=False)

    scanrpms_html_file = open(html_path, 'w')

    with scanrpms_html_file:
        scanrpms_html_file.write(html_document)
        logger.info(f"report has been generated: {html_path}.")


def main():

    scan_rpms("./jsonoutput.json",
              only_show_leap=False,
              exclude_fonts=False,
              exclude_kernel_modules=False)


if __name__ == "__main__":
    main()
