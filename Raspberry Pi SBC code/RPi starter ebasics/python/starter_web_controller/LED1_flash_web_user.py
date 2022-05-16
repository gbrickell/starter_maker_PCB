#!/usr/bin/python
# Starter kit PCB version 1.0
# file name: LED1_flash_web_user.py
# Electronics testing Flask controller: python code as part of a Flask based web server system
#  which controls the flashing of a single LED on/off from a web interface
#  - this version of the app is for use by any non-root user and uses HTTP port 8000
# 
# the CLI command text below is for when the app is in the standard folder
#  BUT this will need to be updated for the individual installation/user name which may be different
# command to run: python3 ./starter_maker_kit1/RPi_code/starter_ebasics/starter_web_controller/LED1_flash_web_user.py
#
# But this can also be run from the Thonny IDE

#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# main code 
#
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

import RPi.GPIO as GPIO   # this imports the module to allow the GPIO pins to be easily utilised
import time               # this imports the module to allow various time functions to be used

GPIO.setwarnings(False)

# This code sets the RPi to use the BCM (Broadcom) pin numbers which is usually the default but is positively set here
GPIO.setmode(GPIO.BCM)

positive_pin = 21  # this is the GPIO pin that the RED LED positive leg (via the resistor) is connected to

global ontime
global offtime
global ledcycles
global status

ontime = "0.5"   # time that the LED is ON - set as a string so that it is more easily passed to/from web
offtime = "0.5"  # time that the LED is OFF - set as a string so that it is more easily passed to/from web
ledcycles = "10" # number of times the ON/OFF cycle is run - set as a string so that it is more easily passed to/from web

# this web interface demonstration code uses Flask - a lightweight web server that integrates with Python
# import the various Flask libraries that are needed
from flask import Flask, render_template
from flask import request
from flask import Response  # used as a custom Response for the video streamimg


# now create a Flask web server object which is run by the code at the end of the program
run_electronics_app01 = Flask(__name__)  # creates a Flask object called run_electronics_app01

# ------------------------------------------------------------------------------------
# the following functions are run depending upon what URL is selected from the HTML 
# ------------------------------------------------------------------------------------

################################################################################
# this route goes to the 'selection mode' routine when the URL root is selected
#    - the 'selection mode' routine provides a simple interface to 
#      either set some parameters or to run the LED lighting process
################################################################################
@run_electronics_app01.route("/") # run the code below this function when the URL root is accessed
def start():
    global ontime
    global offtime
    global ledcycles
    global status

    select_mode = "selection routine",

    GPIO.cleanup()   # set this here to make the GPIO pins safe since they may have been set HIGH elsewhere
    print ("GPIO pins cleaned up - route /")

    # update time now
    timenow = time.strftime('%H:%M %Z')

    status = "main selection"

    template_data = {
        'title' : "mode selection",   # this sets the browser title template parameter
        'time_now' : timenow,         # this sets the current time template parameter
        'on_time' : ontime,           # this sets the current value for the led on time template parameter
        'off_time' : offtime,         # this sets the current value for the led off time template parameter
        'led_cycles' : ledcycles,     # this sets the current value for the led cycles template parameter
        'stat_text' : status,         # this sets the current value for the status text

    }

    return render_template('electronics_select_mode1.html', **template_data)


