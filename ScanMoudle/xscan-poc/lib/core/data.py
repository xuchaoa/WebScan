#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/31/19 10:50 AM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : data.py


from .datatype import AttribDict


paths = AttribDict()

scan_option = AttribDict()   #扫描传入的参数

conf = AttribDict()     #扫描过程中的配置

xscan = AttribDict()    #扫面引擎的参数
