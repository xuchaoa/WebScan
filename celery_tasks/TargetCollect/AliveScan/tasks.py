#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 8/7/19 8:33 PM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : tasks.py


import nmap
from utils.ip_op import ip_range_to_list
from celery_tasks.main import app
import ipaddress
from utils.mongo_op import MongoDB
import json

def nmap_alive_scan(network_prefix, taskID):
    nm = nmap.PortScanner()
    ping_scan_raw = nm.scan(hosts = network_prefix,arguments='-sn') #hosts可以是单个IP地址也可以是一整个网段,arguments就是运用什么方式扫描，-sn就是ping扫描。
    alive_ip = {}
    for result in ping_scan_raw['scan'].values():
        if result['status']['state'] == 'up':
            alive_ip[result['addresses']['ipv4']] = result['status']

    ip_range = ipaddress.ip_network(network_prefix, strict=False)
    handle_data(ip_range.hosts(), alive_ip, taskID)

def nmap_alive_scan_single(ip, FtaskID):
    nm = nmap.PortScanner()
    result = nm.scan(hosts=ip, arguments='-sn')
    print(result)
    if len(result['scan'].values()):
        handle_data([ip],{ip:result['scan'][ip]['status']}, FtaskID)
    else:
        handle_data([ip],{}, FtaskID)

def nmap_alive_scan_single_with_taskid(ip, taskID):
    nm = nmap.PortScanner()
    result = nm.scan(hosts=ip, arguments='-sn')
    _  = MongoDB()
    if len(result['scan'].values()):
        _.add_alive_status(taskID, result['scan'][ip]['status'])
        add_task(taskID, ip)
    else:
        _.add_alive_status(taskID, {'status':'down','reason':''})

def nmap_alive_scan_range(ip_list, taskID):
    nm = nmap.PortScanner()
    alive_ip = {}
    for ip in ip_list:
        ping_scan_raw = nm.scan(hosts=ip,arguments='-sn')
        if len(ping_scan_raw['scan'].values()):
            alive_ip[ip] = ping_scan_raw['scan'][ip]['status']

    handle_data(ip_list, alive_ip, taskID)
    return alive_ip


def handle_data(ip_list, alive_ip, FtaskID):
    for ip in ip_list:
        if str(ip) not in alive_ip.keys():
            alive_ip[str(ip)] = {'state':'down',
                                    'reason':''}
    _ = MongoDB()
    print(alive_ip)
    alive_task_id = _.add_alive_status_with_FtaskID(json.dumps(alive_ip), FtaskID)
    print("alive_task_id", alive_task_id)
    for ip,taskID in alive_task_id.items():
        add_task(taskID, ip)


def add_task(taskID, host):
    # app.send_task(name='PortScan',
    #               queue='PortScan',
    #               kwargs=dict(taskID=taskID, host=host))
    app.send_task(name='PortServScan',
                  queue='PortServScan',
                  kwargs=dict(taskID=taskID, ip_addr=host, resp='syn_normal'))
    app.send_task(name='IpLocation',
                  queue='IpLocation',
                  kwargs=dict(taskID=taskID, ip=host))


@app.task(bind=True,name='AliveScan')
def main(self, ip_type, ip, taskID=None, FtaskID=None):
    if taskID is not None and FtaskID is None:  #subdomain 推送过来的任务包含taskID
        nmap_alive_scan_single_with_taskid(ip, taskID)
    elif FtaskID is not None:  #手动直接从前段添加的任务包含父任务ID
        if ip_type == 'range':  #ip 范围
            ip_list = ip_range_to_list(ip)
            # ip_str = ','.join(ip_list)
            nmap_alive_scan_range(ip_list, FtaskID)
        elif ip_type == 'single':  #单ip
            nmap_alive_scan_single(ip, FtaskID)
        else:  # ip with mask
            nmap_alive_scan(ip, FtaskID)
    else:
        pass

if __name__ == '__main__':
    # main(ip_type='range', ip='123.207.155.221-123.207.155.230')
    main(ip_type='single', ip='188.131.133.213')


