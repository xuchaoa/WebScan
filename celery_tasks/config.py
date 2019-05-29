#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-5-18 上午8:59
# @Author  : Archerx
# @Site    : https://blog.ixuchao.cn
# @File    : config.py
# @Software: PyCharm

from celery.schedules import crontab
from datetime import timedelta

# BROKER_URL = "redis://:SDUTctf@10.6.65.231:6379/2"
# CELERY_BROKER_URL = "redis://:SDUTctf@10.6.65.231:6379/2"
# CELERY_RESULT_BACKEND = 'redis://:SDUTctf@10.6.65.231:6379/3'

BROKER_URL= 'amqp://admin:sdutsec@10.6.65.231:5672/xscan'

# CELERY_RESULT_BACKEND= 'amqp://admin:sdutsec@10.6.65.231:5672/xscan'

CELERY_ACCEPT_CONTENT = ['json']


# 设定 Celery 时区
CELERY_TIMEZONE = 'Asia/Shanghai'

#导入任务文件
# CELERY_IMPORTS = [
#     "celery_tasks.SendCode.tasks",  # 导入py文件
#     # "celery_task.epp_scripts.test2",
# ]


# 配置定时任务
CELERYBEAT_SCHEDULE = {
    "schedule-test": {
        "task": "celery_tasks.SendCode.tasks.test",  #执行的函数
        "schedule": timedelta(seconds=2),   # every minute 每分钟执行
        "args": ()  # # 任务函数参数
    },

    # "test2": {
    #     "task": "celery_task.epp_scripts.test2.celery_run",
    #     "schedule": crontab(minute=0, hour="*/1"),   # every minute 每小时执行
    #     "args": ()
    # },

}
