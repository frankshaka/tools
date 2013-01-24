#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys

def cat(filepath):
	with open(filepath, "r") as source_file:
		for line in source_file:
			print repr(line)

def main():
	filepath = sys.argv[1]
	cat(filepath)

if __name__ == "__main__":
	main()
