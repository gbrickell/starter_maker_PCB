/*
  starter maker kit Arduino IDE/Pico version of LED_flash.py that flashes a single LED on/off
*/

// this is the GPIO pin that the RED LED positive leg (via the resistor) is connected to
int positive_pin = 10; 

// the setup function runs once when you press reset or power the board
void setup() {

  Serial.begin(115200);
  delay(1000); // short pause for the serial connection to 'come up'
  Serial.println("");
  Serial.println("program running - Red LED should be flashing");
  Serial.println("");
  // initialize digital pin positive_pin (the LED on the Starter Maker Kit) as an output.
  pinMode(positive_pin, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  digitalWrite(positive_pin, HIGH); // LED switched on by making the GPIO go HIGH
  delay(500);                       // delay 0.5 seconds with it switched on
  digitalWrite(positive_pin, LOW);  // LED switched off by making the GPIO pin go LOW
  delay(500);                       // delay 0.5 seconds with it switched off before looping back
}
