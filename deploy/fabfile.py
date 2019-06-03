#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/31 下午9:33
# @Author  : Archerx
# @Site    : https://blog.ixuchao.cn
# @File    : fabfile.py.py
# @Software: PyCharm

from fabric.api import local, env, roles, cd , run
from fabric.api import *
from fabric.api import execute
import os, sys
current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_dir)
sys.path.append("..")
from fabric.contrib.files import append
from deploy import conf
from fabric.contrib.console import confirm
from fabric.contrib.project import rsync_project

def prepare_deploy():
    local('echo "hello"')


#必须先在这里指定登录用户
env.user = 'root'

env.roledefs = {
    'scannode':['10.6.65.209'],
    # 'testserver':['10.6.65.209']
    # 'dbservers':['192.168.56.13']
}

env.passwords = {
    'root@10.6.65.209:22':'xuchao971124',
    # 'root@192.168.56.12:22':'1234567',
    # 'root@192.168.56.13:22':'1234567',
}

@roles('scannode')
def remote_task():
    # with cd('/data/logs'):     # with 的左右是让后面的表达式，继承前面的状态
    #     run('ls -l')           # 实现 'cd /data/logs/ && ls -l' 的效果
    run("echo 'this is web1'")


@roles('scannode')
def web_task():
    run("echo 'this is web2'")


@roles('dbservers')
def remote_build():
    with cd('/tmp/citizen_wang'):
        run('git pull')

def remote_deploy():
    run('tar zxvf /tmp/fabric.tar.gz')
    run('mv /tmp/fabric/setup.py /home/www/')

@roles('scannode')
def UpdateRepo():
    '''
    centos7 更改清华源
    :return:
    '''
    run('mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.bak')
    append(filename='/etc/yum.repos.d/CentOS-Base.repo',text=conf.tsinghua)
    run('yum makecache')

def GetPython36():
    run('yum -y install python36')

@roles('scannode')
def PutMasscan():
    with cd("/home"):
        with settings(warn_only=True):  # put（上传）出现异常时继续执行，不终止
            result = put("./DeployFile/masscan", "/usr/bin")
        if result.failed and not confirm("put file failed, Continue[Y/N]?"):  # 出现异常时，确认用户是否继续，（Y继续）
            abort("Aborting file put task!")
@roles('scannode')
def RsyncCode():
    rsync_project(remote_dir="/home/xscan/", local_dir="/home/archerx/PycharmProjects/WebScan/")

def task():
    execute(remote_task)
    execute(web_task)
