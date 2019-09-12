#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/12/19 8:49 PM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : wappalyzer-test.py

from python3_wappalyzer.Wappalyzer import Wappalyzer, WebPage

wappalyzer = Wappalyzer.latest()
webpage = WebPage.new_from_url('https://blog.ixuchao.cn')
res = wappalyzer.analyze(webpage)
print(res)
