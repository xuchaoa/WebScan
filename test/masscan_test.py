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

from PortScan.masscan import masscan

try:
    mas = masscan.PortScanner()
except masscan.PortScannerError:
    print("masscan binary not found", sys.exc_info()[0])
    sys.exit(1)
except:
    print("Unexpected error:", sys.exc_info()[0])
    sys.exit(1)

print("masscan version:", mas.masscan_version)
mas.scan('10.6.65.231', ports='15672,5672',sudo=False)
print("masscan command line:", mas.command_line)
#print('maascan scaninfo: ', mas.scaninfo)
#print('maascan scanstats: ', mas.scanstats)

for host in mas.all_hosts:
    print("Host: %s (%s)" % (host, mas[host]))


print(mas.command_line)
