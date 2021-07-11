# starter maker kit PCB version of LED_button_flash.py that lights a single LED 'on' for 3 secs and then 'off' when a button is pressed

# command to run this script:  python3 /home/pi/starter_maker_kit1/RPi_code/starter_ebasics/LED_button_flash.py

import RPi.GPIO as GPIO   # this imports the module to allow the GPIO pins to be easily utilised
import time               # this imports the module to allow various time functions to be used
GPIO.setwarnings(False)

# This code sets the RPi to use the BCM (Broadcom) pin numbers which is usually the default but is positively set here
GPIO.setmode(GPIO.BCM)

positive_pin = 21  # this is the GPIO pin that the RED LED positive leg (via the resistor) is connected to

button_pin = 26    # this is the GPIO pin that one side of the tactile button is connected to

GPIO.setup(positive_pin, GPIO.OUT)  # this sets the LED GPIO pin to be an output 'type' i.e. it will apply 
                                    # about 3.3V to the pin when it is set HIGH (True)

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
# this is a special setting that indicates when a pin changes from LOW to HIGH ie when the button is pressed

# this is a function to indicate when the button is pressed 
def btn_pressed():
    # if button is pressed GPIO.input will report FALSE
    if not GPIO.input(button_pin):
        return 1

###########
# main code
###########

print (" ")
print ("program running: press the button to light the LED or CTRL-C to stop ")
print (" ")

try:    # this loop is not strictly necessary but it does allow the script to be easily stopped with CTRL-C
    while True:  # this is the loop that checks if the button is pressed and switches the LED on if it is
        GPIO.output(positive_pin, False) # LED switched off by making the GPIO pin go LOW        
        while not btn_pressed():
            pass                         # if not pressed just loop endlessly

        print(" ")
        print("button pressed and LED switched on")
        print(" ")
        GPIO.output(positive_pin, True)  # LED switched on by making the GPIO go HIGH
        time.sleep(3)             # delay 3 seconds with it switched on and then repeat loop
        print ("press the button again to light the LED or CTRL-C to stop ")

finally:  # this code is run when the try is interrupted with a CTRL-C
    print(" ")
    print("Cleaning up the GPIO pins before stopping")
    print(" ")
    print(" ")
    print(" ")
    GPIO.cleanup()
    
# The cleanup command sets all the pins back to inputs which protects the
# Pi from accidental shorts-circuits if something metal touches the GPIO pins.
    