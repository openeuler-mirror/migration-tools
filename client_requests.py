import json
import requests

from func.share import getSysMigConf


uos_sysmig_conf = json.loads(getSysMigConf())
ip = json.loads(uos_sysmig_conf).get('agentip').strip()[1:-1]
port = int(json.loads(uos_sysmig_conf).get('agentport').strip()[1:-1])

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


