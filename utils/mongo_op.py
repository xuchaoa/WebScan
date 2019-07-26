#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/24/19 4:09 PM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : mongo_op.py


from pymongo import MongoClient
import json
from bson.objectid import ObjectId


class MongoDB(object):

    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 27017
        self.database = 'scanner'
        self.conn = MongoClient(self.host, self.port)
        self.db = self.conn.scaner
        # self.db.authenticate('','')

    def add_vuln_info(self,taskID,name,info,notice,payload):

        temp_dic = {
            'info':info,
            'notice':notice,
            'payload':payload
        }
        coll = self.db.scanresult
        try:
            coll.update({'task_id':taskID},{'$set':{"vulnerable_attack."+name: temp_dic}})
            return True
        except:
            return False

    def add_child_tasks(self,parentID,SubDomainResult):
        """
        :param parentID:
        :param SubDomainResult:
        :return:
        """
        if len(SubDomainResult) == 0:
            return None

        child_task_ids = []
        for _ in SubDomainResult.items():
            task_template = {
                "ip":_[0],
                "domain":_[1],
                "ports":"",
                "vulnerable_attack":{

                }
            }
            child_task_ids.append(str(self.db.result.insert(task_template)))

        self.db.task.update({"_id":ObjectId(parentID)},{'$push':{'ChildTaskID':{'$each':child_task_ids}}})


def main():
    x = MongoDB()
    new_posts = {
            "ip":"",
            "domain":"",
            "ports":"",
            "vulnerable_attack":{
                "ssh_burte":{
                    "info":"",
                    "notice":"",
                    "payload":""
                },
                "cve-2017-1221":{
                    "info":"add",
                    "notice":"add",
                    "payload":"add"
                }
            }
        }
    coll = x.db.scanresult
    aaa = coll.insert(new_posts)
    print(str(aaa))
    # coll.update({'task_id':'456'},new_posts,upsert=False)
    # print(coll.find({'task_id':'456'})[0])


if __name__ == '__main__':
    # main()

    # x = MongoDB()
    # x.add_vuln_info('456','cve-2017-11','info','notice','payload')

    x = MongoDB()
    test_data = {'123.207.155.221': ['blog.ixuchao.cn', 'love.ixuchao.cn'], '150.109.112.233': ['www.ixuchao.cn'], '106.12.150.166': ['blogs.ixuchao.cn', 'bb.ixuchao.cn']}
    id = '5d3ac1452083f76b467da2c7'
    x.add_child_tasks(id,{})

