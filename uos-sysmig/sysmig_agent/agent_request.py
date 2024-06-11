# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier:   MulanPubL-2.0-or-later

import requests
import json
from sysmig_agent.share import getSysMigConf ,json_list_to_json, sql_online_statue

uos_sysmig_conf = json.loads(getSysMigConf())
ip = json.loads(uos_sysmig_conf).get('serverip').strip()[1:-1]
port = int(json.loads(uos_sysmig_conf).get('serverport').strip()[1:-1])
mod_sql = '/sql_task'

headers = {'content-type': 'application/json'}


class PostIntranetIP:
    def __init__(self, url, data):
        self.url = url
        self.data = data

    def post_intranetip(self):
        try:
            r = requests.post(url=self.url, data=self.data, headers=headers)
        except:
            r = None
        return r


def post_client_data(data):
    post_url = "http://" + ip + ":" + str(port) + mod_sql
    print('______>post:'+post_url+'\n____> data: '+str(data) +'ip port '+ip+str(port))
    post_data = PostIntranetIP(post_url, data)
    return post_data.post_intranetip()


def post_server(statue, task_id):
    keylist = ['mod','statue','task_id']
    valuelist = ['sql_task',statue,str(task_id)]
    data =  json_list_to_json(keylist,valuelist)

#    data={"mod":"sql_task", "statue": "task_start", "task_id":2}
    t = post_client_data(data)
    print("requires post return code :"+str(t))
    f = 0
    if not t or t.status_code != 200:
        t = post_client_data(data)
        sql_online_statue(1, task_id)
    else:
        sql_online_statue(0, task_id)
