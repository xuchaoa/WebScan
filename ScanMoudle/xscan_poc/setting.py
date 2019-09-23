#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 8/1/19 8:36 PM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : setting.py


import os,sys

ESSENTIAL_MODULE_METHODS = 'poc'

IS_WIN = True if (sys.platform in ["win32", "cygwin"] or os.name == "nt") else False

poc_finger = {
    'redis:6379':['redis_unauth'],
    'weblogic:7001':['weblogic_ssrf','weblogic_weak_pass','weblogic_xmldecoder_exec','weblogic_2019_48814'],
    'thinkphp:80':['thinkphp_rce'],
    'wordpress:80':['wp_social_warfare_rce'],
    'others':[]
}