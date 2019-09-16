#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 8/2/19 3:20 PM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : configparser.py


from configparser import ConfigParser
from lib.core.data import paths



class ConfigFileParser:
    @staticmethod
    def _get_option(section, option):
        try:
            cf = ConfigParser()
            cf.read(paths.CONFIG_FILE)
            return cf.get(section=section, option=option)
        except:
            print('Missing essential options, please check your config-file.')
            return ''

    def ZoomEyeEmail(self):
        return self._get_option('zoomeye', 'email')

    def ZoomEyePassword(self):
        return self._get_option('zoomeye', 'password')

    def fofa_email(self):
        return self._get_option('fofa', 'email')

    def fofa_key(self):
        return self._get_option('fofa', 'key')

    def shodan_apikey(self):
        return self._get_option('shodan', 'api_key')

    def censys_UID(self):
        return self._get_option('censys', 'UID')

    def censys_SECRET(self):
        return self._get_option('censys', 'SECRET')

    def proxy(self):
        return self._get_option('proxy', 'proxy')
