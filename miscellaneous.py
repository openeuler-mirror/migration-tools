# -*- coding: utf-8 -*-
# !/usr/bin/python
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier:   MulanPubL-2.0-or-later
import os
import json
import re
import socket
#os.chdir('/usr/lib/uos-sysmig-server')
from logger import *


migration_log = Logger('/var/tmp/uos-migration/migration.log', logging.DEBUG, logging.DEBUG)


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        return ip
    finally:
        s.close()


def list_to_json(keylist, valuelist):
    res = dict(zip(keylist, valuelist))
    res = json.dumps(res)
    migration_log.info(res)
    return json.dumps(res)


def getSysMigConf(local_ip):
    confpath = '/etc/uos-sysmig/uos-sysmig.conf'
    if not os.path.exists(confpath):
        return None
    else:
        db_name = db_password = db_user = cfid = agentip = serverip = agentport = serverport = baseurl = cftype = agentdatabase_ip = serverdatabase_ip = agentdatabase_port = serverdatabase_port = ''
        server = None
        skip = 0
        with open(confpath, 'r') as cf:
            for line in cf:
                line = line.strip().strip('\n')
                if not line:
                    continue
                if re.search('\[Agent\]', line):
                    server = 0
                    skip = 0
                    continue
                if skip != 0:
                    continue
                if '#' in line:
                    continue
                elif re.search('\[Server\]', line):
                    server = 1
                    continue
                else:
                    p = ret = ''
                    if re.match('\=', line):
                        continue
                    else:
                        p, ret = line.split('=', 1)
                    p = p.strip()
                    if re.fullmatch('ID', p):
                        cfid = ret.strip()
                    if re.fullmatch('IP', p):
                        sip = str(ret).strip()
                        if 0 == server:
                            ip = sip.split('"',-1)[1]
                            if ip != local_ip:
                                skip = 1
                                continue
                            agentip = str(ret).strip()
                        else:
                            serverip = str(ret).strip()
                    if re.fullmatch('PORT', p):
                        if 0 == server:
                            agentport = ret.strip()
                        else:
                            serverport = ret.strip()
                    if re.search('BASEURL', p):
                        baseurl = ret.strip()
                    if re.search('TYPE', p):
                        cftype = ret.strip()
                    if re.search('DATABASE_IP', p):
                        if 0 == server:
                            agentdatabase_ip = ret.strip()
                        else:
                            serverdatabase_ip = ret.strip()
                    if re.search('DATABASE_PORT', p):
                        if 0 == server:
                            agentdatabase_port = ret.strip()
                        else:
                            serverdatabase_port = ret.strip()
                    if re.search('DB_NAME', p):
                        if 0 == server:
                            db_name = ret.strip()
                        else:
                            db_name = ret.strip()
                    if re.search('DB_PASSWORD', p):
                        if 0 == server:
                            db_password = ret.strip()
                        else:
                            db_password = ret.strip()
                    if re.search('DB_USER', p):
                        if 0 == server:
                            db_user = ret.strip()
                        else:
                            db_user = ret.strip()
        cf.close()
        keylist = ['id', 'agentip', 'serverip', 'agentport', 'serverport', 'baseurl', 'type', 'agentdatabase_ip',
                   'serverdatabase_ip', 'agentdatabase_port', 'serverdatabase_port', 'db_name', 'db_password', 'db_user']
        valuelist = [cfid, agentip, serverip, agentport, serverport, baseurl, cftype, agentdatabase_ip,
                     serverdatabase_ip, agentdatabase_port, serverdatabase_port, db_name, db_password, db_user]
        return list_to_json(keylist, valuelist)

