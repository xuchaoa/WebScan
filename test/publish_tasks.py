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

# app.send_task(name='PortScan',
#               queue='PortScan',
#               kwargs=dict(taskID='5d3ac102dd76c2600d6fbc9c', host='123.207.155.221'))
#

# queque指定任务推到哪个队列,如果不存在Rabbitmq会自动创建,不需要指定routing_key 直接添加到相应队列,无此参数默认celery队列
# name 是任务名，相当于路由的key


# 缓冲区已经flush而且消息已经确认发送到了RabbitMQ中，关闭链接
# connection.close()

# app.send_task(name='SFileScan',
#               queue = 'SFileScan',
#               kwargs=dict(taskID='5d7a2f0ccb102ff5bce42782', url='https://binarysec.top'))

# app.send_task(name='FuzzDomain',
#               queue = 'FuzzDomain',
#               kwargs=dict(DOMAIN='ixuchao.cn', MAX_LEVEL=1, THREADS=30))

#
# app.send_task(name='ServScan',
#               queue = 'ServScan',
#               kwargs=dict(host='123.207.155.221', ports=['80','443','8080','9711','22']))

# app.send_task(name='SubDomain',
#               queue = 'SubDomain',
#               kwargs=dict(taskID='5d7a01bc39630c1e8954230e',domain='baidu.com'))
#
# app.send_task(name='testscan',
#               queue = 'testscan')

# app.send_task(name='IpLocation',
#               queue = 'IpLocation',
#               kwargs=dict(taskID='5d3edfd675f097ac6ee499c6',ip='123.207.155.221'))

# app.send_task(name='HydraBrute',
#               queue = 'HydraBrute',
#               kwargs=dict(taskID='', username='dict', dict='small', host='149.129.60.179', port='22', service='ssh')
#               )

app.send_task(name='HydraBrute',
              queue = 'HydraBrute',
              kwargs=dict(taskID='5d9de69076b4eddcbbefeaf0', username='dict', dict='small', host='149.129.89.151', port='22', service='ssh'),
              )
# app.send_task(name='HydraBrute',
#               queue = 'HydraBrute',
#               kwargs=dict(taskID='5d7e32de6846c2a6b6fc1291', username='dict', dict='small', host='127.0.0.1', port='6379', service='redis'),
#               )

# app.send_task(name='AliveScan',
#               queue='AliveScan',
#               kwargs=dict(FtaskID='5d7e306dbc4f8c642bde8a2d',ip='123.207.155.210-123.207.155.221', ip_type='range'))
# #
# app.send_task(name='AliveScan',
#               queue='AliveScan',
#               kwargs=dict(FtaskID='5d7e306dbc4f8c642bde8a2d', ip='149.129.89.220/24', ip_type='mask'))


# app.send_task(name='PortServScan',
#               queue='PortServScan',
#               kwargs=dict(taskID='5d7a2f0ccb102ff5bce42783',ip_addr='192.168.23.1', resp='syn_normal'))

# app.send_task(name='ServInfo',
#               queue='ServInfo',
#               kwargs=dict(taskID='5d6e24694c3e3fdb872e596c',url='https://blog.ixuchao.cn'))
#
# app.send_task(name='CmsFinger',
#               queue='CmsFinger',
#               kwargs=dict(taskID='5d7c96f15ded2c3496c7d368',url='blog.zzp198.cn'))
#
# app.send_task(name='CmsFinger',
#               queue='CmsFinger',
#               kwargs=dict(taskID='5d7c96f15ded2c3496c7d368',url='188.131.133.213'))

# app.send_task(name='Wappalyzer',
#               queue = 'Wappalyzer',
#               kwargs=dict(taskID='5d7a2f0ccb102ff5bce42782', domain='123.207.155.221')
#               )

# app.send_task(name='PortScan',
#               queue = 'PortScan',
#               kwargs=dict(taskID='5d7a2f0ccb102ff5bce42782', host='192.168.232.112')
#               )

# app.send_task(name='DirScan',
#               queue = 'DirScan',
#               kwargs=dict(taskID='5d7a2f0ccb102ff5bce42782', target='https://blog.ixuchao.cn')
#               )

# app.send_task(name='RDPassSpray',
#               queue='RDPassSpray',
#               kwargs=dict(taskID='5d7a2f0ccb102ff5bce42783',target='10.0.83.217'))