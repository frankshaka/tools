#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import os.path
import re
import subprocess

cwd = os.getcwd()
dir_list = []
options = {}

def jar(dir_path):
	if options.get("veryverbose"):
		print ""
	(parent, dir_name) = os.path.split(dir_path)
	jar_path = os.path.join(parent, dir_name + ".jar")
	if options.get("veryverbose"):
		print "Jaring: %s" % jar_path
		print "  from: %s" % dir_path
	if os.path.lexists(jar_path):
		if options.get("force"):
			print "Removing existing JAR file: " + jar_path
			os.remove(jar_path)
		else:
			print "Skipping existing JAR file: " + jar_path
			print "    (Use -f or --force option to remove existing JAR files.)"
	os.chdir(dir_path)
	subprocess.call([
		"jar",
		"-cfM" if not options.get("veryverbose") else "-cvfM",
		jar_path
	] + os.listdir(dir_path), cwd=dir_path)
	if options.get("verbose"):
		print jar_path

def add_dir(dir_name):
	path = os.path.join(cwd, dir_name)
	if os.path.isdir(path):
		dir_list.append(path)
	else:
		(parent, pattern) = os.path.split(path)
		if "*" in pattern:
			pattern = re.compile("^" + pattern.replace("*", ".*") + "$")
			for name in os.listdir(parent):
				path = os.path.join(parent, name)
				if os.path.isdir(path):
					dir_list.append(path)

for arg in sys.argv[1:]:
	if arg == "-f" or arg == "--force":
		options["force"] = True
	elif arg == "-v" or arg == "--verbose":
		options["verbose"] = True
	elif arg == "-vv" or arg == "--veryverbose":
		options["veryverbose"] = True
	elif arg == "-h" or arg == "-?" or arg == "--help":
		options["help"] = True
	elif not arg.startswith("-"):
		add_dir(arg)

if options.get("help") or not dir_list:
	print "A simple tool to jar up files under directories into JAR files with directory names."
	print ""
	print "Usage: jars [OPTIONS] DIR1 [DIR2] ..."
	print ""
	print "Available options:"
	print "    -f  --force        Remove existing JAR files before generating new one"
	print "    -v  --verbose      Print generated JAR file paths"
	print "    -vv --veryverbose  Print even more information"
	print "    -h  --help         Print this help and exit"
	print ""
	print "Sample:"
	print ""
	print "    $ ls"
	print "    test"
	print "    $ ls /usr/local/lib"
	print "    common"
	print "    $ jars test /usr/local/lib/common"
	print "    /Users/USERNAME/Documents/test.jar"
	print "    /usr/local/lib/common.jar"
	print "    $ ls"
	print "    test test.jar"
	print "    $ ls /usr/local/lib"
	print "    common common.jar"
	print ""
else:
	for dir_path in dir_list:
		jar(dir_path)
