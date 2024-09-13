#!/usr/bin/env python3
# coding=utf-8
import os
import subprocess

from mig_merge.migrationTools.utils.logger import Logger

logger = Logger(__name__)


def run_cmd(cmd=""):
    '''
    description:  run shell cmd
    param {}
    return {*}
    '''
    os.putenv('LANG', 'C.UTF-8')
    os.putenv('LC_ALL', 'C.UTF-8')
    os.environ['LANG'] = 'C.UTF-8'
    os.environ['LC_ALL'] = 'C.UTF-8'

    cmd = cmd.encode('utf-8')
    pip_env = os.environ
    if 'LD_LIBRARY_PATH' in pip_env:
        pip_env.pop('LD_LIBRARY_PATH')
    proc = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=pip_env,
    )
    stdout, stderr = proc.communicate()
    stdout = stdout.decode(encoding='utf-8')
    stderr = stderr.decode(encoding='utf-8')
    returncode = proc.returncode

    return returncode, stdout.split('\n'), stderr


def get_valid_lines(lines):
    '''
    Remove lines that are meaningless or have no content.

    Args:
        lines(list): input content

    Returns:
        list: valid lines
    '''
    valid_lines = list()
    lines = list(lines)
    for line in lines:
        ## 先去除无用的空格
        line = line.strip()
        ## 过滤注释
        if line.startswith('#'):
            continue
        ## 过滤空行
        if line == "":
            continue

        valid_lines.append(line)

    return valid_lines


def systemd_escape_lines(lines):
    '''
    returns lines with escaped characters.

    Args:
        lines(list): input content

    Returns:
        list: valid lines
    '''
    valid_lines = list()
    lines = list(lines)
    for line in lines:
        if '\\x2d' in line:
            logger.debug(f"systemd escape line: {line}")
            line = line.replace('\\x2d', '-')
        valid_lines.append(line)

    return valid_lines
