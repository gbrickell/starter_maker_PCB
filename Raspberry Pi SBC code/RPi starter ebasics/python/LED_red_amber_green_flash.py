# starter maker PCB PCB version of LED_red_amber_green_flash.py that alternates on/off for three LEDs (red, amber & green)

# command to run this script:  python3 ./starter_maker_PCB1/RPi_code/starter_ebasics/LED_red_amber_green_flash.py

import RPi.GPIO as GPIO   # this imports the module to allow the GPIO pins to be easily utilised
import time               # this imports the module to allow various time functions to be used
GPIO.setwarnings(False)

# This code sets the RPi to use the BCM (Broadcom) pin numbers which is usually the default but is positively set here
GPIO.setmode(GPIO.BCM)

red_positive_pin = 21    # this is the GPIO pin that the red LED positive leg (via the resistor) is connected to

amber_positive_pin = 20  # this is the GPIO pin that the amber LED positive leg (via the resistor) is connected to

green_positive_pin = 16  # this is the GPIO pin that the green LED positive leg (via the resistor) is connected to

GPIO.setup(red_positive_pin, GPIO.OUT)  # this sets the GPIO pin to be an output 'type' i.e. it will apply about 3.3V
                                        # to the pin when it is set HIGH (True)

GPIO.setup(amber_positive_pin, GPIO.OUT)  # this sets the GPIO pin to be an output 'type' i.e. it will apply about 3.3V
                                          # to the pin when it is set HIGH (True)

GPIO.setup(green_positive_pin, GPIO.OUT)  # this sets the GPIO pin to be an output 'type' i.e. it will apply about 3.3V
                                          # to the pin when it is set HIGH (True

###########
# main code
###########

print (" ")
print ("program running - LEDs should be flashing: CTRL-C to stop ")
print (" ")


try:           # this loop is not strictly necessary but it does allow the script to be easily stopped with CTRL-C
    while True:  # this is the loop that continuously flashes the LED on and off every half second
        GPIO.output(red_positive_pin, True)     # red LED switched on by making the GPIO go HIGH
        GPIO.output(amber_positive_pin, False)  # amber LED switched off by making the GPIO go LOW
        GPIO.output(green_positive_pin, False)  # green LED switched off by making the GPIO go LOW
        time.sleep(0.5)                         # delay 0.5 seconds 
        GPIO.output(red_positive_pin, False)    # LED switched off by making the GPIO pin go LOW
        GPIO.output(amber_positive_pin, True)   # LED switched on by making the GPIO pin go HIGH
        GPIO.output(green_positive_pin, False)  # LED switched on by making the GPIO pin go LOW
        time.sleep(0.5)                         # delay 0.5 seconds before looping back
        GPIO.output(red_positive_pin, False)    # LED switched off by making the GPIO pin go LOW
        GPIO.output(amber_positive_pin, False)  # LED switched on by making the GPIO pin go LOW
        GPIO.output(green_positive_pin, True)   # LED switched on by making the GPIO pin go HIGH
        time.sleep(0.5) 


finally:  # this code is run when the try is interrupted with a CTRL-C
    print(" ")
    print("Cleaning up the GPIO pins before stopping")
    print(" ")
    print(" ")
    print(" ")
    GPIO.cleanup()
    
# The cleanup command sets all the pins back to inputs which protects the
# Pi from accidental shorts-circuits if something metal touches the GPIO pins.
    