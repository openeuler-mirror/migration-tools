#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import platform

from mig_merge.config import FixedInfo
from logger import migration_log


from mig_merge.stock_replace.general_tabs import general_tabs
from mig_merge.stock_replace.packages_tabs import packages_tabs
from mig_merge.stock_replace.rpm_tabs import rpm_tabs
from mig_merge.stock_replace.rpmscan_tabs import rpmscan_tabs
from mig_merge.stock_replace.sysconffile_tabs import sysconffile_tabs

from mig_merge.new_expansion.hardware_tabs import hardware_tabs
from mig_merge.new_expansion.confscan_tabs import confscan_tabs

def MigrationMerge(log, my_query, my_status):

    expansion_json_data = ''
    #expansion_json_data = general_tabs('E', log)+packages_tabs()+\
    #        rpm_tabs('E')+hardware_tabs()+confscan_tabs()+\
    #        rpmscan_tabs('E', log)+','+sysconffile_tabs()+'}'

    expansion_json_data = expansion_json_data + general_tabs('E', log)
    msg_tup = ('13', my_status)
    my_query.put(msg_tup)

    expansion_json_data = expansion_json_data + packages_tabs()
    msg_tup = ('25', my_status)
    my_query.put(msg_tup)

    expansion_json_data = expansion_json_data + rpm_tabs('E')
    msg_tup = ('33', my_status)
    my_query.put(msg_tup)

    expansion_json_data = expansion_json_data + hardware_tabs()
    msg_tup = ('57', my_status)
    my_query.put(msg_tup)

    expansion_json_data = expansion_json_data + confscan_tabs()
    msg_tup = ('74', my_status)
    my_query.put(msg_tup)

    expansion_json_data = expansion_json_data + rpmscan_tabs('E', log)+','
    msg_tup = ('89', my_status)
    my_query.put(msg_tup)

    expansion_json_data = expansion_json_data + sysconffile_tabs()+'}'
    msg_tup = ('93', my_status)
    my_query.put(msg_tup)

    log.info('new expansion check json data:{}'.format(expansion_json_data))
    return expansion_json_data

if __name__ == "__main__":
   MigrationMerge()

