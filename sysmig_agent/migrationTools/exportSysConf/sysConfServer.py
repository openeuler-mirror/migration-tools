#!/usr/bin/python3
#! -*- coding: utf-8 -*-

from flask import Flask, jsonify
from flask import request, make_response
from flask import send_from_directory
from gevent.pywsgi import WSGIServer
import platform, os, sys, shutil, socket
import tarfile
import json

server_ip = ""
server_port = 5000

## enter exportSysConf dir
_curdir = os.path.abspath(os.getcwd())
__base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(__base_path)
os.chdir("exportSysConf")


def create_tar(dir_name: str, folder_name: str, output_filename: str):
    """ 创建 tar.gz 包
    将 dir_name 中的所有文件装进 arcname 文件夹，并输出包到 output_filename

    Args:
        dir_name: 要被压缩的目录，如 /root/utmtc-confdiff/server
        arcname: 被打进 tar 包的最外层文件夹名
        output_filename：输出的文件，要包含目录，如：/root/serverTar.tar.gz
    """
    try:
        tar = tarfile.open(output_filename, "w:gz")
        tar.add(dir_name, arcname=folder_name)
        tar.close()
    except Exception as e:
        print(e)
        raise IOError("tarball compress error")


def create_app():
    global server_port

    app = Flask(__name__)

    @app.route('/')
    def return_main_page():
        """ 返回 index.html 的内容文本，并动态修改文本中的服务器 Endpoint
        """

        with open('./static/index.html') as f:
            index_template = f.read()
        index_template = index_template.replace(
            '10.7.35.161:5000', (request.headers.get('Host').split(':')[0] +
                                 ":" + str(server_port)))
        return index_template

    @app.route('/js/<javascript_file_name>')
    def return_js_file(javascript_file_name):
        """ 响应浏览器的 js 资源请求
        """
        return app.send_static_file('js/' + javascript_file_name)

    @app.route('/css/<css_file_name>')
    def return_css_file(css_file_name):
        """ 响应浏览器的 css 资源请求
        """
        return app.send_static_file('css/' + css_file_name)

    @app.route('/img/<img_file_name>')
    def return_img_file(img_file_name):
        """ 响应浏览器的图像资源请求
        """
        return app.send_static_file('img/' + img_file_name)

    @app.route('/api/getSysInfo', methods=['GET'])
    def get_sys_info():
        """ 获取当前系统版本、机器架构信息
        """
        sysinfo = {
            'system':
            platform.linux_distribution()[0] + ' ' +
            platform.linux_distribution()[1],
            'arch':
            platform.machine()
        }
        response = make_response(jsonify(sysinfo))
        response.headers['Access-Control-Allow-Origin'] = "*"
        return response

    @app.route('/api/getDiffGroups', methods=['GET'])
    def get_diff_groups():
        """ 获取 diff 列表

        目前的数据全是调试用的假数据，稍后在代码合并时，需要直接从数据收集模块的 json 文件中读取
        """
        diff_groups = []
        with open('/var/tmp/utmtc/exportsysconf/exportsysconf.json') as f:
            diff_groups = json.load(f)

        for diff_group in diff_groups:
            for conf_item in diff_group['confList']:
                diff_content = ''
                with open(conf_item['diff']) as diff_file:
                    diff_content = diff_file.read()
                    conf_item['diffContent'] = diff_content

        response = make_response(jsonify(diff_groups))
        response.headers['Access-Control-Allow-Origin'] = "*"
        return response

    @app.route('/api/getConfDetail', methods=['GET'])
    def get_conf_detail():
        pass

    @app.route('/api/downloadConfDiff/<filename>')
    def download_conf_diff(filename):
        """ 根据 conf 的文件名来为前端提供下载
        """
        response = make_response(
            send_from_directory('/var/tmp/utmtc/exportsysconf/.diff/',
                                filename,
                                as_attachment=True))
        # 开发时，到当前目录下找文件。在模块集成时应切换为某个特定目录
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    @app.route('/api/downloadAllConfDiff')
    def download_all_conf_diff():
        """ 将所有 conf 打一个 tar 包，为前端提供下载
        """
        # 这玩意换成最终的目录即可
        dir_name = "/var/tmp/utmtc/exportsysconf/.diff"
        folder_name = "SystemConfigDiff"
        tar_name = "/var/tmp/utmtc/exportsysconf/SystemConfigDiff.tar.gz"
        result = {}
        response = {}
        try:
            create_tar(dir_name, folder_name, tar_name)
            response = make_response(
                send_from_directory(tar_name[:tar_name.rfind('/') + 1],
                                    tar_name[tar_name.rfind('/') + 1:],
                                    as_attachment=True))
        except Exception as e:
            result = {'success': False, 'exception': str(e)}
            response = make_response(result)

        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    @app.route('/api/exportConfDiff/<filename>')
    def export_conf_diff(filename):
        """ 根据文件名来导出 conf 到本地
        """
        # filename 参数不包含路径
        result = {}
        try:
            ## 输出到当前目录下
            output_path = os.path.join(_curdir,'utmtc-output/exportsysconf')
            os.makedirs(output_path, exist_ok=True)
            shutil.copyfile("/var/tmp/utmtc/exportsysconf/.diff/" + filename,
                            output_path + '/' + filename)
            result = {
                'success': True,
                'targetPath': output_path + '/' + filename
            }
        except IOError as e:
            print("导出失败")
            print(str(e))
            result = {
                'success': False,
                'exception': str(e)
            }  # 这里应该可以加一点种类和附加信息
        response = make_response(jsonify(result))
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    @app.route('/api/exportAllConfDiff')
    def export_all_conf_diff():
        """ 将所有 conf 打包并导出到本地
        """
        ## 输出到当前目录下
        output_path = os.path.join(_curdir,'utmtc-output/exportsysconf')
        os.makedirs(output_path, exist_ok=True)
        dir_name = "/var/tmp/utmtc/exportsysconf/.diff"
        folder_name = "SystemConfigDiff"
        tar_name = output_path + "/SystemConfigDiff.tar.gz"
        result = {}
        try:
            create_tar(dir_name, folder_name, tar_name)
            result = {'success': True, 'targetPath': tar_name}
        except Exception as e:
            result = {'success': False, 'exception': str(e)}
        response = make_response(jsonify(result))
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    return app


