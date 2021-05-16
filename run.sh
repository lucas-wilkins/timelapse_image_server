#!/usr/bin/env bash

#
# The server files will be installed on the ramdisk, as the files involved are re-written very frequently, see README.md
#

RAMDISK="/tmp/ramdisk"

if [ -d "$RAMDISK" ]; then
  echo "Copying files to ${RAMDISK}..."
else
  echo "Error: ${RAMDISK} not found, this should be set up to be a ram disk. See README.md"
  exit 1
fi

cp -r web $RAMDISK


# Start the timelapse system, and get its PID so that it can be tracked by the webserver
#TIMELAPSE_PROCESS=$(sh -c 'echo $$; exec python3 timelapse.py -n"thumb-nocache.png')

# Start the webserver
#cd webcontrol || exit
#python3 webserver.py "$TIMELAPSE_PROCESS"

