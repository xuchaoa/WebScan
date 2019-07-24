#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/24/19 4:09 PM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : mongo_op.py


from pymongo import MongoClient


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

def main():
    x = MongoDB()
    new_posts = {
    "task_id":"456",
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
    coll.insert(new_posts)
    # coll.update({'task_id':'456'},new_posts,upsert=False)
    # print(coll.find({'task_id':'456'})[0])


if __name__ == '__main__':
    # main()
    x = MongoDB()
    x.add_vuln_info('456','cve-2017-11','info','notice','payload')

