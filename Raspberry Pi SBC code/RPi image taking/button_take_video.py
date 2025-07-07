#!/usr/bin/python
# Starter PCB PCB button_take_video.py - simple video taking routine using a button
#
# command: python3 ./starter_maker_PCB1/RPi_code/image_taking/button_take_video.py
#

import time                # this imports the module to allow various simple time functions to be used
import RPi.GPIO as GPIO    # this imports the module to allow the GPIO pins to be easily utilised
import os                  # this imports the module to allow direct CLI commands to be run
from builtins import input # allows compatibility for input between Python 2 & 3
import pyautogui
import subprocess
import re

# get the current username for use in file storage paths
user_name = os.getlogin()

# This code sets the RPi to use the BCM (Broadcom) pin numbers which is usually the default but is positively set here
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)   # avoids various warning messages about GPIO pins being already in use

button_pin = 26  # this is the GPIO pin that one side of the tactile button is connected to

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
# this is a special setting that indicates when a pin changes from LOW to HIGH ie when the button is pressed

# this is a function to indicate when the button is pressed 
def btn_pressed():
    # if button is pressed GPIO.input will report FALSE
    if not GPIO.input(button_pin):
        return 1

# define the folder where videos will be stored
video_subfolder = " "
print (" ")
print (" ***************************************************************************")
print (" All button triggered videos will be stored under ")
print (" ./starter_maker_PCB1/RPi_code/image_taking/ ")
print ("   ..... but you must now enter a subfolder name for your VIDEOs")
print ("   ..... just hit RETURN for the default of 'button_video_folder'")
while len(video_subfolder) <= 5 or " " in video_subfolder :
    video_subfolder = input(" Enter sub-folder name - must be more than 5 characters and no spaces (CTRL C to stop? )") or "button_video_folder"
print (" ***************************************************************************")
print (" ")

videofolder = "/home/" + user_name + "/starter_maker_PCB1/RPi_code/image_taking/" + video_subfolder + "/"

# create the directory if it does not exist
if not os.path.exists(videofolder):
    os.makedirs(videofolder)      # execute the folder creation command

    # in some circumstances new file/directory ownership may become an issue
    # so the lines below create a command string to make sure the new directory and its files are 'owned' by 'user_name'
    os_chown_command = "chown -R " + user_name +":" + user_name + " " + videofolder
    os.system(os_chown_command)   # execute the file ownership change command

    print (videofolder + " folder created")
else:
    print (videofolder + " already exists, so no need to create it")
print (" ")

# get the current date and time in a specified format
# as this string will be used in the stored video file name
# only use characters that are allowed in Windows files or 
# the file will not download from the Pi to a Windows machine
now = time.strftime("%Y-%m-%d_%H.%M.%S")   # this creates a string in a designated format e.g. YYYY-mm-dd_HH.MM.SS

# check where the USB camera is connected
lsdevres = subprocess.getoutput('ls /dev/')
if len(re.findall("video0", lsdevres)) > 0 :
    print ("/dev/video0 is present")
    usb_device = "/dev/video0"
elif len(re.findall("video1", lsdevres)) > 0 :
    print ("/dev/video1 is present")
    usb_device = "/dev/video1"
elif len(re.findall("video2", lsdevres)) > 0 :
    print ("/dev/video1 is present")
    usb_device = "/dev/video2"
else:
    print ("no USB camera is present - exiting the program")
    usb_device = "exit"
    sys.exit()

print (now + " - program running: type CTRL-C to stop the program")
print (" ")

try:    # this loop is not strictly necessary but it does allow the script to be easily stopped with CTRL-C
    while True:  # this is the loop that checks if the button is pressed and takes a video if it is

        # input the video duration in seconds
        #  this example shows how to repeat the request if the input is not the required value
        clipduration = 0
        while clipduration <= 0 or clipduration > 59:
            clipduration = float(input("Enter video clip duration in seconds (1-59)? (CTRL C to stop)"))

        print ("press the button to take a short video clip or type CTRL-C to stop the program")
        print (" ")

        while not btn_pressed():
            pass           # if the button is not pressed just loop endlessly

        # button pressed so take the video clip.
        now = time.strftime("%Y-%m-%d_%H.%M.%S") # get the time and date the button was pressed to be used in the file name
        video_name = videofolder + "video_clip_" + now + ".avi"    # create the full file name including the path
        print (now + " - button pressed - video started")
        # create the full ffmpeg command string: 
        # create the relatively simple full ffmpeg command string: 
        # video4linux2 (v4l2) format, 640x480 size, input from camera, elapsed time in HH:MM:SS format, output video name
        # the example below does not have any rotate options which may be needed
        # add '-vf transpose=clock' for 90 degrees - use transpose=cclock for -90 or 270 degrees 
        #     and use transpose=clock,transpose=clock for 180 degrees ie do it twice
        # usb_device is determined earlier to set the -d parameter for where the USB camera is connected
        os_video_command = "ffmpeg -f video4linux2 -s 640x480 -i " + usb_device + " -t 00:00:" + str(int(clipduration)).zfill(2) + " " + video_name  
        print (os_video_command)
        os.system(os_video_command)          # start the video using the ffmpeg command string

        # in some circumstances new file/directory ownership may become an issue
        # so the lines below create a command string to make sure the new file is 'owned' by 'user_name'
        os_chown_command = "chown " + user_name +":" + user_name + " " + video_name
        os.system(os_chown_command)   # execute the file ownership change command

        time.sleep(1)      # wait a short interval before cycling back to allow the video capture to complete
        print (" ")
        print (" ***************************************************************")
        print (" video taken and stored as: " + video_name)
        print (" ***************************************************************")
        print (" ")
        print (" ")
        print (" ***************************************************************")
        print (" ")
        print (" starting another video capture cycle: ")
        print (" ")

finally:  # this code is run when the try is interrupted with a CTRL-C
    print(" ")
    print("Cleaning up the GPIO pins before stopping")
    print(" ")
    print(" ")
    print(" ")
    GPIO.cleanup()
    
# The cleanup command sets all the pins back to inputs which protects the
# Pi from accidental shorts-circuits if something metal touches the GPIO pins.

