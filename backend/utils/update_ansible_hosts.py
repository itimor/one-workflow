# -*- coding: utf-8 -*-
# author: timor

import time
import requests
import sys

http://10.4.12.2:8080/configfiles/json/jenkins-front/default/application
reload(sys)
sys.setdefaultencoding('utf8')

apollo_conf = {
    "pro": {
        "config_server_url": "http://10.4.12.2:8080",
        "appId": "samanage01-inventory",
        "clusterName": "default",
        "namespaceName": "pro",
        "namespaceType": "txt",
        "saveFilename": "/etc/ansible/pro-hosts",
    },
    "uat": {
        "config_server_url": "http://10.4.12.2:8080",
        "appId": "samanage01-inventory",
        "clusterName": "default",
        "namespaceName": "uat",
        "namespaceType": "txt",
        "saveFilename": "/etc/ansible/uat-hosts",
    },
    "fat": {
        "config_server_url": "http://10.4.12.2:8080",
        "appId": "samanage01-inventory",
        "clusterName": "default",
        "namespaceName": "fat",
        "namespaceType": "txt",
        "saveFilename": "/etc/ansible/fat-hosts",
    },
    "dev": {
        "config_server_url": "http://10.4.12.2:8080",
        "appId": "samanage01-inventory",
        "clusterName": "default",
        "namespaceName": "dev",
        "namespaceType": "txt",
        "saveFilename": "/etc/ansible/dev-hosts",
    },
}


def load_conf(conf):
    print('判断版本 {}'.format(conf["namespaceName"]))
    release_url = '{}/configs/{}/{}/{}.{}'.format(conf["config_server_url"], conf["appId"], conf["clusterName"], conf["namespaceName"], conf["namespaceType"])
    html = requests.get(release_url)
    content = html.json()['releaseKey']

    if not check_file_release(content, conf["namespaceName"]):
        print('版本已更新 {}'.format(conf["namespaceName"]))
        print('载入配置 {}'.format(conf["namespaceName"]))
        conf_url = '{}/configfiles/json/{}/{}/{}.{}'.format(conf["config_server_url"], conf["appId"], conf["clusterName"], conf["namespaceName"], conf["namespaceType"])
        html = requests.get(conf_url)
        content = html.json()['content']
        print('保存配置 {} ==> {}'.format(conf["namespaceName"], conf["saveFilename"]))
        save_file(conf["saveFilename"], content)
    else:
        print('版本未更新 {}'.format(conf["namespaceName"]))


def save_file(filename, content):
    with open(filename, 'w') as fn:
        fn.write(content)


def check_file_release(content, namespaceName):
    release_file = namespaceName + '.release'
    try:
        with open(release_file, 'r') as fn:
            if content == fn.read():
                return True
            else:
                return False
    except Exception as e:
        return False
    finally:
        with open(release_file, 'w') as fn:
            fn.write(content)


if __name__ == '__main__':
    while True:
        time.sleep(5)
        print(time.strftime('%Y年%m月%d日 %M时%I分%S秒', time.localtime()))
        for conf in apollo_conf:
            load_conf(conf)
