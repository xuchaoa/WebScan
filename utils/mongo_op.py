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
        self.database = 'xscan'
        self.conn = MongoClient(self.host, self.port)
        self.db = self.conn.xscan
        # self.db.authenticate('','')

    def add_vuln_info(self,taskID,name,info,notice,payload):

        temp_dic = {
            'info':info,
            'notice':notice,
            'payload':payload
        }
        coll = self.db.result
        try:
            coll.update({"_id":ObjectId(taskID)},{'$set':{"vulnerable_attack."+name: temp_dic}})
            return True
        except:
            return False

    def add_child_tasks(self,parentID,SubDomainResult):
        """
        :param parentID: str
        :param SubDomainResult: list
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
            child_task_ids.append(str(self.db.HostScan.insert(task_template)))

        self.db.task.update({"_id":ObjectId(parentID)},{'$push':{'ChildTaskID':{'$each':child_task_ids}}})
        return child_task_ids

    def add_child_tasks_normal(self, FtaskID, ChildTasks):
        self.db.task.update({"_id": ObjectId(FtaskID)}, {'$push': {'ChildTaskID': {'$each': ChildTasks}}})

    def add_open_ports(self, taskID, result):
        result = json.loads(result)
        if result:
            for key,value in result.items():
                del value['services']
                del value['endtime']
            coll = self.db.HostScan
            try:
                coll.update({"_id":ObjectId(taskID)}, {'$set': {"ports" : result}})
                return True
            except Exception as e:
                print(e)
                return False
        else:
            print("no")

    def add_port_serv(self,taskID,result):
        result = json.loads(result)
        for _ in result.keys():
            self.db.HostScan.update({"_id":ObjectId(taskID)},{'$set':{"ports."+_: result[_]}})

    def add_ip_location(self, taskID, result):
        result = json.loads(result)
        self.db.HostScan.update({"_id":ObjectId(taskID)},{'$set':{"location":result}})

    def add_alive_status_with_FtaskID(self, result, FtaskID):
        result = json.loads(result)
        task_id = {}
        child_id = []
        if FtaskID is not None:  #new insert data
            x = MongoDB()
            for ip,status in result.items():
                new_posts = {
                    "ip": ip,
                    "alive": status,
                    "domain": "",
                    "ports": "",
                    "location": "",
                    "vulnerable_attack": {}
                }
                coll = x.db.HostScan
                if status['state'] == 'up':
                    id = coll.insert(new_posts)
                    task_id[ip] = str(id)
                    child_id.append(str(id))
                else:
                    id = coll.insert(new_posts)
                    child_id.append(str(id))
            self.add_child_tasks_normal(FtaskID,child_id)  #子任务id添加到父任务中
        return task_id

    def add_alive_status(self, taskID, result):
        self.db.HostScan.update({"_id": ObjectId(taskID)}, {'$set': {"alive": result}})

    def add_port_sev_result(self, taskID, result):
        ports_result  = json.loads(result)
        coll = self.db.HostScan
        coll.update({"_id": ObjectId(taskID)}, {'$set': {"ports": ports_result}})

    def add_weak_pass_service(self, taskID, result):
        result = json.loads(result)
        for key,value in result.items():
            self.db.HostScan.update({"_id": ObjectId(taskID)}, {'$set': {"weakpass_service."+key : value}})

    def add_cms_finger(self, taskID, result):
        result = json.loads(result)
        # print('sss',type(result))
        for key,value in result.items():
            self.db.HostScan.update({"_id": ObjectId(taskID)}, {'$set': {"cms_finger."+key : value}})


    def add_Ftask(self):  # insert blank document to 'task' collection
        return self.db.task.insert({'ChildTaskID':[]})





def insert_test():
    x = MongoDB()
    new_posts = {
            "ip":"",
            "alive":"",
            "domain":"",
            "ports":"",
            "location":"",
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
    coll = x.db.HostScan
    aaa = coll.insert(new_posts)
    print(str(aaa))
    # coll.update({'task_id':'456'},new_posts,upsert=False)
    # print(coll.find({'task_id':'456'})[0])



def add_child_tasks_test():
    x = MongoDB()
    test_data = {'123.207.155.221': ['blog.ixuchao.cn', 'love.ixuchao.cn'], '150.109.112.233': ['www.ixuchao.cn'],
                 '106.12.150.166': ['blogs.ixuchao.cn', 'bb.ixuchao.cn']}
    id = '5d3ac1452083f76b467da2c7'
    x.add_child_tasks(id, {})


def add_vuln_info_test():
    x = MongoDB()
    x.add_vuln_info('456', 'cve-2017-11', 'info', 'notice', 'payload')

def add_open_ports_test():


    x = MongoDB()
    c = x.add_open_ports('5d3ac102dd76c2600d6fbc9c',json.dumps(a))
    print(c)

def test_ip_location():
    result = {'country_id': 'CN', 'country': 'China', 'region': 'Beijing'}
    taskID = '5d3edfd675f097ac6ee499c6'
    x = MongoDB()
    x.add_ip_location(taskID,json.dumps(result))



if __name__ == '__main__':
    # add_open_ports_test()
    # insert_test()
    test_ip_location()


