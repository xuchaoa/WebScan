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

def nmap_alive_scan(network_prefix):
    nm = nmap.PortScanner()
    ping_scan_raw = nm.scan(hosts = network_prefix,arguments='-sn') #hosts可以是单个IP地址也可以是一整个网段,arguments就是运用什么方式扫描，-sn就是ping扫描。
    alive_ip = {}
    for result in ping_scan_raw['scan'].values():
        if result['status']['state'] == 'up':
            alive_ip[result['addresses']['ipv4']] = result['status']

    ip_range = ipaddress.ip_network(network_prefix, strict=False)
    handle_data(ip_range.hosts(), alive_ip)


def nmap_alive_scan_str(ip_list):
    nm = nmap.PortScanner()
    alive_ip = {}
    for ip in ip_list:
        ping_scan_raw = nm.scan(hosts=ip,arguments='-sn')
        if len(ping_scan_raw['scan'].values()):
            alive_ip[ip] = ping_scan_raw['scan'][ip]['status']

    handle_data(ip_list, alive_ip)
    return alive_ip

def handle_data(ip_list, alive_ip):
    for ip in ip_list:
        if str(ip) not in alive_ip.keys():
            alive_ip[str(ip)] = {'status':'down',
                                    'reason':''}
    print(alive_ip)


def mongo_op():
    pass
    #完善mongo中主机状态字段，没有则创建

@app.task(bind=True,name='alivescan')
def main(self, ip_type, ip, task_id=None):
    if ip_type == 'range':  #ip range
        ip_list = ip_range_to_list(ip)
        # ip_str = ','.join(ip_list)
        nmap_alive_scan_str(ip_list)  # 输入你要扫描的网段。
    else:  # ip with mask or single ip
        nmap_alive_scan(ip)


if __name__ == '__main__':
    main(ip_type='range', ip='123.207.155.230-123.207.155.240')



