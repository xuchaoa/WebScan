#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 8/5/19 7:30 PM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : tasks.py

'''
爆破脚本
'''

import os
import time
import uuid
from celery_tasks.main import app
from conf.global_config import HYDRADIC_SMALL, HYDRADIC_LARGE
from utils.mongo_op import MongoDB
import json
from conf.global_config import realjoin
import re
from conf.global_config import DIC_USERNAME_FTP, DIC_USERNAME_IMAP, DIC_USERNAME_MEMCACHED, DIC_USERNAME_MONGODB, DIC_USERNAME_MYSQL, \
    DIC_USERNAME_ORACLE, DIC_USERNAME_POP3, DIC_USERNAME_POSTGRESQL, DIC_USERNAME_RDP,DIC_USERNAME_REDIS, DIC_USERNAME_SMB,DIC_USERNAME_SMTP,\
    DIC_USERNAME_MSSQL,DIC_USERNAME_SSH,DIC_USERNAME_SVN,DIC_USERNAME_TELNET,DIC_USERNAME_TOMCAT,DIC_USERNAME_VNC,DIC_USERNAME_WEBLOGIC,COMMON_USERNAME,USERNAME_DICT

import celery
class my_task(celery.Task):
    def on_success(self, retval, task_id, args, kwargs):
        print('task success : {}:{}:{}:{}'.format(retval, task_id, args, kwargs))
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print(' task fail {}:{}:{}:{}:{}'.format(exc, task_id, args, kwargs, einfo))
    def on_retry(self, exc, task_id, args, kwargs, einfo):
        print('task retry {}:{}:{}:{}:{}'.format(exc, task_id, args, kwargs, einfo))


@app.task(bind=True, name='HydraBrute', base=my_task)
def dispatch(self, taskID, username, dict, host, port, service):
    #TODO fix 任务执行成功，但是无法发送ack导致任务重复执行 amqp.exceptions.RecoverableConnectionError: connection already closed \
    # 原因是cpu占用过高，心跳线程没有足够的cpu资源导致两次心跳包未发送rabbitmq直接关闭连接
    # http://eventlet.net/doc/modules/debug.html#eventlet.debug.hub_blocking_detection
    # 解决方法  1.降低cpu使用  2.增大rabbitmq的心跳阈值
    # 目前采取将心跳阈值增大到 600s -> 解决，目前没发现别的问题

    if username == "dict":  #跑username字典
        NameDictBrute(taskID, dict, host, port, service)
    else:
        NameBrute(taskID, username, dict, host, port, service)


def handle_result(taskID, result, service):
    print("this is the begin")
    x = result.strip('\n').split(' ')
    if result is 's':
        _result = {
            'redis': {
                'service':service,
                'port': x[0].strip('[').split(']')[0],
                'login': '',
                'password': ''
            }
        }
    else:
        _result = {
            x[0].strip('[').split(']')[1][1:]: {
                'service': service,
                'port': x[0].strip('[').split(']')[0],
                'login': x[6].strip(),
                'password': x[10].strip()
            }
        }
    print(_result)
    x = MongoDB()
    x.add_weak_pass_service(taskID, json.dumps(_result))

def NameBrute(taskID, username, large_or_small, host, port, service):
    '''
    用于username已经确定的情况下
    :param taskID:
    :param username:
    :param large_or_small:
    :param host:
    :param port:
    :param service:
    :return:
    '''
    file_name = str(uuid.uuid1())
    if service in ['redis','cisio','snmp','vnc']:
        _ = os.system("hydra -P {} {} -s  {} {} -I -o {} -f".format(HYDRADIC_LARGE if large_or_small == "large" else HYDRADIC_SMALL,
                                                                             host, port, service, file_name))
    else:
        _ = os.system("hydra -l {} -P {} {} -s  {} {} -I -o {}".format(username, HYDRADIC_LARGE if large_or_small == "large" else HYDRADIC_SMALL,
                                                          host, port, service, file_name))

    with open(file_name,'r') as f:
        print(f.read())
        for _ in f:
            if _.startswith('['):
                handle_result(taskID, _, service)
    os.remove(file_name)

def NameDictBrute(taskID, large_or_small, host, port, service):
    '''
    用于username和passwd都不确定的情况
    :param taskID:
    :param large_or_small:
    :param host:
    :param port:
    :param service:
    :return:
    '''
    # he redis, adam6500, cisco, oracle-listener, s7-300, snmp and vnc modules are only using the -p or -P option, not login (-l, -L) or colon file (-C).
    file_name = str(uuid.uuid1())
    dict_name = 'dic_username_' + service + '.txt'
    username_dict = realjoin(USERNAME_DICT,dict_name)
    if service in ['redis','cisio','snmp','vnc']:
        _ = os.system("hydra -P {} {} -s  {} {} -I -o {} -f".format(HYDRADIC_LARGE if large_or_small == "large" else HYDRADIC_SMALL,
                                                                          host, port, service, file_name))
    else:
        _ = os.system("hydra -L {} -P {} {} -s  {} {} -I -o {} -f".format(username_dict,
                                                                  HYDRADIC_LARGE if large_or_small == "large" else HYDRADIC_SMALL,
                                                                  host, port, service, file_name))

    print(_)
    ## TODO redis未授权访问无法解决
    with open(file_name, 'r') as f:
        print("-------------------------------------------------"+f.read())
        for _ in f:
            if _.startswith('['):
                handle_result(taskID, _ , service)

    os.remove(file_name)





if __name__ == '__main__':
    # SSHBrute('sa','small','127.0.0.1','1433','mssql')

    dispatch('5d7e39cd13e0dfe95c52e4cf','dict','small','127.0.0.1','6379','redis')
    dispatch('5d7e39cd13e0dfe95c52e4cf','dict','small','127.0.0.1','22','ssh')
    # handle_result('5d51652fa814d0464ed543b7',"[22][ssh] host: 127.0.0.1   login: x   password: xuchao")
    # handle_result('5d51652fa814d0464ed543b7',"[22][aaa] host: 127.0.0.1   login: x   password: xuchao")

    # NameBrute('root','small','127.0.0.1','3306','mysql')
    # NameBrute('root','small','127.0.0.1','3389','rdp')
    # 另外还支持 smb pop3 telnet ftp