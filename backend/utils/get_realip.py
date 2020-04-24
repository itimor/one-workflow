# -*- coding: utf-8 -*-
# author: itimor


import requests
import socket
import json

#获取外网ip信息
output = requests.get('https://ifconfig.me/all.json').json()

# 获取本机计算机ip
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip

output['local_ip'] = get_local_ip()

## output
"""
{
  "ip_addr": "203.177.78.226",
  "remote_host": "unavailable",
  "user_agent": "python-requests/2.22.0",
  "port": 38542,
  "method": "GET",
  "encoding": "gzip, deflate",
  "mime": "*/*",
  "via": "1.1 google",
  "forwarded": "203.177.78.226, 216.239.32.21"
  "local_ip": "172.16.51.115"
}"""

with open('d:/ooxx.log', 'a+') as fn:
    print(output)
    fn.write(json.dumps(output))
