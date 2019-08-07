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

def VNCBrute():
    print('111')


if __name__ == '__main__':
    SSHBrute('x','small','127.0.0.1','22','ssh')