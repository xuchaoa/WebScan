#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 8/7/19 7:49 PM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : ip_op.py


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