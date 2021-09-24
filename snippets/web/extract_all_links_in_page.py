#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : extract_all_links_in_page.py
# Author             : Podalirius (@podalirius_)
# Date created       : 30 Jul 2021

import re
import requests
from bs4 import BeautifulSoup


def extract_all_links_in_page(data):
    """Documentation for extract_all_links_in_page"""
    links = []
    soup = BeautifulSoup(data, "lxml")
    tags = soup.findAll()
    for t in tags:
        if t.has_attr("href"):
            links.append(t["href"])
    if type(data) == bytes:
        _matched = re.findall(b"((http|https|ftp)://[a-zA-Z0-9]+\.[a-zA-Z0-9]+([:][0-9]+)?(/[a-zA-Z0-9_]+)+([/])?)", data)
        if _matched is not None:
            for l in _matched:
                links.append(l[0].decode("ISO-8859-1"))
    else:
        _matched = re.findall("((http|https|ftp)://[a-zA-Z0-9]+\.[a-zA-Z0-9]+([:][0-9]+)?(/[a-zA-Z0-9_]+)+([/])?)", data)
        if _matched is not None:
            for l in _matched:
                links.append(l[0])

    links = sorted(set(links))
    return links


if __name__ == '__main__':
    url = "https://podalirius.net/"
    r = requests.get(url)

    links = extract_all_links_in_page(r.content)

    print("[+] Found %d links :" % len(links))
    for link in links:
        print(link)
