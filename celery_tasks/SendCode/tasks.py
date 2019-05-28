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



@app.task(name='test')
def test():
    import time
    # time.sleep(4)
    print("hello")
    return 1

if __name__ == '__main__':
    for i in range(2000):
        test.delay()
    # print('over')
