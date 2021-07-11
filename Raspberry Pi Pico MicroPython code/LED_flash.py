# Starter Maker Kit version of LED_flash.py that flashes a single LED on/off
# Run from Thonny using the file that may be stored at /home/pi/starter_maker_kit1/Pico_MPcode/LED_flash.py
# the file path /home/pi/starter_maker_kit1/Pico_MPcode/ will need to be changed if you have stored your code elsewhere

import machine   # this imports the main Pico library that allows the GPIO pins and many other things to be easily utilised
from machine import Pin
import utime     # this imports the microcontroller version of the time library to allow various time functions to be used

positive_pin = 10  # this is the GPIO pin that the RED LED positive leg (via the resistor) is connected to

# configure a led on the GPIO pin to be an output 'type' i.e. it will apply about 3.3V to the pin when it is set HIGH (True)
redled = machine.Pin(positive_pin, machine.Pin.OUT)

###########
# main code
###########

print (" ")
print ("program running - LED should be flashing:")
print ("  press CTRL-C or the Thonny Stop button to stop ")
print (" ")

try: # this loop is not strictly necessary but it does allow the script to 'clean up' after a CTRL-C
    while True:  # this is the loop that continuously flashes the LED on and off every half second
        redled.value(1)    # LED switched on by making the GPIO go HIGH
        utime.sleep(0.5)   # delay 0.5 seconds with it switched on
        redled.value(0)   # LED switched off by making the GPIO pin go LOW
        utime.sleep(0.5)    # delay 0.5 seconds with it switched off before looping back

except KeyboardInterrupt:
    print(" ")
    print("Cleaning up the GPIO pins before stopping")
    print(" ")
    print(" ")
    print(" ")
    redled.value(0)                            # set the GPIO pin LOW
    machine.Pin(positive_pin, machine.Pin.IN)  # now make the pin an INPUT