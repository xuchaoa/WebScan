#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Archerx


import requests
import os


def fileScan(url,type):
    # with open('../../data/FileScan/')
    filesList = os.listdir('../../../data/FileScan/')
    print(filesList)
    path = '../../../data/FileScan/'

    if type == 'php':
        if type + '.txt' in filesList:
            f = open(path + type + '.txt', 'r', encoding='utf8').read()
            for i in f:
                print(f)
        else:
            return None


if __name__ == '__main__':
    fileScan('1','php')