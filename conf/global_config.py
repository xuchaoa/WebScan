#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/22/19 4:05 PM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : global_config.py

import os

def realjoin(c, d):
    return os.path.realpath(os.path.join(c, d))


PROJECT_PATH = realjoin(__file__,'../../')
# print(PROJECT_PATH)

DATA_PATH = realjoin(PROJECT_PATH,'data')
# print(DATA_PATH)


### fuzzdomain配置

FUZZDOMAIN_PATH = realjoin(DATA_PATH,'fuzzdomain_dic')
FUZZDOMAIN_DIC_NORMAL = realjoin(FUZZDOMAIN_PATH,'normal.txt')
FUZZDOMAIN_DIC_SMALL = realjoin(FUZZDOMAIN_PATH,'small.txt')

# print(FUZZDOMAIN_DIC_SMALL)

###### SubDomain Setting
SUBDOMAIN_PATH = realjoin(DATA_PATH,'subdomain_dict')
SUBDOMAIN_CDN_SERVER_DICT = realjoin(SUBDOMAIN_PATH, 'cdn_servers.txt')
SUBDOMAIN_NEXT_SUB_FULL_DICT = realjoin(SUBDOMAIN_PATH, 'next_sub_full.txt')
SUBDOMAIN_WYDOMAIN_DICT = realjoin(SUBDOMAIN_PATH, 'wydomain.csv')

##### GeoIp setting
GEOLITE_PATH = realjoin(DATA_PATH,'GeoLite2')
GEOLITE_CITY_DB = realjoin(GEOLITE_PATH, 'GeoLite2-City.mmdb')

##### HydraBrute setting
HYDRADIC_PATH = realjoin(DATA_PATH, 'hydra_dict')
HYDRADIC_SMALL = realjoin(HYDRADIC_PATH, 'weakpass_small.txt')
HYDRADIC_LARGE = realjoin(HYDRADIC_PATH, 'weakpass_large.txt')

USERNAME_DICT = realjoin(HYDRADIC_PATH, 'username_dict')
DIC_USERNAME_FTP = realjoin(USERNAME_DICT, 'dic_username_ftp.txt')
DIC_USERNAME_IMAP = realjoin(USERNAME_DICT, 'dic_username_imap.txt')
DIC_USERNAME_MEMCACHED = realjoin(USERNAME_DICT, 'dic_username_memcached.txt')
DIC_USERNAME_MONGODB = realjoin(USERNAME_DICT, 'dic_username_mongodb.txt')
DIC_USERNAME_MYSQL = realjoin(USERNAME_DICT, 'dic_username_mysql.txt')
DIC_USERNAME_ORACLE = realjoin(USERNAME_DICT, 'dic_username_oracle.txt')
DIC_USERNAME_POP3 = realjoin(USERNAME_DICT, 'dic_username_pop3.txt')
DIC_USERNAME_POSTGRESQL = realjoin(USERNAME_DICT, 'dic_username_postgresql.txt')
DIC_USERNAME_RDP = realjoin(USERNAME_DICT, 'dic_username_rdp.txt')
DIC_USERNAME_REDIS = realjoin(USERNAME_DICT, 'dic_username_redis.txt')
DIC_USERNAME_SMB = realjoin(USERNAME_DICT, 'dic_username_smb.txt')
DIC_USERNAME_SMTP = realjoin(USERNAME_DICT, 'dic_username_smtp.txt')
DIC_USERNAME_SQLSERVER = realjoin(USERNAME_DICT, 'dic_username_sqlserver.txt')
DIC_USERNAME_SSH = realjoin(USERNAME_DICT, 'dic_username_ssh.txt')
DIC_USERNAME_SVN = realjoin(USERNAME_DICT, 'dic_username_svn.txt')
DIC_USERNAME_TELNET = realjoin(USERNAME_DICT, 'dic_username_telnet.txt')
DIC_USERNAME_TOMCAT = realjoin(USERNAME_DICT, 'dic_username_tomcat.txt')
DIC_USERNAME_VNC = realjoin(USERNAME_DICT, 'dic_username_vnc.txt')
DIC_USERNAME_WEBLOGIC = realjoin(USERNAME_DICT, 'dic_username_weblogic.txt')
COMMON_USERNAME = realjoin(USERNAME_DICT, 'common_username.txt')



# 在爆破中，如果一个无效ip多次出现，可以将IP加入到下列表中，程序会在爆破中过滤。
waiting_fliter_ip = [
    '222.221.5.253',
    '222.221.5.252',
    '1.1.1.1'
]

# 速度分为三种模式，可以根据以下配置进行调节
# high
high_segment_num = 10000  # 程序采用逐量放到内存爆破，以减少内存占用。该设置会改变每次的读取量
# medium
medium_segment_num = 5000
# low
low_segment_num = 2000
# 设置一个ip出现的最多次数,后续出现将被丢弃
ip_max_count = 30