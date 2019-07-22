#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/30 下午3:43
# @Author  : Archerx
# @Site    : https://blog.ixuchao.cn
# @File    : publish_tasks.py
# @Software: PyCharm

import pika
import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from celery_tasks.main import app

# # ######################### 生产者 #########################
# credentials = pika.PlainCredentials('admin', 'sdutsec')
# #链接rabbit服务器（localhost是本机，如果是其他服务器请修改为ip地址）
# connection = pika.BlockingConnection(pika.ConnectionParameters('10.6.65.231',5672,'xscan',credentials))
#
# #创建频道
# channel = connection.channel()
# 声明消息队列，消息将在这个队列中进行传递。如果将消息发送到不存在的队列，rabbitmq将会自动清除这些消息。如果队列不存在，则创建
# channel.queue_declare(queue='hello')

# exchange -- 它使我们能够确切地指定消息应该到哪个队列去。
# 向队列插入数值 routing_key是队列名 body是要插入的内容Did you remember to import the module containing this task?
# Or maybe you're using relative imports?
#
# Please see
# http://docs.celeryq.org/en/latest/internals/protocol.html
# for more information.

# app.send_task(name='portscan',
#               queue='portscan',
#               kwargs=dict(host='10.0.85.203',ports='0-65535',rate='5000',))
# queque指定任务推到哪个队列,如果不存在Rabbitmq会自动创建,不需要指定routing_key 直接添加到相应队列,无此参数默认celery队列
# name 是任务名
print("开始队列")
# 缓冲区已经flush而且消息已经确认发送到了RabbitMQ中，关闭链接
# connection.close()

# app.send_task(name='sFileScan',
#               queue = 'sFileScan',
#               kwargs=dict(url='https://binarysec.top'))

app.send_task(name='FuzzDomain',
              queue = 'FuzzDomain',
              kwargs=dict(DOMAIN='ixuchao.cn', MAX_LEVEL=1, THREADS=30))
