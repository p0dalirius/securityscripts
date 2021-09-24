#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : hashes.py
# Author             : Podalirius (@podalirius_)
# Date created       : 24 Sep 2021

import hashlib
import argparse


def parseArgs():
    parser = argparse.ArgumentParser(description="Description message")
    group_ex = parser.add_mutually_exclusive_group(required=True)
    group_ex.add_argument("-m", "--message", default=None, type=str, help='Input message')
    group_ex.add_argument("-f", "--file", default=None, type=str, help='Input file')
    return parser.parse_args()


if __name__ == '__main__':
    options = parseArgs()
    #
    if options.message is not None:
        message = bytes(options.message, "UTF-8")
    elif options.file is not None:
        f = open(options.file, 'rb')
        message = f.read()
        f.close()
    #
    print("[+] %d bits" % (32*4))
    print("  | \x1b[93mmd5\x1b[0m       : %s" % hashlib.md5(message).hexdigest())
    #
    print("[+] %d bits" % (40*4))
    print("  | \x1b[93msha1\x1b[0m      : %s" % hashlib.sha1(message).hexdigest())
    #
    print("[+] %d bits" % (56*4))
    print("  | \x1b[93msha3_224\x1b[0m  : %s" % hashlib.sha3_224(message).hexdigest())
    #
    print("[+] %d bits" % (64*4))
    print("  | \x1b[93mblake2s\x1b[0m   : %s" % hashlib.blake2s(message).hexdigest())
    print("  | \x1b[93msha256\x1b[0m    : %s" % hashlib.sha256(message).hexdigest())
    print("  | \x1b[93msha3_256\x1b[0m  : %s" % hashlib.sha3_256(message).hexdigest())
    #
    print("[+] %d bits" % (96*4))
    print("  | \x1b[93msha3_384\x1b[0m  : %s" % hashlib.sha3_384(message).hexdigest())
    print("  | \x1b[93msha384\x1b[0m    : %s" % hashlib.sha384(message).hexdigest())
    #
    print("[+] %d bits" % (128*4))
    print("  | \x1b[93mblake2b\x1b[0m   : %s" % hashlib.blake2b(message).hexdigest())
    print("  | \x1b[93msha3_512\x1b[0m  : %s" % hashlib.sha3_512(message).hexdigest())
    print("  | \x1b[93msha512\x1b[0m    : %s" % hashlib.sha512(message).hexdigest())
