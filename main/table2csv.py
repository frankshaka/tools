#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import os.path
from xml.dom.minidom import parse
import xml.parsers.expat
import traceback

arglen = len(sys.argv)
if arglen < 2:
    input = sys.stdin
else:
    input_path = sys.argv[1]
    if not os.path.isabs(input_path):
        input_path = os.path.join(os.getcwd(), input_path)
    input = open(input_path, "r")

try:
    dom = parse(input)
except xml.parsers.expat.ExpatError:
    traceback.print_exc()
    print >> sys.stderr, "Try converting invalid characters by using 'iconv -f \"gbk\" -t \"utf-8\" < INPUT_FILE > OUTPUT_FILE'."
    sys.exit(2)

tables = dom.getElementsByTagName("table")
if not tables:
    sys.stderr.write("No table element found!")
    sys.exit(3)

rows = tables[0].getElementsByTagName("tr")

def getTextContent(ele):
    buf = []
    child = ele.firstChild
    while child is not None:
        if child.nodeType == child.TEXT_NODE:
            buf.append(child.nodeValue)
        else:
            buf.append(getTextContent(child))
        child = child.nextSibling
    return "".join(buf)

if arglen < 3:
    output = sys.stdout
else:
    output_path = sys.argv[2]
    if not os.path.isabs(output_path):
        output_path = os.path.join(os.getcwd(), output_path)
    output = open(output_path, "w")

try:
    for row in rows:
        row_buf = [getTextContent(cell) for cell in row.getElementsByTagName("td")]
        row_content = ",".join(row_buf)
        output.write(row_content.encode("utf-8"))
        output.write("\r\n")
finally:
    if output != sys.stdout:
        output.close()

