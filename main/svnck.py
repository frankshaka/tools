#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import os.path
import time
import subprocess
import re

range_pattern = re.compile(r"^(\d+)-(\d+)$")

class ExecutionResult(object):
	def __init__(self, cmdargs, cmdkwargs, output, error, exitcode, start_time, ellapse_time):
		self.cmdargs = cmdargs
		self.cmdkwargs = cmdkwargs
		self.output = output
		self.error = error
		self.exitcode = exitcode
		self.start_time = start_time
		self.ellapse_time = ellapse_time

	def __str__(self):
		return repr(self.error)

class ExecutionException(Exception):
	def __init__(self, result):
		Exception.__init__(self, result)
		self.result = result


def run(*args, **kwargs):
	p = subprocess.Popen(args,
		stdin=subprocess.PIPE if "input" in kwargs else None,
		stdout=subprocess.PIPE if "output" in kwargs else None,
		stderr=subprocess.STDOUT if "output" in kwargs else None,
		cwd=kwargs.get("cwd"))
	start_time = time.time()
	(out, err) = p.communicate(kwargs.get("input"))
	ellapse_time = time.time() - start_time
	result = ExecutionResult(args, kwargs, out, err, p.poll(), start_time, ellapse_time)
	if result.exitcode and "noraise" not in kwargs:
		raise ExecutionException(result)
	return result


def parse_status_text(text):
	lines = text.split("\n")
	files = []
	for line in lines:
		if line:
			files.append({
				"index": str(len(files) + 1),
				"path": line[8:],
				"status": line[:7]
				})
	return files


def expand_indexes(indexes):
	expanded = []
	for index in indexes:
		range_match = range_pattern.match(index)
		if range_match:
			for i in xrange(int(range_match.group(1)), int(range_match.group(2)) + 1):
				expanded.append(str(i))
		else:
			expanded.append(index)
	return expanded


class Stage(object):
	def __init__(self, cwd):
		self.cwd = cwd
		self.files = {}
		self.staged = []
		self.unstaged = []

	def print_content(self):
		sys.stdout.write("+------------------------+\n")
		sys.stdout.write("| Unstaged Modifications |\n")
		sys.stdout.write("+------------------------+----------------------------------\n")
		if not self.unstaged:
			sys.stdout.write("| (None)\n")
		else:
			for index in self.unstaged:
				sys.stdout.write("| %(status)s %(path)s [%(index)s]\n" % self.files[index])
		sys.stdout.write("+-----------------------------------------------------------\n")
		sys.stdout.write("\n")

		sys.stdout.write("+----------------------+\n")
		sys.stdout.write("| Staged Modifications |\n")
		sys.stdout.write("+----------------------+------------------------------------\n")
		if not self.staged:
			sys.stdout.write("| (None)\n")
		else:
			for index in self.staged:
				sys.stdout.write("| %(status)s %(path)s [%(index)s]\n" % self.files[index])
		sys.stdout.write("+-----------------------------------------------------------\n")
		sys.stdout.write("\n")

	def refresh(self):
		sys.stdout.write("Current Working Copy: %s\n" % self.cwd)
		sys.stdout.write("Checking for modifications... (Ctrl+C to break)\n")
		status_text = run("svn", "status", cwd=self.cwd, output=True).output
		lines = status_text.split("\n")
		old_staged_paths = [self.files[i]["path"] for i in self.staged]
		self.files = {}
		self.unstaged = []
		self.staged = []
		nonindexed_files = []
		for line in lines:
			if line:
				nonindexed_files.append({
					"index": 0,
					"path": line[8:],
					"status": line[:7]
				})
		nonindexed_files.sort(lambda f1, f2: cmp(f1["path"], f2["path"]))
		for i in xrange(len(nonindexed_files)):
			f = nonindexed_files[i]
			f["index"] = str(i + 1)
			self.files[f["index"]] = f
			if f["path"] in old_staged_paths:
				self.staged.append(f["index"])
			else:
				self.unstaged.append(f["index"])

	def _move_elements(self, these, from_list, to_list, on_move=None):
		i = 0
		while i < len(from_list):
			x = from_list[i]
			if x in these:
				from_list.pop(i)
				to_list.append(x)
				if on_move is not None:
					on_move(x)
			else:
				i += 1

	def stage(self, indexes):
		if "all" in indexes:
			to_stage = self.unstaged
		else:
			to_stage = indexes
		self._move_elements(to_stage, self.unstaged, self.staged, on_move=self._on_stage)
		self.staged.sort()

	def _on_stage(self, index):
		sys.stdout.write("Staged: %s\n" % self.files[index]["path"])

	def unstage(self, indexes):
		if "all" in indexes:
			to_unstage = self.staged
		else:
			to_unstage = indexes
		self._move_elements(to_unstage, self.staged, self.unstaged, on_move=self._on_unstage)
		self.unstaged.sort()

	def _on_unstage(self, index):
		sys.stdout.write("Unstaged: %s\n" % self.files[index]["path"])

	def commit(self, all=False):
		if all:
			self.staged = self.staged + self.unstaged
			self.unstaged = []
			self.staged.sort()
			to_add = [self.files[index]["path"] for index in self.staged if self.files[index]["status"].startswith("?")]
			if to_add:
				sys.stdout.write("Adding files to version control....\n")
				added = run("svn", "add", *to_add, noraise=True)
				if added.exitcode != 0:
					return False
				self.refresh()
			self.print_content()
			sys.stdout.write("\n")

		sys.stdout.write("Write one line of commit message here, or enter a blank line to use default editor:\n")
		message = sys.stdin.readline()[:-1]
		to_commit = [self.files[index]["path"] for index in self.staged]
		if message:
			sys.stdout.write("Commit Message: %s\n" % message)
			sys.stdout.flush()
			run("svn", "commit", "-m", message, *to_commit, noraise=True)
		else:
			sys.stdout.write("Will try running 'svn commit' without commit message....\n")
			sys.stdout.flush()
			run("svn", "commit", *to_commit, noraise=True)
		self.refresh()

	def add(self, indexes):
		if "all" in indexes:
			to_add = [self.files[index]["path"] for index in self.files if self.files[index]["status"].startswith("?")]
		else:
			to_add = [self.files[index]["path"] for index in indexes if index in self.files and self.files[index]["status"].startswith("?")]
		if not to_add:
			sys.stdout.write("No files needed to add to version control.\n")
			return False
		sys.stdout.write("Adding files to version control....\n")
		run("svn", "add", *to_add, noraise=True)
		self.refresh()

	def revert(self, indexes):
		if "all" in indexes:
			to_revert = [self.files[index]["path"] for index in self.files]
		else:
			to_revert = [self.files[index]["path"] for index in indexes if index in self.files]
		if not to_revert:
			sys.stdout.write("No files to be reverted.\n")
			return False
		sys.stdout.write("Reverting files....\n")
		run("svn", "revert", *to_revert, noraise=True)
		self.refresh()

	def delete(self, indexes):
		if "all" in indexes:
			to_delete = [self.files[index]["path"] for index in self.files if self.files[index]["status"].startswith("?")]
		else:
			to_delete = [self.files[index]["path"] for index in indexes if index in self.files and self.files[index]["status"].startswith("?")]
		if not to_delete:
			sys.stdout.write("Only files NOT under version control could be deleted here.\n")
			sys.stdout.write("Quit and use 'svn delete --force' to delete those under version control.\n")
			return False
		sys.stdout.write("\nDelete the following files?\n")
		for path in to_delete:
			sys.stdout.write("    %s\n" % path)
		sys.stdout.write("\n")
		sys.stdout.write("==== WARNING 1: This operation cannot be undone! ====\n")
		sys.stdout.write("==== WARNING 2: This operation cannot be undone! ====\n")
		sys.stdout.write("==== WARNING 3: This operation cannot be undone! ====\n")
		sys.stdout.write("Type 'yes' to confirm, or any other to abort > ")
		ans = sys.stdin.readline()[:-1].lower()
		if ans != "yes":
			sys.stdout.write("Aborted.\n")
			return False
		run("rm", *to_delete, noraise=True)
		self.refresh()


