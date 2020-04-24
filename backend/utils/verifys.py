# -*- coding: utf-8 -*-
# author: itimor

import re
import IPy


def is_valid_domain(value):
    domain_pattern = re.compile(
        r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
        r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
        r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
        r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
    )
    return True if domain_pattern.match(value) else False


def is_domain(domain):
    domain_regex = re.compile(
        r'(?:[A-Z0-9_](?:[A-Z0-9-_]{0,247}[A-Z0-9])?\.)+(?:[A-Z]{2,6}|[A-Z0-9-]{2,}(?<!-))\Z',
        re.IGNORECASE)
    return True if domain_regex.match(domain) else False


def is_ip(address):
    print(address)
    try:
        IPy.IP(address)
        return True
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    print(is_valid_domain('https://aa.www.baidu.com'))
    print(is_ip('22.2.2.256'))
