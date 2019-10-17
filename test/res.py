#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/25/19 8:11 PM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : res.py

import re

if re.search('mongo','Mongo',re.I):
    print(True)

a = {
    'a':'b'
}
if isinstance(a,dict):
    print('aaa')