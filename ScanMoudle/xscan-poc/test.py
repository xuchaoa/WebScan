#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/31/19 3:06 PM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : test.py

from lib.core.datatype import AttribDict
import argparse

# x = AttribDict()
# x.a = 1
# print(x.a)
# import ipaddress
# ip_range = ipaddress.ip_network('192.168.123.1/24', strict=False)
#
# for ip in ip_range:
#     print(ip)

import importlib.util

module_spec = importlib.util.spec_from_file_location('test1', '/home/x/PycharmProjects/WebScan/ScanMoudle/xscan-poc/poc.py')
module = importlib.util.module_from_spec(module_spec)
print(module)
module_spec.loader.exec_module(module)
# bug here how to change poc-->ESSENTIAL_MODULE_METHODS
scan_module = module.test1
