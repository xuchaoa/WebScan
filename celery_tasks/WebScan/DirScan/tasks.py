#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/19/19 4:45 PM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : tasks.py

'''
web目录、文件扫描模块
'''

from ScanMoudle.WebDirMap.dirmap import main
from celery_tasks.main import app


@app.task(bind=True,name='DirScan')
def dirscan(self, taskID, target, thread_num=60, load_config_file=True):
    main(taskID, target, thread_num, load_config_file)
