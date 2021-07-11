#!/usr/bin/python
# button_timer_take_video.py - video taking routine using a button set timer with RGB LED indicator
#
# command: python3 /home/pi/starter_maker_kit1/RPi_code/image_taking/button_timer_take_video.py
#
# this script uses pulse width modulation (PWM) a technique used to control a variety of 
# devices (motors, servos as well as LEDs) esentially by switching them on and off very very fast
# PWM has 2 main parameters:
#  - Frequency: the number of times per second that a pulse is generated
#  - Duty Cycle: the % of time during a single cycle that the signal is high
#   for more information see https://pythonhosted.org/RPIO/pwm_py.html
#   and https://en.wikipedia.org/wiki/Pulse-width_modulation

import time                # this imports the module to allow various simple time functions to be used
import RPi.GPIO as GPIO    # this imports the module to allow the GPIO pins to be easily utilised
import os                  # this imports the module to allow direct CLI commands to be run
from builtins import input # allows compatibility for input between Python 2 & 3

# This code sets the RPi to use the BCM (Broadcom) pin numbers which is usually the default but is positively set here
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)   # avoids various warning messages about GPIO pins being already in use

button_pin = 26  # this is the GPIO pin that one side of tactile button 2 is connected to

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
# this is a special setting that indicates when a pin changes from LOW to HIGH ie when the button is pressed

red_positive_pin = 22    # this is the GPIO pin that the RED RGB leg (via the resistor) is connected to

green_positive_pin = 27  # this is the GPIO pin that the GREEN RGB leg (via the resistor) is connected to

blue_positive_pin = 17   # this is the GPIO pin that the BLUE RGB leg (via the resistor) is connected to

buzzer_pin = 12          # this is the GPIO pin that the buzzer positive leg is connected to

GPIO.setup(red_positive_pin, GPIO.OUT)    # this sets the RED GPIO pin to be an output 'type' i.e. it will 
                                          # apply about 3.3V to the pin when it is set HIGH (True)

GPIO.setup(green_positive_pin, GPIO.OUT)  # this sets the GREEN GPIO pin to be an output 'type' i.e. it will 
                                          # apply about 3.3V to the pin when it is set HIGH (True)

GPIO.setup(blue_positive_pin, GPIO.OUT)   # this sets the BLUE GPIO pin to be an output 'type' i.e. it will 
                                          # apply about 3.3V to the pin when it is set HIGH (True)

GPIO.setup(buzzer_pin, GPIO.OUT)    # this sets the buzzer GPIO pin to be an output 'type' i.e. it will apply 
                                    # about 3.3V to the pin when it is set HIGH (True)

freq = 1000.0          # this is the frequency (cycles/second ie Hz) that the buzzer is switched on/off to make a sound
period = 1.0 / freq             # this is the time period in seconds of a full cycle for the buzzer
half_cycle_time = period / 2.0  # this is the time period for half a cylcle ie the on and off times for the buzzer

# Start the Pulse Width Modulation (PWM) software on each of the LED GPIO control pins which will allow the
#  brightness of the LEDs to be controllable: a quite high frequency is needed for LEDs to avoid visible flicker

pwmRed = GPIO.PWM(red_positive_pin, 500)      # this sets a frequency of 500 i.e. 500 cycles per second
pwmRed.start(0)                               # this sets an inital Duty Cycle of 0% i.e. off all the time

pwmGreen = GPIO.PWM(green_positive_pin, 500)  # this sets a frequency of 500 i.e. 500 cycles per second
pwmGreen.start(0)                             # this sets an inital Duty Cycle of 0% i.e. off all the time

pwmBlue = GPIO.PWM(blue_positive_pin, 500)    # this sets a frequency of 500 i.e. 500 cycles per second
pwmBlue.start(0)                              # this sets an inital Duty Cycle of 0% i.e. off all the time

# set LED to red whilst everything is starting up
pwmRed.ChangeDutyCycle(100)     # red LED switched to 100% (fully on) by changing the Duty Cycle
pwmGreen.ChangeDutyCycle(0)     # green LED switched to 0% (off) by changing the Duty Cycle
pwmBlue.ChangeDutyCycle(0)      # blue LED switched to 0% (off) by changing the Duty Cycle
time.sleep(1.5)                 # wait for 1.5s just so the red LED is actually seen !

# this is a function to indicate when the button is pressed 
def btn_pressed():
    # if button is pressed GPIO.input will report FALSE as we set pull_up_down=GPIO.PUD_UP
    if not GPIO.input(button_pin):
        return 1

# define the folder where videos will be stored
video_subfolder = " "
print (" ")
print (" ***************************************************************************")
print (" All button timed videos will be stored under /home/pi/RPi_maker_kit5/image_taking/ ")
print ("   ..... but you must now enter a subfolder name")
print ("   ..... just hit RETURN for the default of 'button_video_timer_folder'")
while len(video_subfolder) <= 5 or " " in video_subfolder :
    video_subfolder = input(" Enter sub-folder name - must be more than 5 characters and no spaces (CTRL C to stop? )") or "button_video_timer_folder"
print (" ***************************************************************************")
print (" ")

# build the full path as a text string
videofolder = "/home/pi/RPi_maker_kit5/image_taking/" + video_subfolder + "/"

