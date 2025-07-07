# Starter Maker PCB version of LED_button_flash.py that lights a LED when the button is pressed
# Run from Thonny using the file that may be stored at /home/pi/starter_maker_PCB1/Pico_MPcode/LED_button_flash.py
# the file path /home/pi/starter_maker_PCB1/Pico_MPcode/ will need to be changed if you have stored your code elsewhere

import machine   # this imports the main Pico library that allows the GPIO pins and many other things to be easily utilised
from machine import Pin
import utime     # this imports the microcontroller version of the time library to allow various time functions to be used

positive_pin = 10  # this is the GPIO pin that the RED LED positive leg (via the resistor) is connected to
button_pin = 14    # this is the GPIO pin that one side of the (top: button1) tactile switch is connected to

# configure a led on the GPIO pin to be an output 'type' i.e. it will apply about 3.3V to the pin when it is set HIGH (True)
redled = machine.Pin(positive_pin, machine.Pin.OUT)
button = machine.Pin(button_pin, machine.Pin.IN, machine.Pin.PULL_UP)

###########################################################
# this is a function to indicate when the button is pressed
###########################################################
def btn_pressed():
    # if button is pressed button.value() will report LOW
    if button.value() == 0:
        return 1

###########
# main code
###########

print (" ")
print ("program running: press the button to light the red LED or CTRL-C/Thonny STOP to stop ")
print (" ")

try:    # this loop is not strictly necessary but it does allow the script to 'clean up' after a CTRL-C
    while True:  # this is the loop that checks if the button is pressed and switches the LED on if it is
        redled.value(0)          # LED switched off by making the GPIO pin go LOW
        while not btn_pressed():
            pass                 # if not pressed just loop endlessly

        print(" ")
        print("button pressed and red LED switched on")
        print(" ")
        redled.value(1)          # LED switched on by making the GPIO go HIGH
        utime.sleep(3)           # delay 3 seconds with it switched on and then repeat loop
        print ("press the button again to light the red LED or CTRL-C to stop ")

except KeyboardInterrupt:
    print(" ")
    print("Cleaning up the GPIO pins before stopping")
    print(" ")
    print(" ")
    print(" ")
    redled.value(0)                            # set the GPIO pin LOW
    machine.Pin(positive_pin, machine.Pin.IN)  # now make the pin an INPUT

