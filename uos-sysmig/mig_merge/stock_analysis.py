#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

#for test
sys.path.append("..")

import mig_merge.stock_replace.confirm as confirm 
from sysmig_agent.migrationTools.utils.logger import Logger


logger = Logger(__name__)

def stock_replace_analysis():
    '''
        应用场景：存量替换迁移分析-软件包对比
        功    能：迁移前、后软件包对比
        输入参数：无
        返 回 值：success
    '''

    if confirm.migration_confirm():
        print('0000000')


def main():
    stock_replace_analysis()


if __name__ == "__main__":
    main()

