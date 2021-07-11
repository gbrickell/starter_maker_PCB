#!/usr/bin/python
# Starter Kit PCB - image taking routine using a button with Red Amber and Green LED indicator
#
# command: python3 /home/pi/starter_maker_kit1/RPi_code/image_taking/button_led_take_image.py
#
# this script introduces the use of pulse width modulation (PWM) a technique used to control a variety of 
# devices (motors, servos as well as LEDs) esentially by switching them on and off very very fast
# PWM has 2 main parameters:
#  - Frequency: the number of time per second that a pulse is generated
#  - Duty Cycle: the % of time during a single cycle that the signal is high
#   for more information see https://pythonhosted.org/RPIO/pwm_py.html
#   and https://en.wikipedia.org/wiki/Pulse-width_modulation

import time                # this imports the module to allow various simple time functions to be used
import RPi.GPIO as GPIO    # this imports the module to allow the GPIO pins to be easily utilised
import os                  # this imports the module to allow direct CLI commands to be run
from builtins import input # allows compatibility for input between Python 2 & 3
import subprocess

# This code sets the RPi to use the BCM (Broadcom) pin numbers which is usually the default but is positively set here
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)   # avoids various warning messages about GPIO pins being already in use 

button_pin = 26  # this is the GPIO pin that one side of the tactile button is connected to

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
# this is a special setting that indicates when a pin changes from LOW to HIGH ie when the button is pressed

red_positive_pin = 21    # this is the GPIO pin that the RED LED leg (via the resistor) is connected to

amber_positive_pin = 20  # this is the GPIO pin that the AMBER LED leg (via the resistor) is connected to

green_positive_pin = 16  # this is the GPIO pin that the GREEN LEDB leg (via the resistor) is connected to

GPIO.setup(red_positive_pin, GPIO.OUT)    # this sets the RED GPIO pin to be an output 'type' i.e. it will 
                                          # apply about 3.3V to the pin when it is set HIGH (True)

GPIO.setup(amber_positive_pin, GPIO.OUT)  # this sets the AMBER GPIO pin to be an output 'type' i.e. it will 
                                          # apply about 3.3V to the pin when it is set HIGH (True)

GPIO.setup(green_positive_pin, GPIO.OUT)  # this sets the GREEN GPIO pin to be an output 'type' i.e. it will 
                                          # apply about 3.3V to the pin when it is set HIGH (True)

# Start the Pulse Width Modulation (PWM) software on each of the LED GPIO control pins which will allow the
#  brightness of the LEDs to be controllable: a quite high frequency is needed for LEDs to avoid visible flicker

pwmRed = GPIO.PWM(red_positive_pin, 500)      # this sets a frequency of 500 i.e. 500 cycles per second
pwmRed.start(0)                               # this sets an inital Duty Cycle of 0% i.e. off all the time

pwmAmber = GPIO.PWM(amber_positive_pin, 500)    # this sets a frequency of 500 i.e. 500 cycles per second
pwmAmber.start(0)                              # this sets an inital Duty Cycle of 0% i.e. off all the time

pwmGreen = GPIO.PWM(green_positive_pin, 500)  # this sets a frequency of 500 i.e. 500 cycles per second
pwmGreen.start(0)                             # this sets an inital Duty Cycle of 0% i.e. off all the time

# set LED to red whilst everything is starting up
pwmRed.ChangeDutyCycle(100)     # red LED switched to 100% (fully on) by changing the Duty Cycle
pwmGreen.ChangeDutyCycle(0)     # green LED switched to 0% (off) by changing the Duty Cycle
pwmAmber.ChangeDutyCycle(0)     # amber LED switched to 0% (off) by changing the Duty Cycle
time.sleep(1.5)                 # wait for 1.5s just so the red LED is actually seen !

# this is a function to indicate when the button is pressed 
def btn_pressed():
    # if button is pressed GPIO.input will report FALSE
    if not GPIO.input(button_pin):
        return 1

# define the folder where images will be stored
time_subfolder = " "
print (" ")
print (" ****************************************************************************************************")
print (" All button triggered images will be stored under /home/pi/starter_maker_kit1/RPi_code/image_taking/ ")
print ("   ..... but you must now enter a subfolder name")
print ("   ..... just hit RETURN for the default of 'single_image_led_folder'")
while len(time_subfolder) <= 5 or " " in time_subfolder :
    time_subfolder = input(" Enter sub-folder name - must be more than 5 characters and no spaces (CTRL C to stop? )") or "single_image_led_folder"
print (" ****************************************************************************************************")
print (" ")

imagefolder = "/home/pi/starter_maker_kit1/RPi_code/image_taking/" + time_subfolder + "/"

