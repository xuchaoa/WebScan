#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-5-18 上午8:59
# @Author  : Archerx
# @Site    : https://blog.ixuchao.cn
# @File    : main.py
# @Software: PyCharm

from celery import Celery
from . import config

# 为celery使用django配置文件进行设置，根据自己项目设置
# import os
# if not os.getenv('DJANGO_SETTINGS_MODULE'):
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WebScan.settings")

# 创建celery应用
app = Celery(main='celery_tasks')

# 导入celery配置
app.config_from_object(config)

# 自动注册celery任务
# app.autodiscover_tasks(['celery_tasks.SendCode'])

# app.start(argv=['celery', 'worker', '-l', 'info', '-f', 'logs/celery.log'])
# app.start(argv=['celery', 'worker', '-l', 'info', '-l', 'info'])

import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration

sentry_sdk.init("http://4a1bad6dbac74432b238b0f529c25070@192.168.23.128:9000/2", integrations=[CeleryIntegration()])