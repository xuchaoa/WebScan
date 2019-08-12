#!/usr/bin/env python  这一行Linux上才需要
# -*- coding: utf-8 -*-
# @Time    : 2019/8/11 下午10:23
# @Author  : Archerx
# @Site    : https://blog.ixuchao.cn
# @File    : tasks.py


import nmap
from utils.mongo_op import MongoDB
import json
from celery_tasks.main import app

@app.task(bind=True,name='PortServScan')
def namp_port_scan(self, taskID, ip_addr, resp):
    scanner = nmap.PortScanner()
    # 1)SYN ACK Scan == syn
    # 2)UDP Scan  == udp
    # 3)Comprehensive Scan == com
    if resp == 'syn_normal':
        scanner.scan(ip_addr, '21,22,23,80,115,443,445,547,1433,3306,3389,8080', '-sV -sS -Pn')
        # print(scanner[ip_addr]['tcp'])
        # print("Ip Status: ", scanner[ip_addr]['status'])
    if resp == 'syn':
        # print("Nmap Version: ", scanner.nmap_version())
        scanner.scan(ip_addr, '1-1024', '-v -sS')
        # print(scanner.scaninfo())
        # print(scanner[ip_addr])
        print(scanner[ip_addr]['tcp'])
        print("Ip Status: ", scanner[ip_addr]['status'])
        # print(scanner[ip_addr].all_protocols())
        # print("Open Ports: ", scanner[ip_addr]['tcp'].keys())
    elif resp == 'udp':
        scanner.scan(ip_addr, '1-1024', '-v -sU')
        print("Ip Status: ", scanner[ip_addr].state())
        print(scanner[ip_addr].all_protocols())
        print("Open Ports: ", scanner[ip_addr]['udp'].keys())
    elif resp == 'com':
        scanner.scan(ip_addr, '1-1024', '-v -sS -sV -sC -A -O')
        print("Ip Status: ", scanner[ip_addr].state())
        print(scanner[ip_addr].all_protocols())
        print("Open Ports: ", scanner[ip_addr]['tcp'].keys())
    else:
        pass

    result = {}
    for key, value in scanner[ip_addr]['tcp'].items():
        if value['state'] == 'open':
            result[key] = value
    print(result)
    x = MongoDB()
    x.add_port_sev_result(taskID,json.dumps(result))



if __name__ == '__main__':
    namp_port_scan('123.207.155.221', 'syn_normal')