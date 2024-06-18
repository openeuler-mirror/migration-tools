#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import platform

from config import FixedInfo
from logger import migration_log


from stock_replace.general_tabs import general_tabs
from stock_replace.packages_tabs import packages_tabs
from stock_replace.rpm_tabs import rpm_tabs

from new_expansion.hardware_tabs import hardware_tabs
from new_expansion.confscan_tabs import confscan_tabs
from new_expansion.rpmscan_tabs import rpmscan_tabs
from new_expansion.sysconffile_tabs import sysconffile_tabs

def MigrationMerge():
    return general_tabs()+packages_tabs()+rpm_tabs()+hardware_tabs()+confscan_tabs()+rpmscan_tabs()+sysconffile_tabs()

def main():
    print(MigrationMerge())

if __name__ == "__main__":
    main()

