#!/usr/bin/python

# file name: image_camera_usb_opencv_annotate.py
# USB camera openCV camera class: python code as part of a Flask based web server system
# version that uses a ram drive with set permissions etc so that any user can run the main app
# - this version uses imagemagick/convert to 'annotate' the streamed images
# - common version no matter whether the calling app is run as the user or as sudo
# - this 'new' version introduces a wider range of camera setting options 
#     i.e. bright, contrast, sat, hue, gain, exp, wbal, focus
# 
# This class is used to create an instance of a USB camera managed by openCV with python code
#  and is used as part of the image_streaming_app_user_annotate.py Flask controller
#

########################################################
######## function to return the CPU temperature ########
########################################################
# Return CPU temperature as a character string                                     
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))


import cv2     # import the python openCV library
import time    # import the required time functions
import os
 
class Camera():

    # Constructor... build the new camera object with __init__ and additional width & height attributes
    def __init__(self, width, height, bright, contrast, sat, hue, gain, exp, wbal, focus):
        self.width = width
        self.height = height
        self.bright = bright
        self.contrast = contrast
        self.sat = sat
        self.hue = hue
        self.gain = gain
        self.exp = exp
        self.wbal = wbal
        self.focus = focus

        global stop_streaming

        # use the openCV VideoCapture class
        self.cap = cv2.VideoCapture(-1)  # Prepare the camera... using -1 selects the first working camera
        cap_count = 0
        while(self.cap.isOpened() != True):
            print("Camera warming up ...")
            time.sleep(1)  # wait a second to make sure the camera is ready
            cap_count = cap_count + 1
            if cap_count > 3:   # check if camera is not coming up
                print("Camera not restarting - try to stop streaming")
                stop_streaming = True
                self.cap.release()
                break

        # use openCV VideoCapture::set - to set both the width and height camera parameters
        self.cap.set(3, self.width)
        self.cap.set(4, self.height)

        # set the more 'exotic' parameters but only if they have a non-9999 value
        if self.bright != 9999:
            self.cap.set(10, self.bright)   # brightness   min: 0, max: 255, increment:1  typical: 120
        if self.contrast != 9999:
            self.cap.set(11, self.contrast) # contrast     min: 0, max: 255, increment:1  typical: 50
        if self.sat != 9999:
            self.cap.set(12, self.sat)      # saturation   min: 0, max: 255, increment:1  typical: 70
        if self.hue != 9999:
            self.cap.set(13, self.hue)      # hue         
        if self.gain != 9999:
            self.cap.set(14, self.gain)     # gain         min: 0, max: 127, increment:1  typical: 50
        if self.exp != 9999:
            self.cap.set(15, self.exp)      # exposure     min: -7, max: -1, increment:1  typical: -3
        if self.wbal != 9999:
            self.cap.set(17, self.wbal)     # white_balance  min: 4000, max: 7000, increment:1  typical: 5000
        if self.focus != 9999:
            self.cap.set(28, self.focus)    # focus        min: 0, max: 255, increment:5  typical: 0 ??
  
        time.sleep(0.2)  # wait another couple of seconds to make sure the camera is ready
        print ("Resolution set to " + str(self.width) + "x" + str(self.height) + " ...")

        # Prepare Capture: VideoCapture::read returns a true/false plus the next video frame or null
        self.ret, self.frame = self.cap.read()

    # Function for creating an image from camera frame for browser streaming with Flask...	
    def get_frame(self, width):
        global stop_streaming
        frame_state = "not set"
        if str(self.width) == "640":
            textpos1 = "+538+465"
            textpos2 = "+15+465"
            textsize = "18"
        elif str(self.width) == "320":
            textpos1 = "+230+225"
            textpos2 = "+10+225"
            textsize = "16"
        elif str(self.width) == "160":
            textpos1 = "+101+115"
            textpos2 = "+3+115"
            textsize = "12"
        elif str(self.width) == "176":
            textpos1 = "+110+138"
            textpos2 = "+5+138"
            textsize = "13"
        elif str(self.width) == "352":
            textpos1 = "+250+265"
            textpos2 = "+12+265"
            textsize = "17"
        elif str(self.width) == "800":
            textpos1 = "+660+580"
            textpos2 = "+20+580"
            textsize = "22"
        elif str(self.width) == "1280":
            textpos1 = "+1150+685"
            textpos2 = "+25+685"
            textsize = "24"
        elif str(self.width) == "1920":
            textpos1 = "+1720+1030"
            textpos2 = "+35+1030"
            textsize = "28"

        # open a .jpg file to write in binary in the special ramdrive folder
        #   which has to have been set up previously by editing  /etc/fstab
        filename = "/mnt/ramimage/stream.jpg"
        self.frames = open(filename, 'wb+') 


        s, img = self.cap.read()   # get the next frame from the camera
        if s:	# check frame captures without errors...
            cv2.imwrite(filename, img)	# Save image to the 'opened' .jpg  ...
            # get time and CPU temp to add to the annotation
            now = " " + time.strftime('%H:%M:%S') + " "
            CPU_temp = getCPUtemperature()
            # construct a command to 'annotate' the image file
            annotation1 = " CPU:" + CPU_temp + "degC "
            os_image_command1 = "convert " + filename + " -font Courier -undercolor black -pointsize " + textsize + " -fill white -annotate " + textpos1 + " " + now + " " + filename
            os.system(os_image_command1) # execute command1
            os_image_command2 = "convert " + filename + " -font Courier -undercolor black -pointsize " + textsize + " -fill white -annotate " + textpos2 + " " + annotation1 + " " + filename
            os.system(os_image_command2) # execute command2
            frame_state = "OK"
        else:
            # display an error message on screen if a next frame has not been grabbed
            if frame_state != "not set" and frame_state != "error":
                print (frame_state + ": frame capture at: " + time.strftime('%H:%M %Z'))
                frame_state = "error"
                stop_streaming = True
                self.cap.release()
        return self.frames.read()  # return the grabbed frame as the image