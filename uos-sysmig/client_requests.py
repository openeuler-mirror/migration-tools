# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier:   MulanPubL-2.0-or-later
import json
import requests
from sysmig_agent.share import getSysMigConf


uos_sysmig_conf = json.loads(getSysMigConf())
ip = json.loads(uos_sysmig_conf).get('agentip').strip()[1:-1]
port = int(json.loads(uos_sysmig_conf).get('agentport').strip()[1:-1])

headers = {'content-type': 'application/json'}


class PostIntranetIP:
    def __init__(self, url, data):
        self.url = url
        self.data = data

    def post_intranet_ip(self):
        try:
            r = requests.post(url=self.url, data=self.data, headers=headers) 
        except:
            r = None

        return r


def post_client_data(data, mod, url=ip):
    post_url = "http://" + url + ":" + str(port) + mod
    post_data = PostIntranetIP(post_url, data)

    return post_data.post_intranet_ip()
