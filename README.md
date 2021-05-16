# timelapse_image_server
Basic HTTP server controlled timelapse system for a raspberry pi

Security
========

This web server is not intended to be web-facing, so its security has not been checked. Furthermore, it uses python's
SimpleHTTPServer classes, which themselves come with a warning about


Setting up a Ram Disk
=====================

It's best to run the image server from a ramdisk, so save reading and writing to the SD card.
The ramdisk doesn't need to be that big (typical sizes have been 150kB).

We can make a ramdisk appear on boot by doing (This uses vim which will need installing, but other text editors work)

Create a location for it if it doesn't exist
``sudo mkdir /tmp/ramdisk``
make sure it has the right access setup
``sudo chmod 777 /tmp/ramdisk``

``sudo vim /etc/fstab``

and adding an entry like this, the ``5m`` refers to 5MB of RAM, which should be more than sufficient:

``ramdisk0  /tmp/ramdisk  tmpfs  defaults,size=5m,x-gvfs-show  0  0``

To mount it immediately without reboot:

``sudo mount -a``

Use ``mount`` to check.
