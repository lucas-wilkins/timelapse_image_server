#!/usr/bin/env bash

#
# The server files will be installed on the ramdisk, as the files involved are re-written very frequently, see README.md
#

RAMDISK="/tmp/ramdisk"
TIMELAPSEDIR="/mnt/external_hdd/timelapses"

# Copy files over

if [ -d "$RAMDISK" ]; then
  echo "Copying files to ${RAMDISK}..."
else
  echo "Error: ${RAMDISK} not found, this should be set up to be a ram disk. See README.md"
  exit 1
fi

cp -r web $RAMDISK
chmod 777 $RAMDISK/web
chmod 777 $RAMDISK/web/status.txt
chmod 777 $RAMDISK/web/desired-status.txt
chmod 777 $RAMDISK/web/cgi-bin/status.py

# Start timelapse system

# HQ cam max resolution 3840x2400, it seems to take about 1.5 seconds to read, process and store this, use max 5s.

# The webserver update looks for a python3 process with a first argument ending in timelapse, don't rename
python3 ./timelapse.py -x 3840 -y 2400 -s$RAMDISK/web -t5 $TIMELAPSEDIR &

location=$(pwd)
cd /tmp/ramdisk || exit
python3 $location/webserver.py &

cd $location || exit


