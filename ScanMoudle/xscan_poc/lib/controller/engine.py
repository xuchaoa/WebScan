#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/31/19 7:30 PM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : engine.py

# import sys
# sys.path.append('/home/archerx/PycharmProjects/WebScan/ScanMoudle/xscan-poc')

import gevent
import importlib.util
from setting import ESSENTIAL_MODULE_METHODS
from lib.core.data import conf, xscan, scan_option
import sys
import os
import time
import threading
from lib.core.enum import POC_RESULT_STATUS
import json


def initEngine():
    load_module()
    xscan.result = []
    xscan.thread_mode = True if conf.engine_mode == "multi_threaded" else False
    xscan.target = conf.target
    xscan.scan_count = xscan.found_count = 0
    xscan.is_continue = True

    if xscan.target.qsize() < conf.concurrent_num:
        xscan.current_tc_count = xscan.thread_coroutine_num = xscan.target.qsize()
    else:
        xscan.current_tc_count = xscan.thread_coroutine_num = conf.concurrent_num
    xscan.start_time = time.time()


def load_module():
    global scan_poc
    # print(ESSENTIAL_MODULE_METHODS,conf.module_path)
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

def set_thread_lock():
    # xscan.print_screen_lock = threading.Lock()
    xscan.found_count_lock = threading.Lock()
    xscan.scan_conut_lock = threading.Lock()
    xscan.current_tc_count_lock = threading.Lock()
    # xscan.x = threading.Lock()

def change_scan_count(num):
    if xscan.thread_mode:
        xscan.scan_conut_lock.acquire()
    xscan.scan_count += num
    if xscan.thread_mode:
        xscan.scan_conut_lock.release()

def change_found_count(num):
    if xscan.thread_mode:
        xscan.found_count_lock.acquire()
    xscan.found_count += num
    if xscan.thread_mode:
        xscan.found_count_lock.release()

def change_current_tc_count(num):
    if xscan.thread_mode:
        xscan.current_tc_count_lock.acquire()
    xscan.current_tc_count += num
    if xscan.thread_mode:
        xscan.current_tc_count_lock.release()

def result_handle(result, target):
    if not result or result is POC_RESULT_STATUS.FAIL:
        return
    elif result is POC_RESULT_STATUS.RETRAY:  #result == 2
        change_scan_count(-1)
        xscan.target.put(target)
        return

    elif result is True or result is POC_RESULT_STATUS.SUCCESS:
        xscan.result.append(target)  # if vulnerable , add ip to result list
    elif isinstance(result, list):
        for _ in  result:
            xscan.result.append(_)
    else:
        _ = str(result)
        xscan.result.append(_)
    change_found_count(1)

def xpoc():
    while True:
        if xscan.target.qsize() > 0 and xscan.is_continue:
            target = str(xscan.target.get(timeout=1.0))
        else:
            break
        try:
            result = scan_poc(target)
            result_handle(result, target)
        except:
            xscan.is_continue = False
        change_scan_count(1)
    change_current_tc_count(-1)

def run():
    initEngine()
    if xscan.thread_mode:
        set_thread_lock()
        print('nulti thread mode, number is {}'.format(xscan.current_tc_count ))
        for _ in range(xscan.thread_coroutine_num ):
            t = threading.Thread(target=xpoc, name=str(_))
            t.setDaemon(True)
            t.start()
        while xscan.current_tc_count > 0 and xscan.is_continue:
            time.sleep(0.01)
    else:
        print('Coroutine mode, number is {}'.format(xscan.thread_coroutine_num))

        gevent.joinall([gevent.spawn(xpoc) for _ in range(0, xscan.thread_coroutine_num)])

    print('\n')
    msg = '%s found | %s remaining | %s scanned in %.2f seconds' % (
        xscan.found_count, xscan.target.qsize(), xscan.scan_count, time.time() - xscan.start_time)

    print(msg)
    if len(xscan.result) != 0:
        result = {
            scan_option.poc_name: {
                'payload':xscan.result,
                'info':''
            }
        }
        if 'taskID' in scan_option.keys():
            taskID = scan_option.taskID
            from utils.mongo_op import MongoDB
            x = MongoDB()
            x.add_poc_vuln(taskID, json.dumps(result))
        print(result)
    print(xscan.result)
    return xscan.result


