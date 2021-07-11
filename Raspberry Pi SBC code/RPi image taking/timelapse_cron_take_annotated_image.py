#!/usr/bin/python
# timelapse_cron_take_annotated_image.py - simple annotated image taking routine to be run as a cron job for time lapse image capture
#
# command: python3 /home/pi/starter_maker_kit1/RPi_code/image_taking/timelapse_cron_take_annotated_image.py
#

import time                # this imports the module to allow various simple time functions to be used
import RPi.GPIO as GPIO    # this imports the module to allow the GPIO pins to be easily utilised
import os                  # this imports the module to allow direct CLI commands to be run
from builtins import input # allows compatibility for input between Python 2 & 3

# This basic routine does not use any GPIO functions - it just needs the USB camera connected to the Pi
# it should be run with a cron job e.g. as root under the sudo crontab ie create the following entry using "sudo crontab -e"
# script to run every 5 minutes to take an image with the Image Taking Kit's USB camera (adjust time as necessary)
#*/5 * * * * python3 /home/pi/RPi_maker_kit5/image_taking/timelapse_cron_take_annotated_image.py >> /dev/null 2>> /dev/null
# or
# script to run every 5 minutes from 6am through to 9:55pm (adjust time as necessary)
#*/5 6-21 * * * python3 /home/pi/RPi_maker_kit5/image_taking/timelapse_cron_take_annotated_image.py >> /dev/null 2>> /dev/null

# define the text part of what is added to each captured image: the default is "Time-lapse image" but
# you can change this to whatever you like and it appears before the timestamp info that is also added
# to the image - you should however limit the text to about 15 characters so that it will fit OK
annotation_text = "Time-lapse image"

# define the folder where images will be stored
imagefolder = "/home/pi/RPi_maker_kit5/image_taking/timelapse_image_folder/"   # this is hard coded but can be changed to anything

# get the current date and time in a specified format
# as this string will be used in the stored image file name
# only use characters that are allowed in Windows files or 
# the file will not download from the Pi to a Windows machine
now = time.strftime("%Y-%m-%d_%H.%M.%S")   # this creates a string  for use in the file name in this forma: YYYY-mm-dd_HH.MM.SS
datetimenowprint = time.strftime("%H:%M  %d %b %Y")  # and this creates a printable format for annotating the image

print (now + " - program running: normally run as a cron job")  # this screen display is left in so it is visible when running the program as a test

image_name = imagefolder + "single_image_" + now + ".jpg"    # create the full file name including the path
print (now + " - single image being taken")      # this screen display is left in so it is visible when running the program as a test

# create the full fswebcam command string: skip first 5 frames, 640x480 resolution, no messages, no banner, 80% compression, stored file name
# the example below does not have any flip or rotate options which may be needed
# add --rotate <angle> where <angle> can be 90, 180 or 270 if rotation needed
# add --flip <direction> where <direction> can be h or v if you do want to flip the image for some reason
os_image_command = "fswebcam -S 5 -r 640x480 -q --no-banner --jpeg 80 " + image_name  
os.system(os_image_command)          # take the image using the fswebcam command string

# create the command string to make sure the new file is 'owned' by the pi user so that it is easier to manage
os_chown_command = "chown pi:pi " + image_name
os.system(os_chown_command)          # execute the file ownership change command

time.sleep(1)      # wait a short interval before cycling back to allow the image capture to complete

# now add the image annotation text using the convert utility that is part of imagemagick
text_command = "convert " + image_name + " -pointsize 18 -fill white -annotate +20+455 '" + annotation_text + " " + datetimenowprint + "' " + image_name
# the command above sets the text colour as 'white' but you might want to change this to 'black' depending upon the image background
# other choices that might work are 'blue', 'green', red, etc
#print ("text command is: " + text_command)  # this output is usually commented out
os.system(text_command) 
print ("image annotated and resaved with the same name")

# these screen displays are left in so they are visible when running the program as a test
print (" image taken and stored as: " + image_name)
print (" ")

print (" program finished")

