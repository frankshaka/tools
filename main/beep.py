#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import time

count = int(sys.argv[1], 10) if len(sys.argv) > 1 else 1

for x in xrange(count):
    sys.stderr.write("\a")
    time.sleep(0.1)

