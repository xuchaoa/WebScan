#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/23/19 3:23 PM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : tasks.py



import nmap
# from lib.data import logger
import json


def nmapscan(host, ports):
    '''

    :param host: str
    :param ports: str list
    :return: None or json data
    '''
    # 接受从masscan上扫描出来的结果
    # 为了可以多线程使用，此函数支持多线程调用
    nm = nmap.PortScanner()
    argument = "-sV -sS -Pn --host-timeout 1m -p{}".format(','.join(ports))
    try:
        ret = nm.scan(host, arguments=argument)
    except nmap.PortScannerError as e:
        # logger.debug("Nmap PortScannerError host:{}".format(host))
        print(e)
        return None
    except:
        print('22222')
        return None

    # debug
    elapsed = ret["nmap"]["scanstats"]["elapsed"]
    command_line = ret["nmap"]["command_line"]
    # logger.debug("[nmap] successed,elapsed:%s command_line:%s" % (elapsed, command_line))
    if host in ret["scan"]:
        try:
            result = ret["scan"][host]["tcp"]
        except KeyError:
            return None
        print(result)
        return result
    return None


if __name__ == '__main__':
    nmapscan('123.207.155.221',['80','443','8080','9711','22'])
