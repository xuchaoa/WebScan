#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/23/19 3:23 PM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : tasks.py

'''
单独Nmap服务扫描
'''

import os
import sys
import re
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(BASE_DIR)
import nmap
# from lib.data import logger
import json
from celery_tasks.main import app
from utils.mongo_op import MongoDB

def tasks_dispatch(taskID, url):
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
        if key == 80 and 'name' in value.keys() and 'http' in value['name']:
            tasks_dispatch(taskID, ip_addr)
        elif key == 443 and 'name' in value.keys() and 'http' in value['name']:
            tasks_dispatch(taskID, ip_addr)
        if 'name' in value.keys():
            service = value['name']
            ##TODO 确定输出service名称的一致性
            # 详见https://svn.nmap.org/nmap/nmap-services
            if re.search('teedtap', service, re.I):
                service = 'mssql'
            elif 'ssh' == service or re.search('tcpwrapped', service, re.I):  # 'ssh' in service:
                service = 'ssh'
            elif 'mysql' == service:
                service = 'mysql'
            elif re.search('ms-wbt-server', service, re.I):
                service = 'rdp'
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
            # elif re.search('mongodb', service, re.I):
            #     service = 'mongo'
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

@app.task(bind=True,name='ServScan')
def nmapscan(self, taskID, host, ports):
    '''
    :param host: str
    :param ports: str list
    :return: None or json data
    '''
    # 接受从masscan上扫描出来的结果
    # 为了可以多线程使用，此函数支持多线程调用
    nm = nmap.PortScanner()
    argument = "-sV -sS -Pn --host-timeout 1m -p{}".format(','.join(ports))
    try:
        ret = nm.scan(host, arguments=argument)
    except nmap.PortScannerError as e:
        print(e)
        return None
    except:
        print('22222')
        return None

    if host in ret["scan"]:
        try:
            result = ret["scan"][host]["tcp"]
        except KeyError:
            return None
        print(result)
        _ = MongoDB()
        _.add_port_serv(taskID,json.dumps(result))

    handle_result(taskID, host, result)



if __name__ == '__main__':
    nmapscan('111', '123.207.155.221',['80','443','8080','9711','22'])
