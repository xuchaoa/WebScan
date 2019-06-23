#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/23 下午4:16
# @Author  : Archerx
# @Site    : https://blog.ixuchao.cn
# @File    : tasks.py
# @Software: PyCharm

from celery_tasks.main import app
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
import subprocess
import json

@app.task(bind=True,name='fingerscan')
def fingerscan(self,url,proxy=0,thread=50,time=5):
    # os.system("cd "+BASE_DIR+"/ScanMoudle/webscan/fingerdetect/")
    cmd = ['python2','TideFinger.py','-u',url,'-p',str(proxy),'-m',str(thread),'-t',str(time)]
    cmd = ' '.join(cmd)
    print(cmd)
    result = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,cwd=BASE_DIR+"/ScanMoudle/webscan/fingerdetect/")

    res = str(result.stdout.read())[2:-3]
    print(json.loads(res))
    print(res)
    print(type(res))

if __name__ == '__main__':
    print(sys.path[:-1])
    print(BASE_DIR)
    fingerscan("https://blog.bbsec.xyz")
