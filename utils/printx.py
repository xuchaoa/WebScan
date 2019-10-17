#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/26/19 5:36 PM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : printx.py

import json


def print_json_format(j):
    format_result = json.dumps(j, sort_keys=True, indent=4, separators=(',', ':'))
    print(format_result)
