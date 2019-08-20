#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@Author: xxlin
@LastEditors: ttttmr
@Date: 2019-04-10 13:27:58
@LastEditTime: 2019-05-29 16:52:42
'''


import queue
import sys


from lib.controller.bruter import loadConf
from lib.core.common import parseTarget
from lib.core.data import conf, paths


def initOptions(args):
    EngineRegister(args)
    BruterRegister(args)
    TargetRegister(args)


def EngineRegister(args):
    """
    加载并发引擎模块
    """
    conf.engine_mode = 'coroutine'

    #设置线程数
    if args.thread_num > 200 or args.thread_num < 1:
        conf.thread_num = 30
        return
    conf.thread_num = args.thread_num

def BruterRegister(args):
    """
    配置bruter模块
    """

    if args.load_config_file:
        #加载配置文件
        loadConf()
    else:
        print("[+] Function development, coming soon!please use -lcf parameter")
        sys.exit()

def TargetRegister(args):
    """
    加载目标模块
    """
    msg = '[*] Initialize targets...'
    print(msg)

    #初始化目标队列
    conf.target = queue.Queue()

    # 用户输入入队
    if args.target_input:
        # 尝试解析目标地址
        try:
            lists = parseTarget(args.target_input)
        except:
            helpmsg = "Invalid input in [-i], Example: -i [http://]target.com or 192.168.1.1[/24] or 192.168.1.1-192.168.1.100"
            print(helpmsg)
            sys.exit()


        msg = '[+] Load targets from: %s length is %s' % (args.target_input, len(lists))
        print(msg)
        # save to conf
        for target in lists:
            conf.target.put(target)
        conf.target_nums = conf.target.qsize()
