#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 8/8/19 5:18 PM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : complete_publish_test.py

from utils.mongo_op import MongoDB
from celery_tasks.main import app


x = MongoDB()
id = x.add_Ftask()

# app.send_task(name='AliveScan',
#               queue='AliveScan',
#               kwargs=dict(FtaskID=str(id), ip='123.207.155.221', ip_type='single'))

# app.send_task(name='AliveScan',
#               queue='AliveScan',
#               kwargs=dict(FtaskID=str(id), ip='123.207.155.100-123.207.155.200', ip_type='range'))

#149.129.60.133
app.send_task(name='AliveScan',
              queue='AliveScan',
              kwargs=dict(FtaskID=str(id), ip='149.129.60.200-149.129.60.250', ip_type='range'))

# app.send_task(name='AliveScan',
#               queue='AliveScan',
#               kwargs=dict(FtaskID=str(id), ip='123.207.155.221', ip_type='single'))
# app.send_task(name='AliveScan',
#               queue='AliveScan',
#               kwargs=dict(FtaskID=str(id), ip='123.207.155.221', ip_type='single'))
# app.send_task(name='AliveScan',
#               queue='AliveScan',
#               kwargs=dict(FtaskID=str(id), ip='188.131.133.213', ip_type='single'))
# app.send_task(name='SubDomain',
#               queue = 'SubDomain',
#               kwargs=dict(taskID=str(id),domain='baidu.com'))