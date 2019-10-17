#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 8/2/19 3:29 PM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : Request.py

import requests
import urllib3
from ScanMoudle.xscan_poc.lib.utils.random_ua import get_random_ua


class Requests:
    def __init__(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        requests.packages.urllib3.disable_warnings()

        # if conf.proxy:
        #     protocol, ip, port = conf.proxy
        #     if protocol == "socks5":
        #         socks.set_default_proxy(socks.SOCKS5, ip, port)
        #     elif protocol == "socks4":
        #         socks.set_default_proxy(socks.SOCKS4, ip, port)
        #     else:
        #         socks.set_default_proxy(socks.HTTP, ip, port)
        #     socket.socket = socks.socksocket
    def __getattr__(self, method):
        def inner(*args, **kwargs):
            # setting random user agent
            if "headers" not in kwargs.keys():
                kwargs['headers'] = {'User-Agent': get_random_ua()}
            elif 'User-Agent' not in kwargs['headers'].keys():
                kwargs['headers']['User-Agent'] = get_random_ua()
            # setting exclude ssl
            if "verify" not in kwargs.keys():
                kwargs['verify'] = False
            f = getattr(requests, method)
            return f(*args, **kwargs)
        return inner


request = Requests()