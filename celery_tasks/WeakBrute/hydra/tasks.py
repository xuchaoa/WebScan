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

@app.task(bind=True,name='HydraBrute')
def dispatch(self, type):
    if type == 'ssh':
        SSHBrute()


def SSHBrute(username, large_or_small, host, port, service):
    x = os.system("hydra -l {} -P {} {} -s  {} {} -I -o x".format(username, HYDRADIC_LARGE if large_or_small == "large" else HYDRADIC_SMALL,
                                                              host, port, service))
    print(x)
    with open('x','r') as f:
        print('-----------------------------')
        print(f.read())
    os.remove('x')

def MSSqlBrute(username, large_or_small, host, port, service):
    x = os.system("hydra -l {} -P {} {} mssql -o x".format(username,HYDRADIC_LARGE if large_or_small == "large" else HYDRADIC_SMALL,
                                                                  host,  service))
    print(x)
    with open('x', 'r') as f:
        print('-----------------------------')
        print(f.read())
    os.remove('x')

def NameDictBrute(username_dict, large_or_small, host, port, service):
    x = os.system("hydra -L {} -P {} {} mssql -o x".format(username_dict,HYDRADIC_LARGE if large_or_small == "large" else HYDRADIC_SMALL,
                                                                  host,  service))
    print(x)
    with open('x', 'r') as f:
        print('-----------------------------')
        print(f.read())
    os.remove('x')

def VNCBrute():
    print('111')

def MySqlBrute():
    pass


if __name__ == '__main__':
    # SSHBrute('sa','small','127.0.0.1','1433','mssql')
    SSHBrute('x','small','127.0.0.1','22','ssh')
    SSHBrute('x','small','127.0.0.1','22','ssh')