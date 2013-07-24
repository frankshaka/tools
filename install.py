#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import os.path

def help(exit=1):
    print "Utility to install or uninstall package components."
    print ""
    print "Usage: sudo python %s COMMAND [COMPONENTS]" % sys.argv[0]
    print ""
    print "Available commands:"
    print "    i   install     Install components (`sudo` required)"
    print "    u   uninstall   Uninstall components (`sudo` required)"
    print "    l   list        List all available components"
    print "    h   help        Print this help and exit"
    print ""
    print "Available components:"
    print "Type `python install.py list` for a list of all available components."
    print ""
    sys.exit(exit)

def check_root():
    if os.getuid() != 0:
        print >> sys.stderr, "This command must be run as root!"
        print >> sys.stderr, "Type `python %s help` for more information." % sys.argv[0]
        sys.exit(2)

args = sys.argv[1:]
if not args:
    help()

command = args.pop(0)

root_dir = os.path.dirname(os.path.abspath(__file__))
main_dir = os.path.join(root_dir, "main")
install_dir = "/usr/local/bin"

def to_source_path(name, source_dir=main_dir):
    for suffix in [".py", ".sh"]:
        path = os.path.join(source_dir, name + suffix)
        if os.path.lexists(path):
            return path
    return None

def to_component_name(path):
    if path.endswith(".py") or path.endswith(".sh"):
        return path[:-3]
    return None

def iter_components():
    for name in os.listdir(main_dir):
        name = to_component_name(name)
        if name:
            yield name

def list_components():
    print "Component directory: %s" % main_dir
    print " %-12s%-15s" % ("Name", "Status")
    print "-" * 27
    for name in iter_components():
        installed = os.path.lexists(os.path.join(install_dir, name))
        print " %-12s%-15s" % (name, "installed" if installed else "not installed")

def _uninstall(name):
    source_path = to_source_path(name)
    if not source_path:
        print >> sys.stderr, "No component named '%s'." % (name, source_path)
        return
    install_path = os.path.join(install_dir, name)
    if os.path.lexists(install_path):
        os.remove(install_path)
        print "Component '%s' uninstalled." % name
    else:
        print "Component '%s' is not installed yet." % name

def _install(name):
    source_path = to_source_path(name)
    if not source_path:
        print >> sys.stderr, "No component named '%s'." % (name, source_path)
        return
    install_path = os.path.join(install_dir, name)
    if os.path.lexists(install_path):
        print >> sys.stderr, "Component '%s' failed to install: Command '%s' already exists." % (name, install_path)
        return
    if not os.path.exists(install_dir):
        os.makedirs(install_dir)
    os.symlink(source_path, install_path)
    print "Component '%s' installed." % name

def uninstall(names):
    check_root()
    if "all" in names:
        names = iter_components()
    for name in names:
        _uninstall(name)

def install(names):
    check_root()
    if "all" in names:
        names = iter_components()
    for name in names:
        _install(name)

if command == "h" or command == "help":
    help()
elif command == "l" or command == "list":
    list_components()
elif command == "u" or command == "uninstall":
    uninstall(args)
elif command == "i" or command == "install":
    install(args)
else:
    print >> sys.stderr, "No such command: " + command
    print >> sys.stderr, "Type `python %s help` for more information." % sys.argv[0]
    sys.exit(3)

