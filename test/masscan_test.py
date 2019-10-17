#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/24 下午 10:10
# @Author  : Archerx
# @Site    : 
# @File    : masscan_test.py
# @Software: PyCharm

# import masscan
#
# mas = masscan.PortScanner()
# mas.scan('10.6.65.0/24', ports='22,80,8080',sudo=True)
# print (mas.scan_result)

import sys

# from ScanMoudle.PortScan.masscan import masscan
import masscan


mas = masscan.PortScanner()



mas.scan('10.0.85.203', ports='0-443',sudo=False)
# print("masscan command line:", mas.command_line)

PortResult = {}
for host in mas.all_hosts:
    temp = {host:mas[host]}
    PortResult.update(temp)
    print("Host: %s (%s)" % (host, mas[host]))


# print(mas.command_line)
print(PortResult)
