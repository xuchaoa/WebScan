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
import celery
class my_task(celery.Task):
    def on_success(self, retval, task_id, args, kwargs):
        print('task success : {}:{}:{}:{}'.format(retval, task_id, args, kwargs))
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print(' task fail {}:{}:{}:{}:{}'.format(exc, task_id, args, kwargs, einfo))
    def on_retry(self, exc, task_id, args, kwargs, einfo):
        print('task retry {}:{}:{}:{}:{}'.format(exc, task_id, args, kwargs, einfo))
        print('---',self.request.retries)
        if self.request.retries == 2:
            # 连续三次失败,把任务推动到给 nmap
            app.send_task(name='PortServScan',
                          queue='PortServScan',
                          kwargs=dict(taskID=kwargs['taskID'], ip_addr=kwargs['host'], resp='syn_normal'))



def work_name(name, tid=None):
    """ 从环境变量获取扫描记录 tid 值并与基础队列名拼接成该扫描的队列名 """
    if not tid:
        tid = os.environ.get('MISSION_TID', None)
    return '{}'.format(name) if not tid else '{}.{}'.format(str(tid), name)

def add_serv_task(taskID, host, ports):
    app.send_task(name='ServScan',
                  queue='ServScan',
                  kwargs=dict(taskID=taskID, host=host,ports=ports))

@app.task(bind=True,name=work_name('PortScan'), base=my_task)  # , retry_kwargs={'max_retries':3, 'countdown': 10}
def portscan(self, taskID, host, ports='0-10000', rate=1000):
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
        print('当前重试次数',self.request.retries)
        raise self.retry(exc=e, countdown=60, max_retries=2)  #最大重试次数2，对一个ip最多扫描3次结束
        # app.send_task(name='PortServScan',
        #               queue='PortServScan',
        #               kwargs=dict(taskID=taskID, ip_addr=host, resp='syn_normal'))
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
        # add_serv_task(taskID, host, ports)



if __name__ == '__main__':
    portscan('5d5506c57dc1aa461b416202','123.207.155.221',ports='80,443,9711')