# create the directory if it does not exist
if not os.path.exists(videofolder):
    os.makedirs(videofolder)      # execute the folder creation command
    # create a command string to make sure the new folder is 'owned by the pi user so that it is easier to manage
    os_chown_command = "chown -R pi:pi " + videofolder
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

print (now + " - program running: type CTRL-C to stop the program")
print (" ")

try:    # this loop is not strictly necessary but it does allow the script to be easily stopped with CTRL-C
    while True:  # this is the loop that checks if a button is pressed and takes an video if it is

        # set LED to green to show that the system is ready
        pwmRed.ChangeDutyCycle(0)          # red LED switched to 0% (off) by changing the Duty Cycle
        pwmGreen.ChangeDutyCycle(100)      # green LED switched to 100% (fully on) by changing the Duty Cycle
        pwmBlue.ChangeDutyCycle(0)         # blue LED switched to 0% (off) by changing the Duty Cycle

        # input the timer duration in seconds
        #  this example shows how to repeat the request if the input is not the required value
        timerduration = 0
        print (" ")
        print (" ***************************************************************************")
        while timerduration < 5:
            timerduration = float(input("Enter ** countdown timer duration ** in seconds - must be more than 5 seconds? (CTRL C to stop)"))
        print (" ***************************************************************************")
        print (" ")

        # input the video duration in seconds
        #  this example shows how to repeat the request if the input is not the required value
        clipduration = 0
        print (" ")
        print (" ***************************************************************************")
        while clipduration <= 0 or clipduration > 59:
            clipduration = float(input("Enter video clip duration in seconds (1-59)? (CTRL C to stop)"))
        print (" ***************************************************************************")
        print (" ")

        print ("press button 2 to start the timer countdown before taking a short video clip or type CTRL-C to stop the program")
        print (" ")

        while not btn_pressed():
            pass           # if the button is not pressed just loop endlessly

        # button pressed so take start the timer and set LED to flash yellow whist this is happening
        tstart = time.time()

        # now flash the LED blue and beep the buzzer intermittently for the last few seconds whilst the timer runs down
        while (time.time() - tstart) < timerduration:
            timeleft = timerduration - (time.time() - tstart)
            #print ("time left: " + str(timeleft) + " seconds")
            pwmRed.ChangeDutyCycle(0)        # red LED switched to 0% (off) by changing the Duty Cycle
            pwmGreen.ChangeDutyCycle(0)      # green LED switched to 0% (off) by changing the Duty Cycle
            pwmBlue.ChangeDutyCycle(100)     # blue LED switched to 100% (fully on) by changing the Duty Cycle
            time.sleep(0.1)
            pwmRed.ChangeDutyCycle(0)        # red LED switched to 0% (off) by changing the Duty Cycle
            pwmGreen.ChangeDutyCycle(0)      # green LED switched to 0% (off) by changing the Duty Cycle
            pwmBlue.ChangeDutyCycle(0)       # blue LED switched to 0% (off) by changing the Duty Cycle
            time.sleep(0.1)
            if (timeleft) < 3:     # sound buzzer for last 3 seconds
                for x in range(0, 200):
                    GPIO.output(buzzer_pin, True)
                    time.sleep(half_cycle_time)     # 1 half cycle is very short !
                    GPIO.output(buzzer_pin, False)
                    time.sleep(half_cycle_time)        
        
        # timer count down complete - so make sure the LED is still on blue and take video
        pwmRed.ChangeDutyCycle(0)        # red LED switched to 0% (off) by changing the Duty Cycle
        pwmGreen.ChangeDutyCycle(0)      # green LED switched to 0% (off) by changing the Duty Cycle
        pwmBlue.ChangeDutyCycle(100)     # blue LED switched to 100% (fully on) by changing the Duty Cycle

        now = time.strftime("%Y-%m-%d_%H.%M.%S") # get the time and date the button was pressed to be used in the file name
        video_name = videofolder + "video_clip_" + now + ".avi"    # create the full file name including the path
        print (now + " - button pressed - video started")
        # create the relatively simple full ffmpeg command string: 
        # video4linux2 (v4l2) format, 640x480 size, input from camera, elapsed time in HH:MM:SS format, output video name
        # the example below does not have any rotate options which may be needed
        # add '-vf transpose=clock' for 90 degrees - use transpose=cclock for -90 or 270 degrees 
        #     and use transpose=clock,transpose=clock for 180 degrees ie do it twice
        os_video_command = "ffmpeg -f video4linux2 -s 640x480 -i /dev/video0 -t 00:00:" + str(int(clipduration)).zfill(2) + " " + video_name  
        print (os_video_command)
        os.system(os_video_command)          # start the video using the ffmpeg command string
        # create the command string to make sure the new file is 'owned by the pi user so that it is easier to manage
        os_chown_command = "chown pi:pi " + video_name
        os.system(os_chown_command)          # execute the file ownership change command

        time.sleep(1)      # wait a short interval before cycling back to allow the video capture to complete

        print (" ")
        print (" ***************************************************************")
        print (" video taken and stored as: " + video_name)
        print (" ***************************************************************")
        print (" ")

        # input the response to showing the video Y/N
        #  this example shows how to repeat the request if the input is not the required value
        showvideo = "-"
        while showvideo != "N" and showvideo != "Y":
            showvideo = str(input("Do you want to show the captured video now - enter Y or N? "))
        if showvideo == "Y":
            os.system("omxplayer --win '300 200 940 680' " + video_name)
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

