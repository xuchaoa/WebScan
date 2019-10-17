import multiprocessing
import os
import time
import json

# a = {21: {'state': 'filtered', 'reason': 'no-response', 'name': 'ftp', 'product': '', 'version': '', 'extrainfo': '', 'conf': '3', 'cpe': ''}, 22: {'state': 'filtered', 'reason': 'no-response', 'name': 'ssh', 'product': '', 'version': '', 'extrainfo': '', 'conf': '3', 'cpe': ''}, 23: {'state': 'filtered', 'reason': 'no-response', 'name': 'telnet', 'product': '', 'version': '', 'extrainfo': '', 'conf': '3', 'cpe': ''}, 80: {'state': 'open', 'reason': 'syn-ack', 'name': 'http', 'product': 'nginx', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:igor_sysoev:nginx'}, 115: {'state': 'filtered', 'reason': 'no-response', 'name': 'sftp', 'product': '', 'version': '', 'extrainfo': '', 'conf': '3', 'cpe': ''}, 443: {'state': 'open', 'reason': 'syn-ack', 'name': 'http', 'product': 'nginx', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:igor_sysoev:nginx'}, 445: {'state': 'filtered', 'reason': 'no-response', 'name': 'microsoft-ds', 'product': '', 'version': '', 'extrainfo': '', 'conf': '3', 'cpe': ''}, 547: {'state': 'filtered', 'reason': 'no-response', 'name': 'dhcpv6-server', 'product': '', 'version': '', 'extrainfo': '', 'conf': '3', 'cpe': ''}, 1433: {'state': 'filtered', 'reason': 'no-response', 'name': 'ms-sql-s', 'product': '', 'version': '', 'extrainfo': '', 'conf': '3', 'cpe': ''}, 3306: {'state': 'filtered', 'reason': 'no-response', 'name': 'mysql', 'product': '', 'version': '', 'extrainfo': '', 'conf': '3', 'cpe': ''}, 3389: {'state': 'filtered', 'reason': 'no-response', 'name': 'ms-wbt-server', 'product': '', 'version': '', 'extrainfo': '', 'conf': '3', 'cpe': ''}, 8080: {'state': 'filtered', 'reason': 'no-response', 'name': 'http-proxy', 'product': '', 'version': '', 'extrainfo': '', 'conf': '3', 'cpe': ''}}
# a = {22: {'state': 'open', 'reason': 'syn-ack', 'name': 'ssh', 'product': 'OpenSSH', 'version': '7.2p2 Ubuntu 4ubuntu2.2', 'extrainfo': 'Ubuntu Linux; protocol 2.0', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 80: {'state': 'open', 'reason': 'syn-ack', 'name': 'http', 'product': 'nginx', 'version': '1.10.3', 'extrainfo': 'Ubuntu', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel', 'script': {'http-methods': '\n  Supported Methods: GET HEAD', 'http-server-header': 'nginx/1.10.3 (Ubuntu)', 'http-title': 'navigator\\xE5\\xB1\\x9E\\xE6\\x80\\xA7\\xE6\\x98\\xBE\\xE7\\xA4\\xBA'}}, 443: {'state': 'open', 'reason': 'syn-ack', 'name': 'http', 'product': 'nginx', 'version': '1.10.3', 'extrainfo': 'Ubuntu', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel', 'script': {'http-server-header': 'nginx/1.10.3 (Ubuntu)', 'http-title': 'navigator\\xE5\\xB1\\x9E\\xE6\\x80\\xA7\\xE6\\x98\\xBE\\xE7\\xA4\\xBA', 'ssl-cert': 'Subject: commonName=hjd86.cn\nSubject Alternative Name: DNS:hjd86.cn, DNS:www.hjd86.cn\nIssuer: commonName=TrustAsia TLS RSA CA/organizationName=TrustAsia Technologies, Inc./countryName=CN\nPublic Key type: rsa\nPublic Key bits: 2048\nSignature Algorithm: sha256WithRSAEncryption\nNot valid before: 2019-05-06T00:00:00\nNot valid after:  2020-05-05T12:00:00\nMD5:   4c0d 3493 6f85 03d5 6008 c57a 69e8 f0b3\nSHA-1: fd13 39f7 8abd b467 eb25 9537 05eb 7f2c 0ed9 5927', 'ssl-date': 'TLS randomness does not represent time', 'tls-nextprotoneg': '\n  http/1.1'}}}
a = {22: {'state': 'filtered', 'reason': 'no-response', 'name': 'ssh', 'product': '', 'version': '', 'extrainfo': '', 'conf': '3', 'cpe': ''}, 80: {'state': 'open', 'reason': 'syn-ack', 'name': 'http', 'product': 'nginx', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:igor_sysoev:nginx'}, 443: {'state': 'open', 'reason': 'syn-ack', 'name': 'http', 'product': 'nginx', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:igor_sysoev:nginx'}, 8080: {'state': 'filtered', 'reason': 'no-response', 'name': 'http-proxy', 'product': '', 'version': '', 'extrainfo': '', 'conf': '3', 'cpe': ''}, 9711: {'state': 'open', 'reason': 'syn-ack', 'name': 'ssh', 'product': 'OpenSSH', 'version': '7.4', 'extrainfo': 'protocol 2.0', 'conf': '10', 'cpe': 'cpe:/a:openbsd:openssh:7.4'}}


#
# b = json.dumps(a)
# print(type(b))
#
# c = json.loads(b)
# print(type(c))
#
# for a,b in c.items():
#      print(a,b)

# print(list(a.values()))
# print(a.values())
# for _ in a.keys():
#     print(a[_])

# result = {}
# for key,value in a.items():
#      if key == 80 and 'name' in value.keys() and 'http' in value['name']:
#           print(key)
#      if key == 443 and 'name' in value.keys() and 'http' in value['name']:
#           print(key)


# print(result)


# x = json.dumps(a, sort_keys=True, indent=4, separators=(',', ':'))
# with open('x.json','w') as f:
#     f.write(a)


# import re
# if re.search('vnc-\d{1}', 'ssvnc-1', re.I):
#      print(11)
#


x = []
x.append('ss')
x.append('qq')
print(x)

import requests

list = []
res = requests.get('https://blog.ixuchao.cn')
print(res.status_code)
print(type(res.url))
list.append(str(res.status_code))
list.append(str(res.headers['content-type']))
list.append(res.url)
print(list)