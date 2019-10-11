#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-5-18 上午8:59
# @Author  : Archerx
# @Site    : https://blog.ixuchao.cn
# @File    : config.py
# @Software: PyCharm

from celery.schedules import crontab
from datetime import timedelta
from kombu import Queue, Exchange



# BROKER_URL = "redis://:SDUTctf@10.6.65.231:6379/2"
# CELERY_BROKER_URL = "redis://:SDUTctf@10.6.65.231:6379/2"
# CELERY_RESULT_BACKEND = 'redis://:SDUTctf@10.6.65.231:6379/3'


# BROKER_URL= 'amqp://admin:sdutsec@192.168.2.108:5672/xscan'
BROKER_URL= 'amqp://admin:sdutsec@127.0.0.1:5672/xscan'

# CELERY_RESULT_BACKEND= 'amqp://admin:sdutsec@10.6.65.231:5672/xscan'

CELERY_ACCEPT_CONTENT = ['json']

# 设定 Celery 时区
CELERY_TIMEZONE = 'Asia/Shanghai'


# 任务 ACK 确认机制，防止 Task 在处理时程序异常导致 Task 丢失的问题
CELERY_ACKS_LATE = True
# 并发任务数量
CELERYD_CONCURRENCY = 2
# 每个worker最多执行20个任务就会被销毁，可防止内存泄露
CELERYD_MAX_TASKS_PER_CHILD = 1
# 单个任务的运行时间不超过此值，否则会被SIGKILL 信号杀死
CELERYD_TASK_TIME_LIMIT = 600

# 任务发出后，经过一段时间还未收到acknowledge , 就将任务重新交给其他worker执行
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 600}
# 忽略 Task 处理程序的返回结果，结果直接在处理程序中连接后端数据库进行处理
CELERY_IGNORE_RESULT = True

# # 处理程序从任务队列预加载的待处理任务数
CELERYD_PREFETCH_MULTIPLIER = 0

BROKER_HEARTBEAT = 0  # 解决Debug中的 #1

# # 任务发出后，经过一段时间还未收到acknowledge , 就将任务重新交给其他worker执行
# CELERY_DISABLE_RATE_LIMITS = False

# 设置默认,当没有微任务指定队列时,推到默认队列
CELERY_DEFAULT_QUEUE = 'xscan'
CELERY_DEFAULT_ROUTING_KEY = 'xscan'

# work不指定queque启动时会默认监听的队列，同时会自动绑定key和queue
CELERY_QUEUES = (
    Queue("PortScan", Exchange("xscan",type='direct'),routing_key='PortScan'),
    Queue("ServScan", Exchange("xscan",type='direct'),routing_key='ServScan'),
    Queue("SubDomain", Exchange("xscan",type='direct'),routing_key='SubDomain'),
    Queue("IpLocation", Exchange("xscan",type='direct'),routing_key='IpLocation'),
    Queue("AliveScan", Exchange("xscan",type='direct'),routing_key='AliveScan'),
    Queue("PortServScan", Exchange("xscan",type='direct'),routing_key='PortServScan'),
    Queue("HydraBrute", Exchange("xscan_brute",type='direct'),routing_key='HydraBrute'),
    Queue("RDPassSpray", Exchange("xscan_brute",type='direct'),routing_key='RDPassSpray'),
    Queue("SFileScan", Exchange("xscan_web",type='direct'),routing_key='SFileScan'),
    Queue("ServInfo", Exchange("xscan_web",type='direct'),routing_key='ServInfo'),
    Queue("CmsFinger", Exchange("xscan_web",type='direct'),routing_key='CmsFinger'),
    Queue("Wappalyzer", Exchange("xscan_web",type='direct'),routing_key='Wappalyzer'),
    Queue("DirScan", Exchange("xscan_web",type='direct'),routing_key='DirScan'),
    Queue("Struts2Scan", Exchange("xscan_web",type='direct'),routing_key='Struts2Scan'),

    # Queue('portsca',Exchange("xscan",type='direct'), routing_key='portsca'),
    )


CELERY_ROUTES = {
    'celery_tasks.SendCode.tasks.test':{'queue':'test', 'routing_key':'xx'},  #send_task时指定队列,则该配置被忽略.
    # 'task.reduce':{'queue':'queue_reduce', 'routing_key':'queue_sum'},
}

#导入任务文件

CELERY_IMPORTS = [
    "celery_tasks.WebScan.SFileScan.tasks",
    "celery_tasks.WebScan.ServInfo.tasks",
    "celery_tasks.WebScan.CmsFinger.tasks",
    "celery_tasks.WebScan.Wappalyzer.tasks",
    "celery_tasks.WebScan.DirScan.tasks",
    "celery_tasks.WebScan.Struts2Scan.Struts2Scan",
    # "celery_tasks.TargetCollect.fuzzdomain.tasks",
    "celery_tasks.InfoCollect.PortScan.tasks",
    "celery_tasks.InfoCollect.ServScan.tasks",
    "celery_tasks.InfoCollect.PortServScan.tasks",
    "celery_tasks.TargetCollect.subdomain3.tasks",
    "celery_tasks.InfoCollect.IpLocation.tasks",
    "celery_tasks.WeakBrute.hydra.tasks",
    "celery_tasks.WeakBrute.RDPassSpray.RDPassSpray",
    "celery_tasks.TargetCollect.AliveScan.tasks",
    # "celery_task.epp_scripts.test2",
]




CELERYBEAT_SCHEDULE = {
    "schedule-test": {
        "task": "testscan",  #执行的函数
        "schedule": timedelta(seconds=2),   # every minute 每分钟执行
        "args": () , # # 任务函数参数
        "options":{'queue':'testscan','routing_key':'testscan'}
    },

    # "test2": {
    #     "task": "celery_task.epp_scripts.test2.celery_run",
    #     "schedule": crontab(minute=0, hour="*/1"),   # every minute 每小时执行
    #     "args": ()
    # },

}
