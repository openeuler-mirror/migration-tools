import webview
import json
from func.share import getSysMigConf

uos_sysmig_conf = json.loads(getSysMigConf())
ip = json.loads(uos_sysmig_conf).get('serverip').strip()[1:-1]
port = int(json.loads(uos_sysmig_conf).get('serverport').strip()[1:-1])
url = 'http://%s' % ip + ':%s' % port
title = '统信服务器系统迁移软件'
webview.create_window(title, url, width=1200, height=525)
webview.start()

