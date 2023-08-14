from flask import *
import os

from client_requests import *
from func.utils import *

def check_services(data, url):
    info = post_client_data(data, url)
    if info is None or info.status_code != 200:
        print("请求失败,客户端没有启动")
        return list_to_json(['res', 'error'], ['1', '迁移客户端没有启动'])
    else:
        return info.text


def check_environment(data):
    services = check_services(data, '/check_environment')
    if services:
        return services


def check_os(data):
    services = check_services(data, '/check_os')
    if services:
        return services

def check_storage(data):
    services = check_services(data, '/check_storage')
    if services:
        return services

def close_tool(data):
    os.system('kill -9 `ps -ef | grep "start_webview.py" | grep -v grep | awk \'{print $2}\'`')
    data = {"ip": "0.0.0.0"}
    data_json = json.dumps(data)
    return data_json

def check_user(data):
    services = check_services(data, '/check_user')
    if services:
        return services

def check_repo(data):
    services = check_services(data, '/check_repo')
    if services:
        return services


def check_os_kernel(data):
    services = check_services(data, '/check_os_kernel')
    if services:
        return services


def check_repo_kernel(data):
    services = check_services(data, '/check_repo_kernel')
    if services:
        return services


def check_progress(data):
    services = check_services(data, '/check_progress')
    if services:
        return services


def export_migration_reports(data):
    services = check_services(data, '/export_migration_reports')
    if services:
        return services


def system_migration(data):
    services = check_services(data, '/system_migration')
    if services:
        return services