#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 8/1/19 8:36 PM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : setting.py


import os,sys

ESSENTIAL_MODULE_METHODS = 'poc'

IS_WIN = True if (sys.platform in ["win32", "cygwin"] or os.name == "nt") else False

def get_all_poc():
    poc_list = []
    for name in poc_finger.values():

poc_path = {
    'system/redis/':['redis_unauth'],
    'system/mongo/':['mongodb'],
    'cms/discuz/':['discuz_focus_flashxss','discuz_forum_message_ssrf','discuz_plugin_ques_sqli','discuz_x25_path_disclosure'],
    'cms/others/':['coremail_source_leak','fastadmin_weak','onethink_category_sqli','seeyon','source_leak_check'],
    'cms/phpmyadmin/':['phpmyadmin_setup_lfi'],
    'cms/phpstudy/':['phpstudy_phpmyadmin_defaultpwd','phpstudy_probe'],
    'cms/thinkphp/':['thinkphp_rce','onethink_category_sqli','thinkphp_code_exec','thinkphp_v5_exec'],
    'cms/typecho/':['typecho_install_code_exec'],
    'cms/weblogic/':['weblogic_ssrf','weblogic_weak_pass','weblogic_xmldecoder_exec','weblogic_2019_48814'],
    'cms/wordpress/':['wp_social_warfare_rce','wordpress_admin_ajax_filedownload','wordpress_display_widgets_backdoor',
                    'wordpress_plugin_azonpop_sqli','wordpress_plugin_mailpress_rce','wordpress_plugin_ShortCode_lfi',
                    'wordpress_restapi_sqli','wordpress_url_redirect','wordpress_woocommerce_code_exec'],
    'cms/dedecms/':['dedecms_download_redirect','dedecms_error_trace_disclosure','dedecms_recommend_sqli','dedecms_search_typeArr_sqli',
                  'dedecms_version'],
    'cms/phpcms/':['phpcms_v9_file_upload']
}

poc_finger = {
    'redis:6379':['redis_unauth'],
    'weblogic:7001':['weblogic_ssrf','weblogic_weak_pass','weblogic_xmldecoder_exec','weblogic_2019_48814'],
    'thinkphp:80':['thinkphp_rce','onethink_category_sqli','thinkphp_code_exec','thinkphp_v5_exec'],
    'wordpress:80':['wp_social_warfare_rce','wordpress_admin_ajax_filedownload','wordpress_display_widgets_backdoor',
                    'wordpress_plugin_azonpop_sqli','wordpress_plugin_mailpress_rce','wordpress_plugin_ShortCode_lfi',
                    'wordpress_restapi_sqli','wordpress_url_redirect','wordpress_woocommerce_code_exec'],
    'mongo:27017':['mongodb'],
    'discuz:80':['discuz_focus_flashxss','discuz_forum_message_ssrf','discuz_plugin_ques_sqli','discuz_x25_path_disclosure'],
    'phpmyadmin:80':['phpmyadmin_setup_lfi'],
    'typecho:80':['typecho_install_code_exec'],
    'phpstudy:80':['phpstudy_phpmyadmin_defaultpwd','phpstudy_probe'],
    'dedecms:80':['dedecms_download_redirect','dedecms_error_trace_disclosure','dedecms_recommend_sqli','dedecms_search_typeArr_sqli',
                  'dedecms_version'],
    'phpcms:80':['phpcms_v9_file_upload'],
    'x_others:999999':['redis_unauth','coremail_source_leak','fastadmin_weak','seeyon','source_leak_check']

}