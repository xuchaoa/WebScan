#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/25 下午 05:15
# @Author  : Archerx
# @Site    : https://blog.ixuchao.cn
# @File    : pocsuite_test.py
# @Software: PyCharm

from pocsuite3.api import init_pocsuite
from pocsuite3.api import start_pocsuite
from pocsuite3.api import get_results


def run_pocsuite():
    # config 配置可参见命令行参数， 用于初始化 pocsuite3.lib.core.data.conf
    config = {
        'url': '123.207.176.60',
        'poc': 'ssh_burst',
        'mode':'attack',
    }

    init_pocsuite(config)
    start_pocsuite()
    result = get_results()
    print(result)
    print(1)

if __name__ == '__main__':
    run_pocsuite()