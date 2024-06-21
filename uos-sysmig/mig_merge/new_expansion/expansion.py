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

from mig_merge.new_expansion.hardware_tabs import hardware_tabs
from mig_merge.new_expansion.confscan_tabs import confscan_tabs
from mig_merge.new_expansion.rpmscan_tabs import rpmscan_tabs
from mig_merge.new_expansion.sysconffile_tabs import sysconffile_tabs

def MigrationMerge():
    #return sysconffile_tabs()+hardware_tabs()+confscan_tabs()+rpmscan_tabs()+general_tabs('E')+packages_tabs()+rpm_tabs().rsplit(',',1)[0]+'}'
    return general_tabs('E')+packages_tabs()+rpm_tabs()+hardware_tabs()+confscan_tabs()+rpmscan_tabs()+sysconffile_tabs()+'}'

if __name__ == "__main__":
   MigrationMerge()

