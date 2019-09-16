#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Archerx

'''
备份文件扫描
'''

import requests
import os
from celery_tasks.main import app
from utils.mongo_op import MongoDB

@app.task(bind=True, name='SFileScan')
def sfileScan(self, taskID, url):
    keywords = ['wwwroot','web','ftp','admin','www']

    listFile = []
    for i in keywords:
        new = "%s.rar" % (i)
        listFile.append(new)
        new = "%s.zip" % (i)
        listFile.append(new)
        new = "%s.tar.gz" % (i)
        listFile.append(new)
        new = "%s.tar" % (i)
        listFile.append(new)

    warning_list = []
    for payload in listFile:
        loads = url + "/" + payload
        # print(loads)
        try:
            header = dict()
            header[
                "User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
            r = requests.head(loads, headers=header, timeout=7)
            if r.status_code != 200:
                continue
            r = requests.get(loads, header=header, timeout=7)
            if r.status_code == 200 and "Content-Type" in r.headers and "application" in r.headers["Content-Type"]:
                warning_list.append(loads)
        except Exception:
            pass

    # In order to  solve the misreport
    if len(warning_list) > 3:
        return False
    print(warning_list)
    x = MongoDB()
    x.add_sensitive_file(taskID, warning_list)
    return warning_list   #


if __name__ == '__main__':
    sfileScan('http://binarysec.top')  #add the http:// protocol