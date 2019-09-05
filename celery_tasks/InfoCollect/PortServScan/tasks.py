#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/8/11 下午10:23
# @Author  : Archerx
# @Site    : https://blog.ixuchao.cn
# @File    : tasks.py

'''
Nmap端口开放情况及服务扫描
'''

import nmap
from utils.mongo_op import MongoDB
import json
from celery_tasks.main import app

def tasks_dispatch(taskID, url):
    app.send_task(name='ServInfo',
                  queue='ServInfo',
                  kwargs=dict(taskID='5d6e24694c3e3fdb872e596c', url='https://blog.ixuchao.cn'))

    app.send_task(name='CmsFinger',
                  queue='CmsFinger',
                  kwargs=dict(taskID='5d6e24694c3e3fdb872e596c', url='https://blog.ixuchao.cn'))

@app.task(bind=True,name='PortServScan')
def namp_port_scan(self, taskID, ip_addr, resp):
    scanner = nmap.PortScanner()
    # 1)SYN ACK Scan == syn
    # 2)UDP Scan  == udp
    # 3)Comprehensive Scan == com
    if resp == 'syn_normal':
        # 5900开始是VNC端口号
        scanner.scan(ip_addr, '21,22,23,25,80,110,115,139,143,443,445,547,1433,1521,3306,3690,3389,5432,5901,5902,5903,6379,7001,8080,11211,27017', '-sV -sS -Pn')

    if resp == 'syn':
        scanner.scan(ip_addr, '1-1024', '-v -sS')
        print(scanner[ip_addr]['tcp'])
        print("Ip Status: ", scanner[ip_addr]['status'])

    elif resp == 'udp':  # udp扫描在大网络环境下不准确
        scanner.scan(ip_addr, '1-1024', '-v -sU')
        print("Open Ports: ", scanner[ip_addr]['udp'].keys())

    elif resp == 'com':
        scanner.scan(ip_addr, '1-1024', '-v -sS -sV -sC -A -O')

    else:
        pass

    result_open = {}
    result_filter = {}
    result_other = {}
    if 'tcp' in scanner[ip_addr].keys() or 'udp' in scanner[ip_addr].keys():
        if resp == 'com' or resp == 'syn' or resp == 'syn_normal':
            resp = 'tcp'
        for key, value in scanner[ip_addr][resp[:3]].items():
            if value['state'] == 'open':
                result_open[key] = value
            elif value['state'] == 'filtered':
                result_filter[key] = value
            else:
                result_other[key] = value


    # print(result_open)
    x = MongoDB()
    x.add_port_sev_result(taskID, json.dumps(result_open))

    for key, value in result_open.items():
        if key == 80 and 'name' in value.keys() and 'http' in value['name']:
            tasks_dispatch(taskID, ip_addr)
        if key == 443 and 'name' in value.keys() and 'http' in value['name']:
            tasks_dispatch(taskID, ip_addr)

    return result_open



if __name__ == '__main__':
    namp_port_scan('5d54da8362172cc4b8a3bb4c','149.129.89.14', 'syn_normal')