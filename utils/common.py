#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/19/19 11:38 AM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : common.py


def add_http(url):
    if not url.startswith('http'):
        return 'http://' + url
