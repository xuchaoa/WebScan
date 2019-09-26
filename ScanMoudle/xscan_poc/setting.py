#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 8/1/19 8:36 PM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : setting.py


import os,sys

ESSENTIAL_MODULE_METHODS = 'poc'

IS_WIN = True if (sys.platform in ["win32", "cygwin"] or os.name == "nt") else False

poc_finger = {
    'redis:6379':['redis_unauth'],
    'weblogic:7001':['weblogic_ssrf','weblogic_weak_pass','weblogic_xmldecoder_exec','weblogic_2019_48814'],
    'thinkphp:80':['thinkphp_rce','onethink_category_sqli','thinkphp_code_exec','thinkphp_v5_exec'],
    'wordpress:80':['wp_social_warfare_rce'],
    'mongo:27017':['mongodb'],
    'discuz:80':['discuz_focus_flashxss','discuz_forum_message_ssrf','discuz_plugin_ques_sqli','discuz_x25_path_disclosure'],
    'phpmyadmin:80':['phpmyadmin_setup_lfi'],
    'typecho:80':['typecho_install_code_exec'],
    'phpstudy:80':['phpstudy_phpmyadmin_defaultpwd','phpstudy_probe'],
    'x_others:999999':['redis_unauth','coremail_source_leak','fastadmin_weak','seeyon','source_leak_check']

}