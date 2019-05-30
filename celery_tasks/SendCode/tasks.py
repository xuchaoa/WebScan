#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-5-18 上午9:05
# @Author  : Archerx
# @Site    : https://blog.ixuchao.cn
# @File    : test.py
# @Software: PyCharm

from celery_tasks.main import app



import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CTF_AWD_Platform.settings")
django.setup()
from django.conf import settings
from django.core.mail import send_mail


def work_name(name, tid=None):
    """ 从环境变量获取扫描记录 tid 值并与基础队列名拼接成该扫描的队列名 """
    if not tid:
        tid = os.environ.get('MISSION_TID', None)
    return '{}'.format(name) if not tid else '{}.{}'.format(str(tid), name)



@app.task(bind=True,name=work_name('testscan'))
def test(self):
    import time
    # time.sleep(4)
    print("hello")
    # return 1

if __name__ == '__main__':
    for i in range(2):
        test.delay()
    # print('over')
