import os
import argparse
import cv2
import time
import re

parser = argparse.ArgumentParser()
parser.add_argument("image_location", help="max z height for outputting data", type=str)
parser.add_argument("--thumbnail_file", "-n", help="filename for writing thumbnail", type=str, default=None)
parser.add_argument("--width", "-x", help="width of main images (px)", type=int, default=640)
parser.add_argument("--height", "-y", help="height of main images (px)", type=int, default=480)
parser.add_argument("--thumb_width", help="width of thumbnail (px)", type=int, default=320)
parser.add_argument("--thumb_height", help="height of thumbnail (px)", type=int, default=240)
parser.add_argument("-timestep", "-t", help="time between images (s)", type=float, default=10.0)
parser.add_argument("--view_image", "-v", help="display window showing image locally", action="store_true")
parser.add_argument("--enable_file", "-e", help="location of a file containing 1 or 0 to enable/disable", action="store_true")
parser.add_argument("--disable_write", help="disable writing of timelapse data", action="store_true")
parser.add_argument("--camera_index", "-c", help="index of camera device", type=int, default=0)
args = parser.parse_args()

# Filename checking stuff
if not os.path.exists(args.image_location):
    os.mkdir(args.image_location)

if not os.path.isdir(args.image_location):
    raise FileExistsError(f"{args.image_location} exists, but is not a directory.")


# Camera setup
cap = cv2.VideoCapture(0)

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

time_gap = args.timestep
time_zero = time.time()
target_time = time_zero
last_pre_time = 0.0

with open(os.path.join(args.image_location, metadata_filename), 'w') as fid:
    while True:

        # If no environment variable is set, run
        run_env = True
        if not args.disable_env:
            if "DO_TIMELAPSE" in os.environ:
                if os.environ["DO_TIMELAPSE"] != "1":
                    run_env = False

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
            if args.thumbnail_file is not None or args.view_image:
                small = cv2.resize(frame, (args.thumb_width, args.thumb_height))

                if args.thumbnail_file is not None:
                    cv2.imwrite(args.thumbnail_file, small)

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
