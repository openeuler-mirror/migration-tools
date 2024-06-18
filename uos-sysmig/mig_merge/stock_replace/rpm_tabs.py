import os
import sys
import json
import socket
from shutil import copyfile

from logger import migration_log
from migrationTools.scanHardware import utils
from stock_replace.confirm import get_cur_sys_version
from config import FixedInfo

def rpm_tabs():
    '''
        应用场景：存量替换迁移检查-RPM兼容性对比
        功    能：1xxxa版RPM兼容性对比，按照前后端接口生成json格式的RPM兼容性检查数据
        输入参数：无
        返 回 值：json数据
    '''

    third_tab = ''
    rpm_file_name = FixedInfo.inventory_dir + '/abi-incomp-chk.csv'
    for line in open(rpm_file_name, 'r'):
        element_list = line.strip().split(',', 6)
        if element_list[4] == 'N':
            compatible = 'false'
            element = '{"name":"'+element_list[0]+\
                    '","is_compatible": '+compatible+\
                    ',"current_version": "'+element_list[2]+\
                    '","future_version": "'+element_list[3]+\
                    '","incompatible_type": "'+element_list[5]+\
                    '","incompatible_source": "'+element_list[1]+\
                    '","description": "'+element_list[6]+'"},'
        else:
            compatible = 'true'
            element = '{"name":"'+element_list[0]+\
                    '","is_compatible": '+compatible+'},'
        third_tab = third_tab + element
    #migration_log.info('Get rpm packages info:{}'.format(third_tab))
    return FixedInfo.page_rpm_tabs +third_tab.rsplit(',',1)[0]+']}},'

def main():
    rpm_tabs()


if __name__ == "__main__":
    main()

