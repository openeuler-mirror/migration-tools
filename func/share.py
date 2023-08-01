import os
import sys
import re

from func.utils import list_to_json

def getSysMigConf():
    confpath = '/etc/uos-sysmig/uos-sysmig.conf'
    if not os.path.exists(confpath):
        return None
    else:
        cfid=agentip=serverip=agentport=serverport=baseurl=cftype=agentdatabase_ip=serverdatabase_ip=agentdatabase_port=serverdatabase_port=''
        server = None
        with open(confpath,'r') as cf:
            for line in cf:
                line = line.strip().strip('\n')
                if not line:
                    continue
                if re.search('\[Agent\]',line):
                    server=0
                    continue
                elif re.search('\[Server\]',line):
                    server = None
                    continue
                else:
                    p=ret=''
                    if re.match('\=',line):
                        continue
                    else:
                        p,ret=line.split('=',1)
                    p = p.strip()
                    if re.fullmatch('ID',p):
                        cfid = ret.strip()
                    if re.fullmatch('IP',p):
                        if 0 == server:
                            agentip = str(ret).strip()
                        else:
                            serverip = str(ret).strip()
                    if re.fullmatch('PORT',p):
                        if 0 == server:
                            agentport = ret.strip()
                        else:
                            serverport = ret.strip()
                    if re.search('BASEURL',p):
                        baseurl = ret.strip()
                    if re.search('TYPE',p):
                        cftype = ret.strip()
                    if re.search('DATABASE_IP',p):
                        if 0 == server:
                            agentdatabase_ip = ret.strip()
                        else:
                            serverdatabase_ip = ret.strip()
                    if re.search('DATABASE_PORT',p):
                        if 0 == server:
                            agentdatabase_port = ret.strip()
                        else:
                            serverdatabase_port = ret.strip()
        cf.close()
        keylist = ['id','agentip','serverip','agentport','serverport','baseurl','type','agentdatabase_ip','serverdatabase_ip','agentdatabase_port','serverdatabase_port']
        valuelist = [cfid,agentip,serverip,agentport,serverport,baseurl,cftype,agentdatabase_ip,serverdatabase_ip,agentdatabase_port,serverdatabase_port]
        return list_to_json(keylist,valuelist)