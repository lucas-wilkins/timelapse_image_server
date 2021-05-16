import os
import argparse
import cv2
import time
import re
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("image_location", help="max z height for outputting data", type=str)
parser.add_argument("--server_root", "-s", help="root of directory of web-server (probably /tmp/ramdisk/'web')", type=str, default=None)
parser.add_argument("--width", "-x", help="width of main images (px)", type=int, default=640)
parser.add_argument("--height", "-y", help="height of main images (px)", type=int, default=480)
parser.add_argument("--thumb_width", help="width of thumbnail (px)", type=int, default=320)
parser.add_argument("--thumb_height", help="height of thumbnail (px)", type=int, default=240)
parser.add_argument("-timestep", "-t", help="time between images (s)", type=float, default=10.0)
parser.add_argument("--view_image", "-v", help="display window showing image locally", action="store_true")
parser.add_argument("--enable_file", "-e", help="location of a file containing 1 or 0 to enable/disable", action="store_true")
parser.add_argument("--disable_write", help="disable writing of timelapse data", action="store_true")
parser.add_argument("--camera_index", "-c", help="index of camera device (-1 for fake)", type=int, default=0)
args = parser.parse_args()

# Filename checking stuff
if not os.path.exists(args.image_location):
    os.mkdir(args.image_location)

if not os.path.isdir(args.image_location):
    raise FileExistsError(f"{args.image_location} exists, but is not a directory.")

class FakeCap:
    def __init__(self):
        print("Creating fake camera")
        self.w = 640
        self.h = 480
        self.index = 0

    def set(self, key, value):
        if key == cv2.CAP_PROP_FRAME_WIDTH:
            self.w = value
        elif key == cv2.CAP_PROP_FRAME_HEIGHT:
            self.h = value

    def read(self):
        im = np.zeros((self.h, self.w, 3), dtype=np.uint8)

        # Using cv2.putText() method
        cv2.putText(im, 'Capture %i'%self.index, (50, self.h-50), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (255,255,255), 4, cv2.LINE_AA)

        self.index += 1
        return True, im

# Camera setup

cap = cv2.VideoCapture(args.camera_index) if args.camera_index >= 0 else FakeCap()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)

# File naming system
filename_pattern = re.compile("([0-9]*\.png)")

image_counter = 0
for filename in os.listdir(args.image_location):
    if filename_pattern.match(filename):
        this_index = int(filename[:-4])
        image_counter = max([image_counter, this_index])
image_counter += 1

metadata_filename = "meta_%s.csv"%(time.strftime("%Y-%m-%d_%H-%M-%S"))

# We show a first image before the timelapse begins,
#  because it seems that displaying the window
#  causes significant lag
if args.view_image:
    ret, frame = cap.read()
    small = cv2.resize(frame, (args.thumb_width, args.thumb_height))
    cv2.imshow("Timelapse", small)
    cv2.waitKey(1)

thumbnail_file = None if args.server_root is None else os.path.join(args.server_root, "thumb-nocache.png")
command_file = None if args.server_root is None else os.path.join(args.server_root, "status.txt")

def run_enabled():
    if command_file is None:
        return True
    else:
        try:
            with open(command_file, 'r') as fid:
                return fid.readline().strip() == "active"
        except Exception as e:
            #print("Read failed:", e.args)
            return True

time_gap = args.timestep
time_zero = time.time()
target_time = time_zero
last_pre_time = 0.0


with open(os.path.join(args.image_location, metadata_filename), 'w') as fid:
    while True:

        # If no environment variable is set, run
        run_env = run_enabled()
        # Timing system, as well as gathering stats for post-recording verification
        actual_time = time.time()
        target_time += time_gap

        time_delta = target_time - time.time() # This will track any severe lags

        # Wait until we hit the target time unless we're lagging
        time.sleep(max([time_delta, 0.0]))

        # Timed camera read (if statement in the way)
        pre_time = time.time() - time_zero

        if run_env:
            ret, frame = cap.read()
            post_time = time.time() - time_zero

            # Thumbnail stuff for monitoring
            if thumbnail_file is not None or args.view_image:
                small = cv2.resize(frame, (args.thumb_width, args.thumb_height))

                if thumbnail_file is not None:
                    cv2.imwrite(thumbnail_file, small)

                if args.view_image:
                    cv2.imshow("Timelapse", small)
                    cv2.waitKey(1)

            pre_time_delta = pre_time - last_pre_time

            if not args.disable_write:

                main_filename = "%06i.png"%(image_counter)
                cv2.imwrite(os.path.join(args.image_location, main_filename), frame)

                fid.write("%i, %s, %.6f, %.6f, %.6f, %.6f, %.6f, %.6f\n"%(
                    image_counter, main_filename,
                    target_time - time_zero, pre_time,
                    target_time, actual_time,
                    post_time, pre_time_delta))
                fid.flush()

        # Prepare for next loop
        last_pre_time = pre_time
        image_counter += 1
