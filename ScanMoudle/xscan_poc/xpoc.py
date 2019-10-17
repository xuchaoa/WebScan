#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/31/19 10:38 AM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : xpoc.py
# modify from POC-T Proj by Archerx

# xpoc将作为一个单独可运行的组件，和主调度引擎之间耦合度很小,方便单独拿出来用

import os, sys
from conf.global_config import XPOC_PATH
sys.path.append(XPOC_PATH)

from gevent import monkey
monkey.patch_all()
import os
from ScanMoudle.xscan_poc.lib.core.common import set_paths
from ScanMoudle.xscan_poc.lib.core.data import scan_option, xscan
from ScanMoudle.xscan_poc.lib.core.option import init_options
from ScanMoudle.xscan_poc.lib.controller.engine import run
from setting import poc_finger, get_all_poc
import re

def module_path():
    return os.path.dirname(os.path.realpath(__file__))

def finger_load_poc_and_run(taskID, ip, keyword=None, port=None):
    '''
    此入口函数只能进行 单ip 多poc
    选择payload以keyword为准。
    :param ip:
    :param keyword:
    :param port:
    :return:
    '''
    poc_list = set()
    if keyword is not None:
        for keys in poc_finger.keys():
            if re.search(keys.split(':')[0], keyword, re.I):
            # if keys.split(':')[0] in keyword:
                poc_list.update(poc_finger[keys])
    if port is not None:
        for keys in poc_finger.keys():
            if keys.split(':')[1] == '222':
                poc_list.update(poc_finger[keys])
    # 服务不是标准端口也可以检测，同时为防止漏报依旧匹配端口
    if len(poc_list) == 0:
        # poc_list = poc_finger['x_others:999999']
    ## 匹配不到直接暴力跑所有poc
        poc_list = get_all_poc()
    print(poc_list)
    for _ in poc_list:
        if port is not None:
            main( poc_name=_, target_single=ip + ':' + port , taskID=taskID)
        else:
            main(poc_name=_, target_single=ip, taskID=taskID)

def main(poc_name=None, taskID=None, target_single=None, target_range=None, target_network=None, zoomeye_dork=None, shodan_dork=None, fofa_dork=None,
         engine_thread=False, concurrent_num=100, censys_dork=None, search_type=None, proxy=None, api_limit=100, api_offset=0):
    try:
        set_paths(module_path())

        # x = {'engine_thread': False, 'concurrent_num': 100, 'poc_name': 'weblogic_2019_48814',
        #      'target_single': '', 'target_range': '', 'target_network': '', 'zoomeye_dork': 'weblogic',
        #      'shodan_dork': '', 'fofa_dork': '', 'censys_dork': '', 'api_limit': 50, 'api_offset': 0, 'search_type': 'host',
        #      'output_path': '', 'logging_level': 0, 'proxy': ''}
        # x = {'engine_thread': False, 'concurrent_num': 100, 'poc_name': 'poc',
        #      'target_single': '', 'target_range': '', 'target_network': '', 'zoomeye_dork': '',
        #      'shodan_dork': 'phpcms', 'fofa_dork': '', 'censys_dork': '', 'api_limit': 100, 'api_offset': 0,
        #      'search_type': '', 'proxy': ''}
        x = {'engine_thread': engine_thread, 'concurrent_num': concurrent_num, 'poc_name': poc_name,
             'target_single': target_single, 'target_range': target_range, 'target_network': target_network, 'zoomeye_dork': zoomeye_dork,
             'shodan_dork': shodan_dork, 'fofa_dork': fofa_dork, 'censys_dork': censys_dork, 'api_limit': api_limit, 'api_offset': api_offset,
             'search_type': search_type, 'proxy': proxy}
        if taskID is not None:
            scan_option.taskID = taskID
        scan_option.update(x)
        init_options(scan_option)
        run()
    except Exception as e:
        print(e)
        pass
    finally:
        print('done')

if __name__ == '__main__':
    # main()
    # finger_load_poc_and_run('5d9f404daf1af103b9e0de2c','127.0.0.1','mongo')
    finger_load_poc_and_run('5d7a2f0ccb102ff5bce42783','127.0.0.1', keyword='mongo')