def main():
	try:
		cwd = os.getcwd()

		stage = Stage(cwd)
		stage.refresh()
		if not stage.unstaged:
			sys.stdout.write("No modifications yet.\n")
			return

		while 1:
			stage.print_content()
			sys.stdout.write("Command: q=quit, s=stage, u=unstage, c=commit, a=add, r=revert, d=delete, f=refresh\n")
			command_handled = False
			while not command_handled:
				sys.stdout.write("> ")
				args = sys.stdin.readline()[:-1].split(" ")
				command = args[0].lower()
				args = args[1:]

				if command == "q":
					# Quit program:
					sys.stdout.write("Quit.\n")
					return
				elif command == "s":
					# Stage files:
					if not args:
						sys.stdout.write("Usage: s [all] [INDEX1] [INDEX2-INDEX3]...\n")
					else:
						command_handled = stage.stage(expand_indexes(args)) is not False
				elif command == "u":
					# Unstage files:
					if not args:
						sys.stdout.write("Usage: u [all] [INDEX1] [INDEX2-INDEX3]...\n")
					else:
						command_handled = stage.unstage(expand_indexes(args)) is not False
				elif command == "c":
					# Commit changes:
					if not stage.staged and "all" not in args:
						sys.stdout.write("No files staged. Use 's' command to mark files to be commited with.\n")
					else:
						command_handled = stage.commit(all="all" in args) is not False
						if not stage.unstaged and not stage.staged:
							sys.stdout.write("All modifications have been commited.\n")
							return
				elif command == "a":
					# Add files to version control:
					if not args:
						sys.stdout.write("Usage: a [all] [INDEX1] [INDEX2-INDEX3]...\n")
					else:
						command_handled = stage.add(expand_indexes(args)) is not False
				elif command == "r":
					# Revert files to last update:
					if not args:
						sys.stdout.write("Usage: r [all] [INDEX1] [INDEX2-INDEX3]...\n")
					else:
						command_handled = stage.revert(expand_indexes(args)) is not False
				elif command == "d":
					# Delete files:
					if not args:
						sys.stdout.write("Usage: d [all] [INDEX1] [INDEX2-INDEX3]...\n")
					else:
						command_handled = stage.delete(expand_indexes(args)) is not False
						if not stage.unstaged and not stage.staged:
							sys.stdout.write("All modifications have been deleted.\n")
							return
				elif command == "f":
					# Refresh staging status:
					stage.refresh()
					command_handled = True
	except ExecutionException, e:
		sys.stderr.write(e.result.output)
	except KeyboardInterrupt:
		sys.stderr.write("\n")


if __name__ == "__main__":
	main()
