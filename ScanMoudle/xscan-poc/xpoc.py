#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/31/19 10:38 AM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : xpoc.py
# modify from POC-T Proj by Archerx
# xpoc将作为一个单独可运行的组件，和主调度引擎之间耦合度很小,方便单独拿出来用

from gevent import monkey
monkey.patch_all()
import os
from lib.core.common import set_paths
from lib.core.data import scan_option
from lib.core.option import init_options
from lib.controller.engine import run

def module_path():
    return os.path.dirname(os.path.realpath(__file__))

def main():
    try:
        set_paths(module_path())

        # x = {'engine_thread': False, 'concurrent_num': 100, 'poc_name': 'weblogic_2019_48814',
        #      'target_single': '', 'target_range': '', 'target_network': '', 'zoomeye_dork': 'weblogic',
        #      'shodan_dork': '', 'fofa_dork': '', 'censys_dork': '', 'api_limit': 50, 'api_offset': 0, 'search_type': 'host',
        #      'output_path': '', 'logging_level': 0, 'proxy': ''}
        x = {'engine_thread': False, 'concurrent_num': 100, 'poc_name': 'redis_unauth',
             'target_single': '114.113.112.182:4000', 'target_range': '', 'target_network': '', 'zoomeye_dork': '',
             'shodan_dork': '', 'fofa_dork': '', 'censys_dork': '', 'api_limit': 100, 'api_offset': 0,
             'search_type': '', 'proxy': ''}
        scan_option.update(x)
        init_options(scan_option)
        run()
    except Exception as e:
        print(e)
        pass
    finally:
        print('done')

if __name__ == '__main__':
    main()
