#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/31/19 4:59 PM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : option.py

import sys
from lib.core.data import conf
import os
from lib.core.data import paths
import queue
from lib.core.common import ip_range_to_list
import ipaddress


def init_options(scan_option):
    engine_register(scan_option)
    poc_register(scan_option)
    target_register(scan_option)

def  engine_register(args):

    if args.engine_thread:
        conf.engine_mode = "multi_threaded"
    else:
        conf.engine_mode = "coroutine"

    # set concurrent number
    if args.concurrent_num > 1000 or args.concurrent_num < 1:
        print('concurrent number is not allow , auto turn to num 100')
        conf.concurrent_num = 100
    else:
        conf.concurrent_num = args.concurrent_num

def poc_register(args):
    if not args.poc_name:
        print("no poc name ")
        return
    conf.module_path = os.path.abspath(os.path.abspath(os.path.join(paths.POC_PATH, args.poc_name + '.py')))

def target_register(args):
    conf.target = queue.Queue()

    if args.target_single:
        conf.target.put(args.target_single)
    elif args.target_range:
        try:
            list = ip_range_to_list(args.target_range)
            for _ in list:
                conf.target.put(_)
        except:
            pass
    # ip/mask e.g. 192.168.1.2/24
    elif args.target_network:
        try:
            ip_range = ipaddress.ip_network(args.target_network, strict=False)
            for ip in ip_range.hosts():
                conf.target.put(ip)
        except:
            pass
    else:
        conf.limit = args.api_limit
        conf.offset = args.api_offset

        if args.zoomeye_dork:
            from lib.api.zoomeye import handle_zoomeye
            conf.search_type = args.search_type
            handle_zoomeye(query=args.zoomeye_dork, limit=conf.limit, type=conf.search_type, offset = conf.offset)
        elif args.fofa_dork:
            from lib.api.fofa import handle_fofa
            handle_fofa(query=args.fofa_dork, limit=conf.limit, offset=conf.offset)
        elif args.shodan_dork:
            from lib.api.shodan import handle_shodan
            handle_shodan(query=args.shodan_dork, limit=conf.limit, offset=conf.offset)
        elif args.censys_dork:
            from lib.api.censys import handle_censys
            handle_censys(query=args.censys_dork, limit=conf.limit, offset=conf.offset)




