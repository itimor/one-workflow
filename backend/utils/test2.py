#!/usr/bin/env python
# coding: utf8

import json
a = '[{"id": 2, "field_value": "2020-03-31T16:00:00.000Z"}, {"id": 3, "field_value": "2020-04-06T16:00:00.000Z"}]'

b = json.loads(a)
for i in b:
    print(i)