def start_server():
    """ 启动服务器。该函数供外部直接调用
    """
    global server_ip
    global server_port

    # 判断是否已经有导出数据的，如果还没有就直接返回
    if os.path.exists(
            "/var/tmp/utmtc/exportsysconf/exportsysconf.json") == False:
        print(
            "\n  Config scan file not found. Please run 'utmtc exportsysconf' first.\n"
        )
        return

    # 获取本机 ip 地址
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("10.255.255.255", 30304))
        server_ip = s.getsockname()[0]
        s.close()
    except Exception as e:
        print(str(e))
        print("UTMTC Web server failed to get local IP address")

    # 从 5000 端口开始找未被占用的端口，然后在这个端口上起服务器
    for port in range(5000, 10000):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.bind((server_ip, port))
            server_port = port
            break
        except Exception as e:
            continue

    # 启动服务器
    try:
        app = create_app()
        http_server = WSGIServer((server_ip, server_port), app)
    except Exception as e:
        print("UTMTC Web server start failed.")
        print(e)
    try:
        print("\n   ============ UTMTC Web Interface started ============")
        print(" Please use web browser to visit: http://%s:%d/\n" %
              (server_ip, server_port))
        print(
            " You can exit the current program by pressing CTRL+C on your keyboard.\n"
        )
        http_server.serve_forever()
    except KeyboardInterrupt as ki:
        print('   ==== Ctrl+C Pressed.  Terminate UTMTC Web Server ====\n')


def main():
    start_server()


if __name__ == "__main__":
    main()