# create the directory if it does not exist
if not os.path.exists(imagefolder):
    os.makedirs(imagefolder)      # execute the folder creation command
    # create a command string to make sure the new folder is 'owned' by the pi user
    os_chown_command = "chown -R pi:pi " + imagefolder
    os.system(os_chown_command)   # execute the file ownership change command
    print (imagefolder + " folder created")
else:
    print (imagefolder + " already exists, so no need to create it")
print (" ")

# get the current date and time in a specified format
# as this string will be used in the stored image file name
# only use characters that are allowed in Windows files or 
# the file will not download from the Pi to a Windows machine
now = time.strftime("%Y-%m-%d_%H.%M.%S")   # this creates a string in a designated format e.g. YYYY-mm-dd_HH.MM.SS


print (now + " - program running : press the button to take a single image or type CTRL-C to stop the program")
try:    # this loop is not strictly necessary but it does allow the script to be easily stopped with CTRL-C
    while True:  # this is the loop that checks if the button is pressed and takes an image if it is

        # set LED to green to show that the system is ready
        pwmRed.ChangeDutyCycle(0)          # red LED switched to 0% (off) by changing the Duty Cycle
        pwmGreen.ChangeDutyCycle(100)      # green LED switched to 100% (fully on) by changing the Duty Cycle
        pwmAmber.ChangeDutyCycle(0)        # amber LED switched to 0% (off) by changing the Duty Cycle

        while not btn_pressed():
            pass           # if the button is not pressed just loop endlessly

        # button pressed so take a single image and set LED to amber whist this is happening
        pwmRed.ChangeDutyCycle(0)        # red LED switched to 0% (off) by changing the Duty Cycle
        pwmGreen.ChangeDutyCycle(0)      # green LED switched to 0% (off) by changing the Duty Cycle
        pwmAmber.ChangeDutyCycle(100)    # amber LED switched to 100% (fully on) by changing the Duty Cycle

        now = time.strftime("%Y-%m-%d_%H.%M.%S") # get the time and date the button was pressed to be used in the file name
        image_name = imagefolder + "single_image_" + now + ".jpg"    # create the full file name including the path
        print (now + " - button pressed - single image being taken")
        # create the full fswebcam command string: 
        # skip first 5 frames, 640x480 size, no messages, no banner, 80% compression, stored file name
        # the example below does not have any flip or rotate options which may be needed
        # add --rotate <angle> where <angle> can be 90, 180 or 270 if rotation needed
        # add --flip <direction> where <direction> can be h or v if you do want to flip the image for some reason
        os_image_command = "fswebcam -S 5 -r 640x480 -q --no-banner --jpeg 80 " + image_name  
        os.system(os_image_command)          # take the image using the fswebcam command string
        # create the command string to make sure the new file is 'owned' by the pi usert
        os_chown_command = "chown pi:pi " + image_name
        os.system(os_chown_command)          # execute the file ownership change command

        time.sleep(1)      # wait a short interval before cycling back to allow the image capture to complete
        print (" ")
        print (" *************************************************************************************************************")
        print (" image taken and stored as: " + image_name)
        print (" *************************************************************************************************************")
        print (" ")

        # input the response to showing the image just taken Y/N
        #  this example shows how to repeat the request if the input is not the required value
        showimage = "-"
        while showimage != "N" and showimage != "n" and showimage != "Y" and showimage != "y":
            showimage = str(input("Do you want to show the captured image for 10 seconds - enter Y or N? "))
        if showimage == "Y" or showimage == "y":
            # display the image using 'feh' (see https://man.finalrewind.org/1/feh/) with the following parameters:
            # --hide-pointer does what it says
            # -x  borderless window
            # -B  background colour for transparent parts - set by next parameter i.e. black
            # -g (geometry) widthxheight+x-offset+y-offset - set by next parameter i.e. 640x480+400+200
            #  
            print ("press ESC to stop showing the image")
            image = subprocess.Popen(["feh", "--hide-pointer", "-x", "-B", "black", "-g", "640x480+400+200", image_name])
            time.sleep(10)

        print (" ")
        print (" ")
        print (" ***************************************************************")
        print (" ")
        print (" starting another image capture cycle: ")
        print (" ")
        print (" press the button again to take another single image or type CTRL-C to stop the program")
        # close the image - if it was shown - before starting the next cycle
        if showimage == "Y" or showimage == "y":
            image.kill()


finally:  # this code is run when the try is interrupted with a CTRL-C
    # close the image - if it was shown just before a CTRL-C
    if showimage == "Y":
        image.kill()

    print(" ")
    print("Cleaning up the GPIO pins before stopping")
    print(" ")
    print(" ")
    print(" ")
    GPIO.cleanup()
    
# The cleanup command sets all the pins back to inputs which protects the
# Pi from accidental shorts-circuits if something metal touches the GPIO pins.
