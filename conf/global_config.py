#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/22/19 4:05 PM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : global_config.py

import os

def realjoin(c, d):
    return os.path.realpath(os.path.join(c, d))


PROJECT_PATH = realjoin(__file__,'../../')
print(PROJECT_PATH)

DATA_PATH = realjoin(PROJECT_PATH,'data')
print(DATA_PATH)

FUZZDOMAIN_PATH = realjoin(DATA_PATH,'fuzzdomain_dic')
FUZZDOMAIN_DIC_NORMAL = realjoin(FUZZDOMAIN_PATH,'normal.txt')
FUZZDOMAIN_DIC_SMALL = realjoin(FUZZDOMAIN_PATH,'small.txt')

print(FUZZDOMAIN_DIC_SMALL)