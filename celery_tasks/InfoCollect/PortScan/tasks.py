#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/2 下午5:02
# @Author  : Archerx
# @Site    : https://blog.ixuchao.cn
# @File    : tasks.py
# @Software: PyCharm

import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
from ScanMoudle.PortScan.masscan import masscan
import json
from celery_tasks.main import app
from utils.mongo_op import MongoDB
from utils.printx import print_json_format


def work_name(name, tid=None):
    """ 从环境变量获取扫描记录 tid 值并与基础队列名拼接成该扫描的队列名 """
    if not tid:
        tid = os.environ.get('MISSION_TID', None)
    return '{}'.format(name) if not tid else '{}.{}'.format(str(tid), name)



@app.task(bind=True,name=work_name('PortScan'))
def portscan(self, taskID, host, ports='0-10000', rate=2000):
    try:
        mas = masscan.PortScanner()
    except masscan.PortScannerError:
        print("masscan binary not found", sys.exc_info()[0])
    except:
        print("Unexpected error:", sys.exc_info()[0])
    mas.scan(host, ports, sudo=False,arguments="--rate {}".format(rate))
    # print("masscan command line:", mas.command_line)

    PortResult = {}
    for host in mas.all_hosts:
        temp = {host: mas[host]}
        PortResult.update(temp)
        # print("Host: %s (%s)" % (host, mas[host]))
    # print(PortResult)
    print_json_format(PortResult)

    _ = MongoDB()
    _.add_open_ports(taskID, json.dumps(PortResult))



if __name__ == '__main__':
    portscan('123.207.172.60','0-10000',2000)