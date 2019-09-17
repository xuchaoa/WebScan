#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 8/9/19 7:47 PM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : redis_unauth.py


import socket

def poc(url):
    # url = host2IP(url)  # 自动判断输入格式,并将URL转为IP
    port = int(url.split(':')[-1]) if ':' in url else 6379  # 不指定端口则为默认端口
    payload = b'\x2a\x31\x0d\x0a\x24\x34\x0d\x0a\x69\x6e\x66\x6f\x0d\x0a'
    s = socket.socket()
    socket.setdefaulttimeout(10)
    try:
        host = url.split(':')[0]
        s.connect((host, port))
        s.send(payload)
        recvdata = s.recv(1024)
        s.close()
        if recvdata and b"redis_version" in recvdata:
            return True
    except Exception:
        pass
    return False
