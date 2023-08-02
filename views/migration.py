from flask import *

from client_requests import *
from func.utils import *

def check_services(data, url):
    info = post_client_data(data, url)
    if info is None or info.status_code != 200:
        migration_log.error("请求失败,客户端没有启动")
        return list_to_json(['res', 'error'], ['1', '迁移客户端没有启动'])
    else:
        return info.text