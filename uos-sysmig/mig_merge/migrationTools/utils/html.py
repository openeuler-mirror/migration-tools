#!/bin/python3
import os
from re import L
import shutil
import fcntl
import time
from mig_merge.migrationTools.utils.config import PathConf



def gen_html_template(datapath: str) -> str:
    # 拼接 HTML
    html_template = PathConf.report_template_file
    with open(html_template, 'r', encoding='utf-8') as f:
        template_str = f.read()

    result_js = os.path.basename(datapath)
    if result_js.endswith('.js'):
        html = template_str.replace('/datafile/scanresult.js',
                                    './datafile/' + result_js)
    else:
        html = template_str.replace('/datafile/scanresult.js',
                                    f'./datafile/{result_js}.js')
    html = html.replace('="/css', '="./resource/css')
    html = html.replace('="/js', '="./resource/js')

    return html

class LockDirectory(object):
    def __init__(self, directory):
        assert os.path.exists(directory)
        self.directory = directory

    def __enter__(self):
        self.dir_fd = os.open(self.directory, os.O_RDONLY)
        try:
            fcntl.flock(self.dir_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except IOError as ex:
            time.sleep(10)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # fcntl.flock(self.dir_fd,fcntl.LOCK_UN)
        os.close(self.dir_fd)

def copy_html_resource():
    # 拷贝资源文件
    resource_dir = os.path.join(PathConf.data_path, "report-template",
                                'resource')
    dst_dir = os.path.join(PathConf.report_dir, "resource")
    if not os.path.exists(PathConf.report_dir):
        os.makedirs(PathConf.report_dir)
    with LockDirectory(PathConf.report_dir) as lock:
        if os.path.exists(dst_dir):
            shutil.rmtree(dst_dir)
        shutil.copytree(resource_dir, dst_dir)
