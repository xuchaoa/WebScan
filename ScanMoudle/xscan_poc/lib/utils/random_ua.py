#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 8/2/19 3:35 PM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : random_ua.py


import random


# random user agent
def get_random_ua():
    first_num = random.randint(55, 75)
    third_num = random.randint(0, 3200)
    fourth_num = random.randint(0, 140)
    os_type = [
        '(Windows NT 6.1; WOW64)',
        '(Windows NT 10.0; WOW64)',
        '(X11; Linux x86_64)',
        '(X11; Linux i686) ',
        '(Macintosh;U; Intel Mac OS X 10_12_6;en-AU)',
        '(iPhone; U; CPU iPhone OS 11_0_6 like Mac OS X; en-SG)',
        '(Windows NT 10.0; Win64; x64; Xbox; Xbox One) ',
        '(iPad; U; CPU OS 11_3_2 like Mac OS X; en-US) ',
        '(Macintosh; Intel Mac OS X 10_14_1)'
    ]
    chrome_version = 'Chrome/{}.0.{}.{}'.format(
        first_num, third_num, fourth_num)

    random_ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
                   '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
                  )
    return random_ua


# random user agent of PC
def get_pc_ua():
    first_num = random.randint(55, 75)
    third_num = random.randint(0, 3200)
    fourth_num = random.randint(0, 140)
    os_type = [
        '(Windows NT 6.1; WOW64)',
        '(Windows NT 10.0; WOW64)',
        '(X11; Linux x86_64)',
        '(X11; Linux i686) ',
        '(Macintosh;U; Intel Mac OS X 10_12_6;en-AU)',
        '(Windows NT 10.0; Win64; x64; Xbox; Xbox One) ',
        '(iPad; U; CPU OS 11_3_2 like Mac OS X; en-US) ',
        '(Macintosh; Intel Mac OS X 10_14_1)'
    ]
    chrome_version = 'Chrome/{}.0.{}.{}'.format(
        first_num, third_num, fourth_num)

    random_ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
                   '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
                  )
    return random_ua

# random user agent of mobile phone
def get_phone_ua():
    first_num = random.randint(55, 75)
    third_num = random.randint(0, 3200)
    fourth_num = random.randint(0, 140)
    os_type = [
    '(iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us)',
    '(iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us)',
    '(Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00)',
    '(Linux; U; Android 8.0.0; zh-cn; Mi Note 7 Build/OPR1.170623.032)',
    ]
    chrome_version = 'Chrome/{}.0.{}.{}'.format(
        first_num, third_num, fourth_num)

    random_ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
                   '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
                  )
    return random_ua
