#!/usr/bin/env bash

#
# The server files will be installed on the ramdisk, as the files involved are re-written very frequently, see README.md
#

RAMDISK="/tmp/ramdisk"

# Copy files over

if [ -d "$RAMDISK" ]; then
  echo "Copying files to ${RAMDISK}..."
else
  echo "Error: ${RAMDISK} not found, this should be set up to be a ram disk. See README.md"
  exit 1
fi

cp -r web $RAMDISK
chmod 777 $RAMDISK/web

# Start timelapse system

python3 timelapse.py -s"/tmp/ramdisk/web" -t${2:-10} $1 &

echo "Timelapse PID $!"

location=$(pwd)
cd /tmp/ramdisk || exit
python3 $location/webserver.py &

cd $location || exit

echo "Server PID $!"

