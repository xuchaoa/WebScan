#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/12/19 8:49 PM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : wappalyzer.py

'''
Wappalyzer是一款能够分析目标网站所采用的平台构架、网站环境、服务器配置环境、JavaScript框架、编程语言等参数的网站技术分析插件。
'''

from celery_tasks.WebScan.Wappalyzer.wappalyzer.Wappalyzer import Wappalyzer, WebPage
from utils.mongo_op import MongoDB
from celery_tasks.main import app
import requests
requests.packages.urllib3.disable_warnings()

@app.task(bind=True, name='Wappalyzer', max_retries=3)
def wappalyzer(self, taskID, domain):
    if not domain.startswith('http'):
        domain = 'http://' + domain
    wappalyzer = Wappalyzer.latest()
    res = ''
    try:
        webpage = WebPage.new_from_url(domain, verify=False)
        res = wappalyzer.analyze(webpage)
        print(list(res))
        x = MongoDB()
        x.add_wappalyzer(taskID, list(res))
    except requests.exceptions.ConnectTimeout as e:
        print(e)
        app.send_task(name='Wappalyzer',
                      queue='Wappalyzer',
                      kwargs=dict(taskID=taskID, domain=domain),
                      )
    except requests.exceptions.ConnectionError as e:
        # 可能是该主机不存在http服务
        print(e)
        # app.send_task(name='Wappalyzer',
        #               queue='Wappalyzer',
        #               kwargs=dict(taskID=taskID, domain=domain),
        #               )
    except Exception as e:
        print(e)
    return list(res)

if __name__ == '__main__':
    wappalyzer('5d7a2f0ccb102ff5bce42782', '123.207.155.222')