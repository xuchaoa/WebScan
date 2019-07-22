#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/22/19 4:00 PM
# @Author  : Archerx
# @Blog    : https://blog.ixuchao.cn
# @File    : tasks.py

import sys
import json
import queue
import string
import asyncio
import argparse
import traceback
import tldextract

import dns.resolver
import concurrent.futures

from random import choice
from random import randint

import urllib3
from urllib3.exceptions import InsecureRequestWarning

from conf.global_config import FUZZDOMAIN_DIC_NORMAL, FUZZDOMAIN_DIC_SMALL
from celery_tasks.main import app

urllib3.disable_warnings(InsecureRequestWarning)

DEBUG = True


def _debug_(s):
    if DEBUG:
        sys.stderr.write('[DEBUG] {}\n'.format(s))
        sys.stderr.flush()


def fetch_fastest_nameserver():
    """ 获取当地环境速度最快的 DNS 服务器 """
    return '180.76.76.76'


class SubdomainBrute(object):

    def __init__(self, max_level=3, threads=25, nameservers=None):

        self.max_level = max_level

        self.threads = threads

        self.fuzz_queue = queue.Queue()

        self.subs = []
        self.nexts = []
        self.resolver = dns.resolver.Resolver()
        self.resolver.lifetime = 5
        self.resolver.timeout = 5

        if nameservers is None:
            nameservers = fetch_fastest_nameserver()
        else:
            nameservers = nameservers

        self.resolver.nameservers.insert(0, '8.8.8.8')

        temp_file = FUZZDOMAIN_DIC_NORMAL
        with open(temp_file) as fd:
            for line in fd:
                self.subs.append(line.strip())
        temp_file = FUZZDOMAIN_DIC_SMALL
        with open(temp_file) as fd:
            for line in fd:
                self.nexts.append(line.strip())

    def query_domain_arecord(self, domain):
        ips = []
        try:
            answers = self.resolver.query(domain)
            if answers:
                ips = [answer.address for answer in answers]
                if ips:
                    _debug_('fetch "{}" => {}'.format(domain, ips))
            return domain, ips
        except dns.resolver.NoNameservers:
            return domain, ips
        except Exception:
            return domain, ips

    def analysis_wirdcard_domain(self, domain):
        _debug_('checking "{}" is wirdcard domain or not'.format(domain))
        for _ in range(3):
            if self._is_wirdcard_domain(domain):
                _debug_('"{}" is wirdcard domain'.format(domain))
                return domain, True
        return domain, False

    def _is_wirdcard_domain(self, domain):
        def rstr():
            return ''.join(
                [choice(string.ascii_lowercase + string.digits)
                 for _ in range(randint(3, 6))])

        def build_random_sub(max_level=5):
            return '.'.join([rstr() for _ in range(2, max_level)])

        fuzz_domain1 = '.'.join([build_random_sub(), domain])
        fuzz_domain2 = '.'.join([build_random_sub(), domain])
        _, ips1 = self.query_domain_arecord(fuzz_domain1)
        _, ips2 = self.query_domain_arecord(fuzz_domain2)
        if ips1 and ips2 and (sorted(ips1) == sorted(ips2)):
            _debug_('fuzzing {} => {}, {} => {}, [ips1 == ips2]'
                    .format(fuzz_domain1, ips1, fuzz_domain2, ips2))
            return True
        elif ips1 or ips2:
            _debug_('fuzzing {} => {}, {} => {}, [ips1 or ips2]'
                    .format(fuzz_domain1, ips1, fuzz_domain2, ips2))
            return True
        else:
            return False

    async def fuzz_domain(self, domain):
        _debug_('fuzzing "{}" subdomains'.format(domain))

        ext = tldextract.extract(domain)
        if ext.subdomain:
            level = ext.subdomain.count('.') + 1
        else:
            level = 0
        if level > int(self.max_level):
            _debug_('{} level is more than max_level({})'
                    .format(domain, self.max_level))
            return dict(), dict()

        with concurrent.futures.ThreadPoolExecutor(
                max_workers=self.threads) as executor:
            _loop = asyncio.get_event_loop()

            if level == 0:
                futures = [
                    _loop.run_in_executor(
                        executor,
                        self.query_domain_arecord,
                        '.'.join([sub, domain]))
                    for sub in self.subs
                ]
            else:
                futures = [
                    _loop.run_in_executor(
                        executor,
                        self.query_domain_arecord,
                        '.'.join([nxt, domain]))
                    for nxt in self.nexts
                ]

            results = await asyncio.gather(*futures)
            results = list(filter(lambda _: len(_[1]) != 0, results))

            sub_domains = dict(results).keys()

            futures = [
                _loop.run_in_executor(
                    executor,
                    self.analysis_wirdcard_domain,
                    sub_domain)
                for sub_domain in sub_domains
            ]
            next_brute_results = await asyncio.gather(*futures)
            next_brute_results = list(filter(lambda _: not _[1],
                                             next_brute_results))

            return dict(results), dict(next_brute_results)

    async def fuzz_domains(self, domains):
        with concurrent.futures.ThreadPoolExecutor(
                max_workers=self.threads) as executor:
            _loop = asyncio.get_event_loop()

            futures = []
            for domain in domains:
                ext = tldextract.extract(domain)
                if ext.subdomain:
                    level = ext.subdomain.count('.') + 1
                else:
                    level = 0
                if level > int(self.max_level):
                    _debug_('{} level is more than max_level({})'
                            .format(domain, self.max_level))
                    continue

                if level == 0:
                    futures.extend([
                        _loop.run_in_executor(
                            executor,
                            self.query_domain_arecord,
                            '.'.join([sub, domain]))
                        for sub in self.subs
                    ])
                else:
                    futures.extend([
                        _loop.run_in_executor(
                            executor,
                            self.query_domain_arecord,
                            '.'.join([nxt, domain]))
                        for nxt in self.nexts
                    ])
            sub_results = await asyncio.gather(*futures)
            sub_results = list(filter(lambda _: len(_[1]) != 0, sub_results))

            sub_domains = dict(sub_results).keys()

            futures = [
                _loop.run_in_executor(
                    executor,
                    self.analysis_wirdcard_domain,
                    sub_domain)
                for sub_domain in sub_domains
            ]
            sub_wd_results = await asyncio.gather(*futures)
            sub_wd_results = list(filter(lambda _: not _[1], sub_wd_results))

            return dict(sub_results), dict(sub_wd_results)

    def fuzz(self, brute_domain):
        results = {}
        # 首先获取爆破域名的 A 记录，并判断该域名是否为泛解析域名
        _, brute_domain_ips = self.query_domain_arecord(brute_domain)
        if len(brute_domain_ips) > 0:
            results[brute_domain] = brute_domain_ips
        _, _is_wirdcard = self.analysis_wirdcard_domain(brute_domain)
        if _is_wirdcard:
            return results

        self.fuzz_queue.put(brute_domain)
        loop = asyncio.get_event_loop()
        while self.fuzz_queue.qsize() > 0:

            qsize = self.fuzz_queue.qsize()
            domains = [self.fuzz_queue.get() for _ in range(qsize)]
            task = loop.create_task(self.fuzz_domains(domains))
            loop.run_until_complete(task)

            _results, _next_brute_results = task.result()

            if _results is None:
                continue

            for _next_domain, _is_wirdcard in _next_brute_results.items():
                if not _is_wirdcard:
                    self.fuzz_queue.put(_next_domain)

            if _results:
                results.update(_results)

        return results


def fuzzdomain(domain, max_level=1, threads=100):
    result = {}
    others = []
    fuzz_engine = SubdomainBrute(max_level=max_level, threads=threads)
    try:
        result = fuzz_engine.fuzz(brute_domain=domain)
    except Exception as ex:
        print('failed to brute subdomain on "{}", {}'.format(domain, str(ex)))
        traceback.print_exc()
        return dict(domains=result, other_domains=others)
    return dict(domains=result, other_domains=others)


@app.task(bind=True,name='FuzzDomain')
def run(self,DOMAIN, MAX_LEVEL=3, THREADS=25):
    global DEBUG
    DEBUG = False

    max_level = MAX_LEVEL
    threads = THREADS

    domain = DOMAIN
    fuzz_engine = SubdomainBrute(max_level=max_level, threads=threads)
    try:
        result = fuzz_engine.fuzz(brute_domain=domain)
    except Exception as ex:
        print('failed to brute subdomain on "{}", {}'.format(domain, str(ex)))
        traceback.print_exc()
        return
    print(json.dumps(result))



if __name__ == '__main__':
    import time
    start = time.time()
    run('ixuchao.cn')
    end = time.time()
    print('cost: {:.4f}s'.format(end - start))



# TODO: make the runtime lower
