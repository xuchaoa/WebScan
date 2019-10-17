#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@Author: xxlin
@LastEditors: xxlin
@Date: 2019-04-10 13:27:59
@LastEditTime: 2019-05-01 17:57:11
'''

import os, sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)


from gevent import monkey
monkey.patch_all()
from lib.controller.engine import run
from lib.core.common import setPaths
from lib.core.data import cmdLineOptions, conf, paths, result
from lib.core.option import initOptions
from utils.mongo_op import MongoDB
# from lib.parse.cmdline import cmdLineParser




def main(taskID, target, thread_num, load_config_file):
    """
    main fuction of dirmap 
    """

    # set paths of project 
    paths.ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
    setPaths()

    scan_param = {
        'thread_num': thread_num,
        'target_input': target,  # single or range or mask
        'target_file': '',
        'load_config_file': load_config_file,
        'debug': False
    }
    # received command >> cmdLineOptions
    cmdLineOptions.update(scan_param)
    
    # loader script,target,working way(threads? gevent?),output_file from cmdLineOptions
    # and send it to conf
    initOptions(cmdLineOptions) # 扫描中的全部参数放到conf中
    # run!
    run()
    print(result)
    _ = MongoDB()
    _.add_web_dir(taskID, result)
    return result

if __name__ == "__main__":
    main('xx', 'http://123.207.155.221', 30, True)
