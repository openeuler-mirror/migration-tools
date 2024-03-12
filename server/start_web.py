import socket
import http.server
import socketserver
import os
import json

os.chdir('/usr/lib/uos-sysmig-data/template')
start_port=8080

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    s.connect(('10.255.255.255', 1))
    ip = s.getsockname()[0]
except Exception:
    ip = '127.0.0.1'
finally:
    s.close()

for port in range(start_port, start_port+1000):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.bind((ip, port))
        server_port = port
        break
    except Exception as e:
        continue

Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer((ip, server_port), Handler) as httpd:
    print("serving at http://%s:%s" % (ip, server_port))
    data = {'ip': ip, 'port': server_port}
    with open('/usr/lib/uos-sysmig-data/web.json', 'w+') as f:
        json.dump(data, f)
    httpd.serve_forever()
