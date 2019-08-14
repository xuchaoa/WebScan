#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 8/5/19 7:30 PM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : tasks.py

# ssh

import os
from celery_tasks.main import app
from conf.global_config import HYDRADIC_SMALL, HYDRADIC_LARGE
from utils.mongo_op import MongoDB
import json

@app.task(bind=True,name='HydraBrute')
def dispatch(self, taskID, username, dict, host, port, service):
    if username == "dict":
        NameDictBrute(taskID, username, dict, host, port, service)
    else:
        NameBrute(taskID, username, dict, host, port, service)
#     if type == 'ssh':
#         SSHBrute()


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
    x = os.system("hydra -l {} -P {} {} -s  {} {} -I -o x".format(username, HYDRADIC_LARGE if large_or_small == "large" else HYDRADIC_SMALL,
                                                          host, port, service))
    # print(x)
    with open('x','r') as f:
        print('-----------------------------')
        # print(f.read())
        for _ in f:
            if _.startswith('['):
                handle_result(taskID, _)
            print(_)
        # handle_result(f.read())
    os.remove('x')

def NameDictBrute(taskID, username_dict, large_or_small, host, port, service):
    x = os.system("hydra -L {} -P {} {} -s  {} {} -I -o x".format(username_dict,
                                                                  HYDRADIC_LARGE if large_or_small == "large" else HYDRADIC_SMALL,
                                                                  host, port, service))
    print(x)
    with open('x', 'r') as f:
        for _ in f:
            if _.startswith('['):
                handle_result(taskID, _)
            print(_)
    os.remove('x')




if __name__ == '__main__':
    # SSHBrute('sa','small','127.0.0.1','1433','mssql')

    # NameBrute('5d51652fa814d0464ed543b6','x','small','127.0.0.1','22','ssh')
    handle_result('5d51652fa814d0464ed543b7',"[22][ssh] host: 127.0.0.1   login: x   password: xuchao")
    handle_result('5d51652fa814d0464ed543b7',"[22][aaa] host: 127.0.0.1   login: x   password: xuchao")

    # NameBrute('root','small','127.0.0.1','3306','mysql')
    # NameBrute('root','small','127.0.0.1','3389','rdp')
    # 另外还支持 smb pop3 telnet ftp