#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys

args = sys.argv[1:] or ['-']

def cate(fin):
    for line in fin.xreadlines():
        print repr(line)

for arg in args:
    if arg == '-':
        cate(sys.stdin)
    else:
        with open(arg, 'rb') as fin:
            cate(fin)
