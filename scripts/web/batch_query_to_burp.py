#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : batch_query_to_burp.py
# Author             : Podalirius (@podalirius_)
# Date created       : 7 Jan 2022

import argparse
import os
import time
from concurrent.futures import ThreadPoolExecutor
from rich.progress import Progress
import requests

# Disable warings of insecure connection for invalid cerificates
requests.packages.urllib3.disable_warnings()
# Allow use of deprecated and weak cipher methods
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
except AttributeError:
    pass


def parseArgs():
    parser = argparse.ArgumentParser(description="Description message")
    parser.add_argument("-P", "--proxy-ip", default="127.0.0.1", type=str, help='Proxy IP (default: 127.0.0.1)')
    parser.add_argument("-p", "--proxy-port", default=8080, type=int, help='Proxy port (default: 8080)')
    parser.add_argument("-f", "--urlsfile", default=None, required=True, help='File containing a list of URLs to get.')
    parser.add_argument("-v", "--verbose", default=False, action="store_true", help='Verbose mode. (default: False)')
    parser.add_argument("-t", "--threads", default=15, type=int, help='Number of threads (default: 15)')
    return parser.parse_args()


def worker(url, proxyDict, completed):
    r = requests.get(url, proxies=proxyDict, verify=False)
    completed[url] = True


if __name__ == '__main__':
    options = parseArgs()

    proxyDict = {
        "http": "http://%s:%d" % (options.proxy_ip, options.proxy_port),
        "https": "http://%s:%d" % (options.proxy_ip, options.proxy_port),
        "ftp": "ftp://%s:%d" % (options.proxy_ip, options.proxy_port)
    }

    if options.urlsfile is not None:
        if os.path.exists(options.urlsfile):
            f = open(options.urlsfile, 'r')
            urls = [l.strip() for l in f.readlines()]
            f.close()
            urls = list(sorted(set(urls)))

            # Waits for all the threads to be completed
            completed = {}
            with ThreadPoolExecutor(max_workers=min(options.threads, len(urls))) as tp:
                for url in urls:
                    tp.submit(worker, url, proxyDict, completed)
                #
                with Progress() as progress:
                    newlen, oldlen, targetlen = 0, 0, len(urls)
                    pb = progress.add_task("[cyan]Requesting urls ...", total=len(urls))
                    while newlen < targetlen:
                        newlen = len(completed.keys())
                        # print("%d  =>  %d / %d" % (oldlen, newlen, targetlen))
                        progress.update(pb, advance=(newlen - oldlen))
                        oldlen = newlen
                        time.sleep(0.25)
