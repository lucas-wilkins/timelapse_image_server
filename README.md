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

Don't forget to update and upgrade everything (this will help many things, including keeping the pi cool if using a pi 4)

``
sudo apt update
sudo apt full-upgrade
``


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

We can then put an entry in fstab, it is good practice to make a backup of these files when editing them


``
sudo cp /etc/fstab /etc/fstab.backup
sudo vim /etc/fstab
``

and adding an entry like this, the ``5m`` refers to 5MB of RAM, which should be more than sufficient:

``ramdisk0  /tmp/ramdisk  tmpfs  defaults,size=5m,x-gvfs-show  0  0``

To mount it immediately without reboot:

``sudo mount -a``

Use ``mount`` to check.


Mounting a Hard Disk on Start Up
--------------------------------

It is likely that you'll be recording onto an external hard disk. In order to have the system start when the hard disk mounted, the appropriate entry will need to be put into fstab.

First of all you need a directory as a mount point, I have chosen  `/mnt/external_hdd` so

``
sudo mkdir /mnt/external_hdd
sudo chmod 777 /mnt/external_hdd
``

You also need to know what kind of file system it has, you can find this out `file`.
On my system the external disk is `/dev/sda` and the partition is `/dev/sda1`. 
So I type

``sudo file /dev/sda1``

Now to try and mount it. If it is already be mounted. Unmount it with

``sudo umount /dev/sda1``

Mounting will need a 

The user pi will have a UID and GID of 1000 by default on many Raspian editions.
To put an entry into ``fstab`` you will need to know the UUID for the partition you are mounting.

Get the UUID with 

``sudo blkid``

First try and mount it without putting anything in fstab

``sudo mount -t vfat -o nofail,uid=1000,gid=1000 /dev/sda1 /mnt/external_hdd/``

Assuming that this is successful add to fstab much like the ramdisk above, 
but this time we want a specific id, and we'll add some useful extra options.

* ``noatime`` and ``nodiratime`` - Don't record last access time (+speed)
* ``async`` - Reduces number of flushes (+speed, +disk lifetime)
* ``nofail`` - Pi will boot if drive isn't there (+usability)

```
UUID=[insert UUID here!] /mnt/external_hdd vfat async,noatime,nodiratime,nofail,uid=1000,gid=1000,umask=007 0 0
```

Configuring a Timelapse
-----------------------


Starting Paused or Active
+++++++++++++++++++++++++

When controlled from the webserver `timelapse.py` looks at 
 `/tmp/ramdisk/web/status.txt` (by default). 
At start up will have been copied from the local copy in the 
local repository. To change the default state at startup, 
simply change the local `status.txt` contents to either 
`active` or `paused`.
