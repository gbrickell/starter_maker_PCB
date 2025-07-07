# starter maker PCB version of LED_button_buzzer.py that lights a RED LED 
#   and sounds a passive buzzer for 'duration' (3) secs when a button is pressed

# command to run this script:  python3 ./starter_maker_PCB1/RPi_code/starter_ebasics/LED_button_buzzer.py

import RPi.GPIO as GPIO   # this imports the module to allow the GPIO pins to be easily utilised
import time               # this imports the module to allow various time functions to be used
GPIO.setwarnings(False)

duration = 3.0           # total time in seconds that LED is on and buzzer sounded
freq = 1000.0            # this is the frequency (cycles/second ie HZ) that the buzzer is switched on/off to make a sound
period = 1.0 / freq             # this is the time period in seconds of a full cycle
half_cycle_time = period / 2.0  # this is the time period for half a cylcle ie the on and off times

# This code sets the RPi to use the BCM (Broadcom) pin numbers which is usually the default but is positively set here
GPIO.setmode(GPIO.BCM)

LED_plus_pin = 21  # this is the GPIO pin that the RED LED positive leg (via the resistor) is connected to

buzzer_pin = 19    # this is the GPIO pin that the positive pin of the buzzer s connected to

button_pin = 26    # this is the GPIO pin that one side of the tactile button is connected to

GPIO.setup(LED_plus_pin, GPIO.OUT)  # this sets the LED GPIO pin to be an output 'type' i.e. it will apply 
                                    # about 3.3V to the pin when it is set HIGH (True)

GPIO.setup(buzzer_pin, GPIO.OUT)    # this sets the buzzer GPIO pin to be an output 'type' i.e. it will apply 
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
print ("program running: press button to light the LED or CTRL-C to stop ")
print (" ")

try:    # this loop is not strictly necessary but it does allow the script to be easily stopped with CTRL-C
    while True:  # this is the loop that checks if the button is pressed and switches the LED on if it is
        GPIO.output(LED_plus_pin, False) # LED switched off by making the GPIO pin go LOW        
        GPIO.output(buzzer_pin, False)   # buzzer switched off by making the GPIO pin go LOW
        while not btn_pressed():
            pass                         # if not pressed just loop endlessly

        print(" ")
        print("button pressed and LED + buzzer switched on")
        print(" ")
        # if we are here then the button has been pressed
        t1 = time.time()                 # start the clock by recording the current time
        GPIO.output(LED_plus_pin, True)  # LED switched on by making the GPIO go HIGH

        # energise the buzzer on/off for the duration time
        while time.time() - t1 < duration:   
            GPIO.output(buzzer_pin, True)
            time.sleep(half_cycle_time)
            GPIO.output(buzzer_pin, False)
            time.sleep(half_cycle_time)
        GPIO.output(LED_plus_pin, False) # LED switched off by making the GPIO pin go LOW
        # now loop back to wait for the button to be pressed again
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
    