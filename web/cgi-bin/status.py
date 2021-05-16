#!/bin/env python3

import os
import sys
import cgi

form = cgi.FieldStorage()

# If there are args provided, set the value
if "state" in form:
    target = form["state"].value


    with open("web/status.txt", 'w') as fid:

        if target == "1":
            fid.write("active")

        elif target == "0":
            fid.write("paused")

        else:
            pass
            #fid.write(str(form["state"]))

#print("Content-type:text/plain\r\n\r\n")
#print(status)