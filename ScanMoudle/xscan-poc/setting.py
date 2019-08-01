#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 8/1/19 8:36 PM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : setting.py


import os,sys

ESSENTIAL_MODULE_METHODS = 'poc'

IS_WIN = True if (sys.platform in ["win32", "cygwin"] or os.name == "nt") else False