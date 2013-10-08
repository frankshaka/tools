#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys

def cat(filepath, trimmed):
    with open(filepath, "r") as source_file:
        for line in source_file:
            if trimmed:
                print repr(line)[1:-1]
            else:
                print repr(line)

def main():
    trimmed = False
    for filepath in sys.argv[1:]:
        if filepath == "-t":
            trimmed = True
        else:
            cat(filepath, trimmed)
            trimmed = False

if __name__ == "__main__":
    main()
