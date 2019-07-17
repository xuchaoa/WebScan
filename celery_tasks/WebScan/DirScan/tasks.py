#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Archerx


import requests
import os


def fileScan(url):
    # with open('../../data/FileScan/')
    filesList = os.listdir('../../../data/FileScan/')
    SFileList = []
    for fi in filesList:
        SFileList.append('../../../data/FileScan/' + fi)
    f = open('../../../data/FileScan/php.txt','r',encoding='utf8').read()
    for i in f:
        print(f)


if __name__ == '__main__':
    fileScan('1')