##########################################################################################
# this route defines the actions taken when in 'selection mode'
##########################################################################################
@run_electronics_app01.route("/<choice_mode>")  # run the code below this function when URL /<choice_mode> is accessed from select_mode1.html where choice_mode is a variable
def mode_selection(choice_mode=None):
    global ontime
    global offtime
    global ledcycles
    global status

    none_selected = "no mode selected"
    if status != "RED LED switched ON" :   # don't clean up if the LED is supposed to be ON
        GPIO.cleanup()   # set this here to make the GPIO pins safe since they may have been set HIGH elsewhere
        print ("GPIO pins cleaned up - route <choice mode>")

    # update time now
    timenow = time.strftime('%H:%M %Z')

    status = ""

    if choice_mode == 'ledlight':   # run this section of code if 'ledlight' is chosen at the main selection HTML template

        status = "RED LED being controlled"
        # template data: individual parameters that are passed for use in the template to render the browser display
        template_data = {
            'title' : "LED lighting options", # this sets the browser title template parameter
            'time_now' : timenow,                 # this sets the current time template parameter
            'on_time' : ontime,                   # this sets the current value for the led on time template parameter
            'off_time' : offtime,                 # this sets the current value for the led off time template parameter
            'led_cycles' : ledcycles,             # this sets the current value for the led cycles template parameter
            'stat_text' : status,                 # this sets the current value for the status text

        }

        # echo the values of the key LED parameters to the screen
        print ("LED on time : " + ontime)
        print ("LED off time: " + offtime)
        print ("LED cycles  : " + ledcycles)

        return render_template('run_led1.html', **template_data)   # run the 'run_led1.html' template

    elif choice_mode == 'ledsetup':   # run this section of code if 'ledsetup' is chosen at the main selection HTML template

        status = "RED LED being set up"
        # template data: individual parameters that are passed for use in the template to render the browser display
        template_data = {
            'title' : "update LED parameters",    # this sets the browser title template parameter
            'time_now' : timenow,                 # this sets the current time template parameter
            'on_time' : ontime,                   # this sets the current value for the led on time template parameter
            'off_time' : offtime,                 # this sets the current value for the led off time template parameter
            'led_cycles' : ledcycles,             # this sets the current value for the led cycles template parameter
            'stat_text' : status,                 # this sets the current value for the status text

        }

        # echo the values of the key LED parameters to the screen
        print ("LED on time : " + ontime)
        print ("LED off time: " + offtime)
        print ("LED cycles  : " + ledcycles)

        return render_template('led1_setup_mode.html', **template_data)    # run the 'led1_setup_mode.html' template

    else:     # shouldn't ever arrive here but run this section of code if  neither 'ledlight' nor 'ledsetup' are selected at the template
        template_data = {
            'title' : "mode selection",         # this sets the browser title template parameter
            'time_now' : timenow,               # this sets the current time template parameter
            'on_time' : ontime,                 # this sets the current value for the led on time template parameter
            'off_time' : offtime,               # this sets the current value for the led off time template parameter
            'led_cycles' : ledcycles,           # this sets the current value for the led cycles template parameter
            'stat_text' : status,               # this sets the current value for the status text

        }
        return render_template('electronics_select_mode1.html', **template_data)


##################################################################################################################
# this route defines the actions selected when in LED set up mode
##################################################################################################################
@run_electronics_app01.route("/ledsetup/<setup_command>")  # run the code below this function when URL /camsetup/<setup_command> is accessed where <setup_command> is a variable
def update_ledsettings(setup_command=None):
    global ontime
    global offtime
    global ledcycles
    global status

    none_selected = "no mode selected"
    GPIO.cleanup()   # set this here to make the GPIO pins safe since they may have been set HIGH elsewhere
    print ("GPIO pins cleaned up - route /ledsetup/<setup_command>")

    # update time now
    timenow = time.strftime('%H:%M %Z')

    status = ""

    if setup_command == 'update_settings':
        # execute this set of code to update the LED lighting settings

        print ("request method: " + str(request.method))

        print ("new LED on time : " + str(request.args.get('ledontime')))
        ontime = str(request.args.get('ledontime'))

        print ("new LED off time: " + str(request.args.get('ledofftime')))
        offtime = str(request.args.get('ledofftime'))

        print ("new LED cycles: " + str(request.args.get('cyclesled')))
        ledcycles = str(request.args.get('cyclesled'))

        status = "LED parameters updated"

        # template data: individual parameters that are passed for use in the template to render the browser display
        template_data = {
            'title' : "LED parameters update",    # this sets the browser title template parameter
            'time_now' : timenow,                 # this sets the current time template parameter
            'on_time' : ontime,                   # this sets the current value for the led on time template parameter
            'off_time' : offtime,                 # this sets the current value for the led off time template parameter
            'led_cycles' : ledcycles,             # this sets the current value for the led cycles template parameter
            'stat_text' : status,                 # this sets the current value for the status text

        }

        return render_template('led1_setup_mode.html', **template_data)    # run the 'led1_setup_mode.html' template


    elif setup_command == 'select_mode':

        status = "main selection"
        print (" going back to select .....")
        template_data = {
            'title' : "mode selection",         # this sets the browser title template parameter
            'time_now' : timenow,               # this sets the current time template parameter
            'on_time' : ontime,                 # this sets the current value for the led on time template parameter
            'off_time' : offtime,               # this sets the current value for the led off time template parameter
            'led_cycles' : ledcycles,           # this sets the current value for the led cycles template parameter
            'stat_text' : status,               # this sets the current value for the status text

        }

        return render_template('electronics_select_mode1.html', **template_data)


