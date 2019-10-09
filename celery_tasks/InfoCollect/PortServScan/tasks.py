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
import re
from utils.mongo_op import MongoDB


def tasks_dispatch_web(taskID, url):
    app.send_task(name='ServInfo',
                  queue='ServInfo',
                  kwargs=dict(taskID=taskID, url=url))

    app.send_task(name='CmsFinger',
                  queue='CmsFinger',
                  kwargs=dict(taskID=taskID, url=url))

    app.send_task(name='Wappalyzer',
                  queue='Wappalyzer',
                  kwargs=dict(taskID=taskID, domain=url),
                  )
    app.send_task(name='SFileScan',
                  queue='SFileScan',
                  kwargs=dict(taskID=taskID, url=url))
    _ = MongoDB()
    info = _.get_one_hostscan_info(taskID)
    if 'domain' in info.keys() and len(info['domain']) != 0:
        app.send_task(name='DirScan',
                      queue='DirScan',
                      kwargs=dict(taskID=taskID, target=info['domain'])
                      )
    else:
        pass
        # TODO 以ip作为扫描目标,暂未实现


def handle_result(taskID, ip_addr, result):
    for key, value in result.items():
        # TODO 需要添加 只有443开放但是80未开放  的情况 和web端口更改的情况
        if (key == 80 or key == 443) and 'name' in value.keys() and 'http' in value['name']:
            tasks_dispatch_web(taskID, ip_addr)
        # elif key == 443 and 'name' in value.keys() and 'http' in value['name']:
        #     tasks_dispatch(taskID, ip_addr)
        if 'name' in value.keys() and re.search('ms-wbt-server', value['name'], re.I):
            #推送给单独爆破的脚本
            app.send_task(name='RDPassSpray',
                          queue='RDPassSpray',
                          kwargs=dict(taskID=taskID, target=ip_addr))
        if key == 8080:
        # TODO 找出明确特征证明使用的是st2框架
            pass

        if 'name' in value.keys():
            service = value['name']
            # 详见https://svn.nmap.org/nmap/nmap-services
            if re.search('teedtap', service, re.I):
                service = 'mssql'
            elif 'ssh' == service or re.search('tcpwrapped', service, re.I):  # 'ssh' in service:
                service = 'ssh'
            elif 'mysql' == service:
                service = 'mysql'
            # elif re.search('ms-wbt-server', service, re.I):
            #     service = 'rdp'
            ## 因为hydra的rdp爆破脚本过时，支持不够广泛，这里的爆破任务推送给独立爆破脚本
            elif re.search('microsoft-ds', service, re.I):
                service = 'smb'
            # elif re.search('pop3', service, re.I):  #太耗费时间，成功率不高
            #     service = 'pop3'
            elif re.search('telnet', service, re.I):
                service = 'telnet'
            elif re.search('ftp', service, re.I):
                service = 'ftp'
            elif re.search('memcache', service, re.I):
                service = 'memcache'
            elif re.search('postgresql', service, re.I):
                service = 'postgresql'
            elif re.search('redis', service, re.I):
                service = 'redis'
            elif re.search('oracle', service, re.I):
                service = 'oracle'
            # elif re.search('mongod', service, re.I):  ##TODO mongo 爆破
            #     service = 'mongod'
            elif 'tomcat' in service:
                service = 'tomcat'
            elif re.search('^vnc-\d{1}', service, re.I):
                service = 'vnc'
            elif 'weblogic' in service:
                service = 'weblogic'
            # elif 'imap' == service:
            #     service = 'imap'
            # elif 'smtp' == service:
            #     service = 'smtp'
            elif 'svn' == service:
                service = 'svn'
            else:
                service = 'xxx'
            if not service == 'xxx':
                app.send_task(name='HydraBrute',
                              queue='HydraBrute',
                              kwargs=dict(taskID=taskID, username='dict', dict='small', host=ip_addr, port=key, service=service)
                              )
        else:
            print('no name in keys')

        #TODO 考虑一下8080,java系服务器中间件、，以及中间件的详细探测

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

    handle_result(taskID, ip_addr, result_open)
    return result_open



if __name__ == '__main__':
    namp_port_scan('5d54da8362172cc4b8a3bb4c','149.129.89.14', 'syn_normal')