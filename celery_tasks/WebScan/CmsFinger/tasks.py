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
from conf.global_config import PROJECT_PATH
sys.path.append(PROJECT_PATH)
import subprocess
import json
from utils.mongo_op import MongoDB
from utils.common import add_http

@app.task(bind=True,name='CmsFinger')
def fingerscan(self, taskID, url, proxy=0, thread=50, time=5):
    url = add_http(url)
    # os.system("cd "+BASE_DIR+"/ScanMoudle/webscan/fingerdetect/")
    cmd = ['python2','TideFinger.py','-u',url,'-p',str(proxy),'-m',str(thread),'-t',str(time)]
    cmd = ' '.join(cmd)
    print(cmd)
    result = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,cwd=PROJECT_PATH+"/ScanMoudle/webscan/fingerdetect/")
    res = str(result.stdout.read())[2:-3]
    # print(json.dumps(res))
    try:
        print(res)
        json.loads(res)
        _ = MongoDB()
        _.add_cms_finger(taskID, res)
    except Exception as e:
        print(e)
    return res


if __name__ == '__main__':
    # print(sys.path[:-1])
    # print(BASE_DIR)
    # fingerscan("https://blog.bbsec.xyz")
    # fingerscan('5d6e24694c3e3fdb872e596c',"http://blog.zzp198.cn")
    fingerscan('5d7c96f15ded2c3496c7d368',"http://www.freebuf.com")