##################################################################################################################
# this route defines the actions selected when in LED lighting mode
##################################################################################################################
@run_electronics_app01.route("/ledlight/<led_command>")  # run the code below this function when URL /ledlight/<led_command> is accessed where <led_command> is a variable
def run_led_lights(led_command=None):
    global ontime
    global offtime
    global ledcycles
    global status

    none_selected = "no mode selected"

    # update time now
    timenow = time.strftime('%H:%M %Z')

    if led_command == 'led_cycle':
        # execute this set of code to start the LED cycle on/off process

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(positive_pin, GPIO.OUT)  # this sets the GPIO pin to be an output 'type' i.e. it will apply 
                                            # about 3.3V to the pin when it is set HIGH (True)
                                            # need to set this here since GPIO.cleanup() is set everywhere else to be safe

        i=1
        while i <= int(ledcycles):           # this is the loop that flashes the LED on and off for ledcycles
            GPIO.output(positive_pin, True)  # LED switched on by making the GPIO go HIGH
            time.sleep(float(ontime))          # delay ontime seconds with it switched on
            GPIO.output(positive_pin, False) # LED switched off by making the GPIO pin go LOW
            time.sleep(float(offtime))         # delay offtime seconds with it switched off before looping back
            i += 1

        status = "LED lighting cycle just completed"

        # template data: individual parameters that are passed for use in the template to render the browser display
        template_data = {
            'title' : "LED lighting options",    # this sets the browser title template parameter
            'time_now' : timenow,                        # this sets the current time template parameter
            'on_time' : ontime,                          # this sets the current value for the led on time template parameter
            'off_time' : offtime,                        # this sets the current value for the led off time template parameter
            'led_cycles' : ledcycles,                    # this sets the current value for the led cycles template parameter
            'stat_text' : status,                        # this sets the current value for the status text

        }

        return render_template('run_led1.html', **template_data)    # run the 'run_led1.html' template

    elif led_command == 'led_on':
        # execute this set of code to switch the RED LED on

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(positive_pin, GPIO.OUT)  # this sets the GPIO pin to be an output 'type' i.e. it will apply 
                                            # about 3.3V to the pin when it is set HIGH (True)
                                            # need to set this here since GPIO.cleanup() is set everywhere else to be safe

        GPIO.output(positive_pin, True) # LED switched on by making the GPIO pin go HIGH
        print(" ")
        print("RED LED switched ON")
        print(" ")

        status = "RED LED switched ON"

        # template data: individual parameters that are passed for use in the template to render the browser display
        template_data = {
            'title' : "LED lighting options",    # this sets the browser title template parameter
            'time_now' : timenow,                    # this sets the current time template parameter
            'on_time' : ontime,                      # this sets the current value for the led on time template parameter
            'off_time' : offtime,                    # this sets the current value for the led off time template parameter
            'led_cycles' : ledcycles,                # this sets the current value for the led cycles template paramete
            'stat_text' : status,                    # this sets the current value for the status text

        }

        return render_template('run_led1.html', **template_data)    # run the 'run_led1.html' template

    elif led_command == 'led_off':
        # execute this set of code to stop the LED lighting process and set all the GPIO pins safe

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(positive_pin, GPIO.OUT)  # this sets the GPIO pin to be an output 'type' i.e. it will apply 
                                            # about 3.3V to the pin when it is set HIGH (True)
                                            # need to set this here since GPIO.cleanup() is set everywhere else to be safe

        GPIO.output(positive_pin, False) # LED switched off by making the GPIO pin go LOW
        print(" ")
        print("RED LED switched OFF  and GPIO pins 'cleaned up' just in case")
        print(" ")
        print(" ")
        print(" ")
        GPIO.cleanup()
        print ("GPIO pins cleaned up /ledlight/<led_off>")

        status = "RED LED switched OFF"

        # template data: individual parameters that are passed for use in the template to render the browser display
        template_data = {
            'title' : "LED lighting options",    # this sets the browser title template parameter
            'time_now' : timenow,                    # this sets the current time template parameter
            'on_time' : ontime,                      # this sets the current value for the led on time template parameter
            'off_time' : offtime,                    # this sets the current value for the led off time template parameter
            'led_cycles' : ledcycles,                # this sets the current value for the led cycles template paramete
            'stat_text' : status,                    # this sets the current value for the status text

        }

        return render_template('run_led1.html', **template_data)    # run the 'run_led1.html' template


    elif led_command == 'select_mode':

        print (" going back to select .....")
        status = "main selection"

        template_data = {
            'title' : "mode selection",         # this sets the browser title template parameter
            'time_now' : timenow,               # this sets the current time template parameter
            'on_time' : ontime,                 # this sets the current value for the led on time template parameter
            'off_time' : offtime,               # this sets the current value for the led off time template parameter
            'led_cycles' : ledcycles,           # this sets the current value for the led cycles template parameter
            'stat_text' : status,               # this sets the current value for the status text

        }

        return render_template('electronics_select_mode1.html', **template_data)


##################################################################################
# the code below is the last code in the system
# when running a Flask server you need sudo access to use the noaml HTTP port 80
# without sudo a non-standard port must be used e.g. 8000 is used below
##################################################################################

if __name__ == "__main__":
    run_electronics_app01.run(host='0.0.0.0', port=8000, debug=False, threaded=True) # 0.0.0.0 means any device on the network can access the web app
    # use port 8000 so that you do not have to run the app as root (ie use sudo) which is necessary if the 'production' port 80 is used

    # debug version
    #run_electronics_app01.run(host='0.0.0.0', port=8000, debug=True)   # 0.0.0.0 means any device on the network can access the web app




