#!/usr/bin/env python
# -*- coding:utf-8 -*-
########################################################
# This script generates MD5 and SHA1 digest for files.
########################################################

import sys
import glob
import subprocess
import re
import os.path


DIGEST_PREFIX_PATTERN = re.compile(r"^.* ")


def print_help():
    print "Usage: dgen [OPTIONS] FILE1 [FILE2]..."
    print "Options:"
    # print " -v --verbose   - Print more details"
    print "    --md5       - Generate/verify only MD5 digest files"
    print "    --sha1      - Generate/verify only SHA1 digest files"
    print "    --verify    - Verify each file against its digest file"
    print "    --help      - Print this help and exit"
    sys.exit(1)


def generate_digest(file_path, digest_type):
    (out, err) = subprocess.Popen(["openssl", digest_type, file_path],
        stdout=subprocess.PIPE).communicate()
    return DIGEST_PREFIX_PATTERN.sub("", out or "")[:-1]


def read_file(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r") as f:
        return f.read()


def generate_digest_file(file_path, digest_type, suffix):
    digest = generate_digest(file_path, digest_type)
    with open(file_path + suffix, "w") as f:
        f.write(digest)


def verify_digest_file(file_path, digest_type, suffix):
    digest = read_file(file_path + suffix)
    if digest:
        if digest == generate_digest(file_path, digest_type):
            print "%s: %s Valid" % (file_path, digest_type.upper())
        else:
            print "%s: %s Invalid" % (file_path, digest_type.upper())


def run(files, verbose=False, nosha1=False, nomd5=False, verify=False, **options):
    for file_path in files:
        if verify:
            if not nomd5:
                verify_digest_file(file_path, "md5", ".md5")
            if not nosha1:
                verify_digest_file(file_path, "sha1", ".sha1")
        else:
            if not nomd5:
                generate_digest_file(file_path, "md5", ".md5")
            if not nosha1:
                generate_digest_file(file_path, "sha1", ".sha1")
    return 0


def main():
    options = {}
    files = []
    for arg in sys.argv[1:]:
        if arg == "help" or arg == "--help":
            return print_help()
        elif arg == "-v" or arg == "--verbose":
            options["verbose"] = True
        elif arg == "--md5":
            if "nosha1" not in options:
                options["nosha1"] = True
            options["nomd5"] = False
        elif arg == "--sha1":
            if "nomd5" not in options:
                options["nomd5"] = True
            options["nosha1"] = False
        elif arg == "--verify":
            options["verify"] = True
        else:
            files = files + glob.glob(arg)
    if not files:
        return print_help()
    code = run(files, **options)
    sys.exit(code or 0)

if __name__ == "__main__":
    main()
