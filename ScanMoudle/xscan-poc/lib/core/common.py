#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/31/19 10:48 AM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : common.py

from .data import paths
import os

def set_paths(module_path):
    '''
    :param proj_path:
    :return:
    '''
    paths.ROOT_PATH = module_path
    paths.DATA_PATH = os.path.join(paths.ROOT_PATH, "data")
    paths.POC_PATH = os.path.join(paths.ROOT_PATH, "pocs")
    paths.CONFIG_FILE = os.path.join(paths.ROOT_PATH, "config.conf")


def ip_range_to_list(ip_range):
    '''
    print (gen_ip('192.18.1.1-192.168.1.3'))
    ==> ['192.168.1.1', '192.168.1.2', '192.168.1.3']
    '''

    def num2ip(num):
        return '%s.%s.%s.%s' % ((num >> 24) & 0xff, (num >> 16) & 0xff, (num >> 8) & 0xff, (num & 0xff))

    def ip2num(ip):
        ips = [int(x) for x in ip.split('.')]
        return ips[0] << 24 | ips[1] << 16 | ips[2] << 8 | ips[3]

    start, end = [ip2num(x) for x in ip_range.split('-')]
    return [num2ip(num) for num in range(start, end + 1) if num & 0xff]
