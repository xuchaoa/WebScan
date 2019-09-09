#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-5-26 上午9:19
# @Author  : Archerx
# @Site    : https://blog.ixuchao.cn
# @File    : shell_test.py
# @Software: PyCharm

import os
import subprocess

# result = os.popen('ping -c 5 www.baidu.com')
# a = result.read()
# print(type(a))
# print(a)
#
# print(result.readlines())





# a = subprocess.getstatusoutput('ifconfig')
# print(a)
#
# a = subprocess.getoutput('ifconfig')
# print(a)



# 可同步或者async
# a = subprocess.Popen('ping -c 5 baidu.com',stdout=subprocess.PIPE,shell=True)
# a.wait()
# print(a.stdout.read())
#
# print('over')




# exitcode,result = subprocess.getstatusoutput('ping -c 5 baidu.com')
#
# if exitcode == 0:
#     print(result)


# sudo masscan -p0-65535 10.6.65.231 --rate=5000
shell = 'echo %s | sudo -S %s --rate=5000'%('xuchao','masscan -p0-65535 10.6.65.231 --rate=5000')
s = subprocess.run(shell,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
# print(dir(s))
print(s.stdout.decode())
print(s.returncode)
