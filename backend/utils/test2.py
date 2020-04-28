#!/usr/bin/env python
# coding: utf8

a = [
    {
        "id": 1,
        "create_time": "2020-04-28 10:53:14",
        "update_time": "2020-04-28 18:06:04",
        "memo": "",
        "name": "aaa",
        "ticket_sn_prefix": "xx",
        "limit_expression": "",
        "display_form_str": "",
        "title_template": "",
        "type": {
            "id": 1,
            "create_time": "2020-04-28 10:47:35",
            "update_time": "2020-04-28 10:47:35",
            "memo": "",
            "name": "IT",
            "code": "it"
        }
    },
    {
        "id": 2,
        "create_time": "2020-04-28 18:03:51",
        "update_time": "2020-04-28 18:03:51",
        "memo": "",
        "name": "bbb",
        "ticket_sn_prefix": "oo",
        "limit_expression": "",
        "display_form_str": "",
        "title_template": "",
        "type": {
            "id": 2,
            "create_time": "2020-04-28 18:03:34",
            "update_time": "2020-04-28 18:03:34",
            "memo": "",
            "name": "行政",
            "code": "ad"
        }
    }
]

b = []

for i in a:
    k = i["type"]["name"]
    if k not in b:
        b.append(k)
