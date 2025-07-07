# starter maker PCB version of LED_flash.py that flashes a single LED on/off

# command to run this script:  python3 ./starter_maker_PCB1/RPi_code/starter_ebasics/LED_flash.py

# the file path ./maker_PCB5 will need to be changed if you have stored your code elsewhere

import RPi.GPIO as GPIO   # this imports the module to allow the GPIO pins to be easily utilised
import time               # this imports the module to allow various time functions to be used
GPIO.setwarnings(False)

# This code sets the RPi to use the BCM (Broadcom) pin numbers which is usually the default but is positively set here
GPIO.setmode(GPIO.BCM)

positive_pin = 21  # this is the GPIO pin that the RED LED positive leg (via the resistor) is connected to

GPIO.setup(positive_pin, GPIO.OUT)  # this sets the GPIO pin to be an output 'type' i.e. it will apply about 3.3V
                                    # to the pin when it is set HIGH (True)


###########
# main code
###########

print (" ")
print ("program running - LED should be flashing: CTRL-C to stop ")
print (" ")

try:           # this loop is not strictly necessary but it does allow the script to be easily stopped with CTRL-C
    while True:  # this is the loop that continuously flashes the LED on and off every half second
        GPIO.output(positive_pin, True)  # LED switched on by making the GPIO go HIGH
        time.sleep(0.5)             # delay 0.5 seconds with it switched on
        GPIO.output(positive_pin, False) # LED switched off by making the GPIO pin go LOW
        time.sleep(0.5)             # delay 0.5 seconds with it switched off before looping back
finally:  # this code is run when the try is interrupted with a CTRL-C
    print(" ")
    print("Cleaning up the GPIO pins before stopping")
    print(" ")
    print(" ")
    print(" ")
    GPIO.cleanup()
    
# The cleanup command sets all the pins back to inputs which protects the
# Pi from accidental shorts-circuits if something metal touches the GPIO pins.
    