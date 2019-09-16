#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/2 下午5:02
# @Author  : Archerx
# @Site    : https://blog.ixuchao.cn
# @File    : tasks.py
# @Software: PyCharm


import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
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

def add_serv_task(taskID, host, ports):
    app.send_task(name='ServScan',
                  queue='ServScan',
                  kwargs=dict(taskID=taskID, host=host,ports=ports))

@app.task(bind=True,name=work_name('PortScan'), rate_limit='1/m')  #TODO 任务限制测试 效果未知
def portscan(self, taskID, host, ports='0-10000', rate=1500):
    try:
        mas = masscan.PortScanner()
    except masscan.PortScannerError:
        print("masscan binary not found", sys.exc_info()[0])
    except masscan.NetworkConnectionError:
        print("-------------------")
    except:
        print("Unexpected error:", sys.exc_info()[0])
    try:
        mas.scan(host, ports, sudo=False,arguments="--rate {}".format(rate))
    except masscan.NetworkConnectionError or masscan.PortScannerError as e:
        print(e)
        app.send_task(name='PortServScan',
                      queue='PortServScan',
                      kwargs=dict(taskID=taskID, ip_addr=host, resp='syn_normal'))
    else:
        PortResult = {}
        for host in mas.all_hosts:
            PortResult.update(mas[host]['tcp'])
        print(PortResult)
        _ = MongoDB()
        _.add_open_ports(taskID, json.dumps(PortResult))

        ports = []
        for _ in PortResult.keys():
            ports.append(str(_))
        add_serv_task(taskID, host, ports)



if __name__ == '__main__':
    portscan('5d5506c57dc1aa461b416202','123.207.155.221',ports='80,443,9711')
