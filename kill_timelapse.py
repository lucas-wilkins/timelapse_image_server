#!/bin/env python3

import psutil

""" Kill the timelapse script """

found = None
for proc in psutil.process_iter():
    if proc.name() == "python3":
        if proc.cmdline()[1].endswith("timelapse.py"):
            found = proc
            break
            

if found is None:
    print("Could not find timelapse process")
else:
    found.kill()

