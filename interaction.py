import requests
import json
from sysmig_agent.share import getSysMigConf

headers = {'content-type': 'application/json'}

class Interaction:
    def __init__(self, url, data):
        self.url = url
        self.data = data

    def send_post_requests(self):
        try:
            r = requests.post(url=self.url, data=self.data, headers=headers, timeout=10) 
        except:
            r = None
        return r


def splice_url(data, url, ip):
    uos_sysmig_conf = json.loads(getSysMigConf(ip))
    port = json.loads(uos_sysmig_conf).get('agentport').strip()[1:-1]
    post_url = "http://" + ip + ":" + port + url
    data = Interaction(post_url, data)
    return data.send_post_requests()