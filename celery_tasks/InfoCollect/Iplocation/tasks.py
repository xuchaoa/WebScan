#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/7/28 下午9:40
# @Author  : Archerx
# @Site    : https://blog.ixuchao.cn
# @File    : tasks.py
# @Software: PyCharm

import os
import requests
import json
import geoip2.database
import ipaddress
from conf.global_config import GEOLITE_CITY_DB

'''
判断ip地理位置
'''


def taobao_api(arg):
    api = "http://ip.taobao.com/service/getIpInfo.php?ip={0}".format(arg)
    try:
        r = requests.get(api)
    except Exception as e:
        return False
    if r.status_code != 200:
        return False
    jsonp = r.text
    data = json.loads(jsonp)
    if data.get("data", None):
        d = {
            "country_id": data["data"]["country_id"],
            "country": data["data"]["country"],
            "region": data["data"]["region"]
        }
        return d
    else:
        return False


def geoip(arg):
    reader = geoip2.database.Reader(GEOLITE_CITY_DB)
    response = reader.city(arg)
    d = {
        "country_id": response.country.iso_code,
        "country": response.country.name,
        "region": response.city.name
    }

    return d

def poc(ip):
    if ipaddress.ip_address(ip).is_private:  #判断是否是内网ip
        d = {
            "country_id": "internal icon-disc",
            "country": "Internal Ip",
            "region": ""
        }
        return d
    interface = geoip(ip)
    return interface



if __name__ == '__main__':
    x = poc('123.207.155.221')
    print(x)

    print(ipaddress.ip_address('192.168.89.4').is_private)
