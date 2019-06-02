# -*- coding: utf-8 -*-
"""Example to use python-masscan."""
import sys

import masscan

try:
    mas = masscan.PortScanner()
except masscan.PortScannerError:
    print("masscan binary not found", sys.exc_info()[0])
    sys.exit(1)
except:
    print("Unexpected error:", sys.exc_info()[0])
    sys.exit(1)

print("masscan version:", mas.masscan_version)
mas.scan('47.99.62.36', ports='22,80,3306')
print("masscan command line:", mas.command_line)
#print('maascan scaninfo: ', mas.scaninfo)
#print('maascan scanstats: ', mas.scanstats)

for host in mas.all_hosts:
    print("Host: %s (%s)" % (host, mas[host]))

