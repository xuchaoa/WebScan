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
