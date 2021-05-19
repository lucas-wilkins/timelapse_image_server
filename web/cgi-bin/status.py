#!/bin/env python3

import cgi
import psutil
import sys

# Check whether the timelapse script is running 

found = False
for proc in psutil.process_iter():
    if proc.name() == "python3":
        if proc.cmdline()[1].endswith("timelapse.py"):
            found = True

if not found:
    with open("web/status.txt", 'w') as fid:
        fid.write("crashed")


# Update the desired state for the timelapse script

form = cgi.FieldStorage()
if "state" in form:
    target = form["state"].value


    with open("web/desired-status.txt", 'w') as desired_fid:

    	with open("web/status.txt",'w') as actual_fid:
            if target == "1":
                desired_fid.write("active")
                actual_fid.write("starting")    

            elif target == "0":
                desired_fid.write("paused")
                actual_fid.write("pausing")




