#!/bin/env python3

import cgi
import psutil
import sys

form = cgi.FieldStorage()

# If there are args provided, set the value

with open("pid.txt") as fid:
    pid = int(fid.readline().strip())
    if not psutil.pid_exists(pid):
        with open("web/status.txt", 'w') as fid2:
            fid2.write("crashed")
        sys.exit()


if "state" in form:
    target = form["state"].value


    with open("web/status.txt", 'w') as fid:

        if target == "1":
            fid.write("active")

        elif target == "0":
            fid.write("paused")

