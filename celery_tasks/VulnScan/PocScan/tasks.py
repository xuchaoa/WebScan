#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/16/19 8:52 PM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : tasks.py

import os, sys
from conf.global_config import XPOC_PATH
sys.path.append(XPOC_PATH)

from ScanMoudle.xscan_poc.xpoc import finger_load_poc_and_run
from celery_tasks.main import app

@app.task(bind=True,name='PocScan')
def xpoc(self, taskID, ip, keyword=None, port=None):
    finger_load_poc_and_run(taskID, ip , keyword, port)



