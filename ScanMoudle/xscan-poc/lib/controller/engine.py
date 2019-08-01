#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/31/19 7:30 PM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : engine.py

import importlib.util
from setting import ESSENTIAL_MODULE_METHODS
from lib.core.data import conf, xscan
import sys
import os

def initEngine():
    load_module()
    xscan.result = []
    xscan.thread_mode = True if conf.engine_mode == "multi_threaded" else False
    xscan.target = conf.target
    xscan.scan_count = xscan.found_count = 0
    xscan.is_continue = True

    if xscan.target.qsize() < conf.concurrent_num:
        xscan.concurrent_count = xscan.thread_coroutine_num = xscan.target.qsize()
    else:
        xscan.concurrent_count = xscan.thread_coroutine_num = conf.concurrent_num





def load_module():
    global module
    try:
        module_spec = importlib.util.spec_from_file_location(ESSENTIAL_MODULE_METHODS,conf.module_path)
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        #TODO to change the method
        scan_poc = module.poc
    except Exception as e:
        msg = "[-] Your current script [%s.py] caused this exception\n%s\n%s" % (os.path.basename(conf.module_path),
              '[Error Msg]: ' + str(e), 'Maybe you can download this module from pip or easy_install')
        print(msg)
        sys.exit(0)

def run():
    initEngine()
