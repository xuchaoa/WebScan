#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/2 下午5:02
# @Author  : Archerx
# @Site    : https://blog.ixuchao.cn
# @File    : tasks.py
# @Software: PyCharm


from celery_tasks.main import app

import os
import sys
from ScanMoudle.PortScan.masscan import masscan



def work_name(name, tid=None):
    """ 从环境变量获取扫描记录 tid 值并与基础队列名拼接成该扫描的队列名 """
    if not tid:
        tid = os.environ.get('MISSION_TID', None)
    return '{}'.format(name) if not tid else '{}.{}'.format(str(tid), name)



@app.task(bind=True,name=work_name('portscan'))
def portscan(self,host,port=[]):


    try:
        mas = masscan.PortScanner()
    except masscan.PortScannerError:
        print("masscan binary not found", sys.exc_info()[0])
    except:
        print("Unexpected error:", sys.exc_info()[0])

    print("masscan version:", mas.masscan_version)
    mas.scan('10.6.65.231', ports='15672,5672', sudo=False)
    print("masscan command line:", mas.command_line)
    # print('maascan scaninfo: ', mas.scaninfo)
    # print('maascan scanstats: ', mas.scanstats)

    for host in mas.all_hosts:
        print("Host: %s (%s)" % (host, mas[host]))

    print(mas.command_line)

