import os
import sys
import cgi

form = cgi.FieldStorage()

# If there are args provided, set the value
if "state" in form:
    target = form["state"]

    if target == "1":
        os.environ["DO_TIMELAPSE"] = "1"

    elif target == "0":
        os.environ["DO_TIMELAPSE"] = "0"

# Check process with specified ID somehow


# Check the environment variable
status = "active"
if "DO_TIMELAPSE" in os.environ:
    if os.environ["DO_TIMELAPSE"] == "0":
        print("paused")

print("Content-type:text/plain\r\n\r\n")
print(status)