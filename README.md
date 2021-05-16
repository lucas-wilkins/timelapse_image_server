Timelapse System
==================

A basic HTTP server controlable timelapse system for a Raspberry Pi.

This code provides a timelapse system that can either be run as a standalone 
program (timelapse.py) or integrated into a standalone system that can be 
started and stopped remotely via a web-app. For more critical applications,
it is advisable to run the server when the pi is started.

Some effort has been put into assuring accurate timings for the timelapse, 
and the system records the time at which a photo is taken along with when 
the capture ended and other timing information.

Dependencies
------------

* python3
* python3-opencv
* python3-psutil
* python3-numpy

General
=======

To record a timelapse without the webserver, all that is needed is timelapse.py.
There is a command line option (-v) that will show a preview window if an x-server is present.

Files are numerically identified, and added sequentially to a specified 
directory. There is a single  `.csv` file with timing data for each run.


Disable Wifi Sleeping
---------------------

The default settings on a raspberry pi is that the wifi card will go into 
low-power mode after a period of time, and thus turn off. This can be
a problem when using it for timelapses you wont be able to log in, or check
with the webserver. To disable this, do:

`sudo iw wlan0 set power_save off`

and it can be checked with

`iw wlan0 get power_save`


Getting Camera Resolutions
--------------------------

A script to list camera resolutions will be added soon.

GPU Memory and HQ Pi Camera
---------------------------

The highest resolutions of the new "high quality" raspberry pi camera require quite 
a substantial amount of graphics memory, at least 256GB, if not 512GB will need to 
be assigned to use them. This can be done via `raspi-config`.

Dedicated Pi Setup
==================

Security Note
-------------

This web server is **not intended to be web-facing**, so its security has not been checked. Furthermore, it uses python's
SimpleHTTPServer classes, which themselves come with a warning about their unchecked security.


Setting up a Ram Disk
---------------------

`run.sh` will copy the files, found in the `web` sub-directory or this repository,
into the ramdisk when it is run, and start the various processes. This is because of the repeated writing of a single file.

It's best to run the image server from a ramdisk, so save reading and writing to the SD card.
The ramdisk doesn't need to be that big (typical sizes have been 150kB).

We can make a ramdisk appear on boot by doing (This uses vim which will need installing, but other text editors work)

Create a location for it if it doesn't exist. The code here assumes that this location is `/tmp/ramdisk`,
a different location can be specified through `$RAMDISK` in `run.sh`.

``sudo mkdir /tmp/ramdisk``

make sure it has the right access setup

``sudo chmod 777 /tmp/ramdisk``

``sudo vim /etc/fstab``

and adding an entry like this, the ``5m`` refers to 5MB of RAM, which should be more than sufficient:

``ramdisk0  /tmp/ramdisk  tmpfs  defaults,size=5m,x-gvfs-show  0  0``

To mount it immediately without reboot:

``sudo mount -a``

Use ``mount`` to check.

Configuring a Timelapse
-----------------------




Starting Paused or Active
-------------------------

When controlled from the webserver `timelapse.py` looks at 
 `/tmp/ramdisk/web/status.txt` (by default). 
At start up will have been copied from the local copy in the 
local repository. To change the default state at startup, 
simply change the local `status.txt` contents to either 
`active` or `paused`.