# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier:   MulanPubL-2.0-or-later

import webview
import json
import os
from sysmig_agent.share import getSysMigConf
uos_sysmig_conf = json.loads(getSysMigConf())
ip = json.loads(uos_sysmig_conf).get('serverip').strip()[1:-1]
port_os = os.popen('systemctl status uos-sysmig-data.service | grep "Network"')
port = port_os.readlines()[0][-6:-2]
url = 'http://%s' % ip + ':%s' % port
title = '统信服务器系统迁移软件'
webview.create_window(title, url, fullscreen=True, frameless=True)
webview.start()
