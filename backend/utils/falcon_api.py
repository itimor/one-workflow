#!/usr/bin/python
# -*- coding:utf8 -*-


import requests
import json
import time

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


class FalconApi(object):
    def __init__(self, endpoint=None, user=None, password=None, keys=[], session=None, ssl_verify=True):
        self._endpoint = endpoint
        self._url_prex = '/api/v1/'
        self._keys = keys
        self._session = session
        self.ssl_verify = ssl_verify

        if endpoint:
            self._endpoint = endpoint

        if not session:
            params = {
                "name": user,
                "password": password
            }
            self._session = requests.Session()
            ret = self.do_request('post', 'user/login', params=params)
            api_token = {
                "name": user,
                "sig": ret.get("sig")
            }
            self._session.headers.update({
                'Content-Type': 'application/json; charset=utf-8',
                'Accept': 'application/json',
                'Apitoken': json.dumps(api_token)
            })

    def __getattr__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]

        return self.__class__(
            endpoint=self._endpoint,
            keys=self._keys + [key],
            session=self._session,
            ssl_verify=self.ssl_verify)

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __call__(self, **kwargs):
        method = self._keys[-1]
        url = "/".join(self._keys[0:-1])
        url = url.strip("/")
        return self.do_request(method, url, **kwargs)

    def do_request(self, method, url, params=None, data=None):
        url = self._endpoint + self._url_prex + url

        if params is None:
            params = {}

        if method == 'get' or method == 'list':
            response = self._session.get(url, params=params, verify=self.ssl_verify)

        if method == 'post' or method == 'create':
            response = self._session.post(url, params=params, json=data, verify=self.ssl_verify)

        if method == 'put' or method == 'update':
            response = self._session.put(url, json=data, verify=self.ssl_verify)

        if method == 'delete':
            response = self._session.delete(url, params=params, json=data, verify=self.ssl_verify)

        try:
            body = response.json()
        except ValueError:
            body = "Get unknow error from falcon:%s" % response.text
        if response.status_code >= 400:
            return {'code': response.status_code, 'method': method, 'url': url, 'message': body}

        return body


if __name__ == '__main__':
    cli = FalconApi(endpoint="http://47.56.11.71:8080", user='root', password='v5benzro-gf*TY1k')
    # 查询用户列表
    # r = cli.user.users.list()
    node = ["aliyun-hk-yabo-prod-boce01", "aliyun-huabei-yabo-prod-boce04"]
    # 查询 Counter eid
    query = {
        "q": node[0],
    }
    eid = cli.graph.endpoint.get(params=query)[0]["id"]
    # 查询 Counter
    query = {
        "eid": eid,
        "metricQuery": "cpu.idle"
    }
    r = cli.graph.endpoint_counter.get(params=query)
    counters = [x["counter"] for x in r]
    # 查询历史数据
    end_time = int(time.time())  # 必须要整形
    start_time = end_time - 1800  # 30分钟
    query = {
        "step": 240,
        "start_time": start_time,
        "end_time": end_time,
        "hostnames": node,
        "consol_fun": "AVERAGE",
        "counters": counters
    }
    r = cli.graph.history.post(data=query)
    print(r)
