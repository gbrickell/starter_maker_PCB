/*
  Blink
  Turns an LED on for one second, then off for one second, repeatedly.
*/

int LEDpin = 12; // GREEN

// the setup function runs once when you press reset or power the board
void setup() {

  Serial.begin(115200);
  delay(1000); // short pause for the serial connection to 'come up'
  Serial.println("");
  Serial.println("Pico blink test code");
  Serial.println("");
  // initialize digital pin LEDpin (the LED on the Starter Maker PCB) as an output.
  pinMode(LEDpin, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  digitalWrite(LEDpin, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);                  // wait for a second
  digitalWrite(LEDpin, LOW);    // turn the LED off by making the voltage LOW
  delay(1000);                  // wait for a second
}
