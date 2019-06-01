#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/31 下午9:33
# @Author  : Archerx
# @Site    : https://blog.ixuchao.cn
# @File    : fabfile.py.py
# @Software: PyCharm

from fabric.api import local, env, roles, cd , run
from fabric.api import *

def prepare_deploy():
    local('echo "hello"')

#必须先在这里指定登录用户
env.user = 'root'

env.roledefs = {
    'webservers':['10.6.65.209'],
    # 'dbservers':['192.168.56.13']
}

env.passwords = {
    'root@10.6.65.209:22':'xuchao971124',
    # 'root@192.168.56.12:22':'1234567',
    # 'root@192.168.56.13:22':'1234567',
}

@roles('webservers')
def remote_task():
    # with cd('/data/logs'):     # with 的左右是让后面的表达式，继承前面的状态
    #     run('ls -l')           # 实现 'cd /data/logs/ && ls -l' 的效果
    run("echo 'this is web1'")


@roles('webservers')
def web_task():
    run("echo 'this is web2'")


@roles('dbservers')
def remote_build():
    with cd('/tmp/citizen_wang'):
        run('git pull')

def remote_deploy():
    run('tar zxvf /tmp/fabric.tar.gz')
    run('mv /tmp/fabric/setup.py /home/www/')

# def task():
#     execute(remote_build)
#     execute(remote_deploy)
