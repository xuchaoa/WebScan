#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/22/19 2:55 PM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : PocLoader.py


import os
import importlib

def poc_loader():
    POC_PATH = 'pocs'
    files = os.listdir(POC_PATH)
    pocs = filter(lambda x:not x.startswith("__") and x.endswith(".py"),files)
    poc_name = map(lambda x:x[:-3],pocs)
    poc_list = list(poc_name)
    print(poc_list)
    Plist = []
    for poc in poc_list:
        _ = importlib.import_module(POC_PATH + '.' + poc)
        Plist.append(_)
    for _ in Plist:
        _.test('archerx').pp()


if __name__ == '__main__':
    poc_loader()
    # for i in os.walk('pocs'):
    #     print(i)
