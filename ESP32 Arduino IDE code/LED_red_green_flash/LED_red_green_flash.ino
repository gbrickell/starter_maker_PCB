/*
  starter maker kit Arduino IDE/ESP32 version of LED_red_green_flash.py 
      that alternates on/off for two LEDs (red & green)
*/

//  code developed and compiled using the Arduino IDE v1.8.13 on a Windows 10 PC
//  ESP32 Dev Module set as the Board in the IDE - using board "Espressif Systsems version 1.0.6
//   even though the board is probably the NodeMCU-32S i.e. 38 pin ESP32
//  Flash Size: 4MB
//  Upload speed: 921600
//  Partition Scheme set to: Default 4MB with spiffs (1.2 MB App / 1.5MB SPIFFS)
//   lots of other Board settings! but none experimented with

// this is the GPIO pin that the RED LED positive leg (via the resistor) is connected to
int red_positive_pin = 25; 

// this is the GPIO pin that the GREEN LED positive leg (via the resistor) is connected to
int green_positive_pin = 27; 

// the setup function runs once when you press reset or power the board
void setup() {

  Serial.begin(115200);
  delay(1000); // short pause for the serial connection to 'come up'
  Serial.println("");
  Serial.println("program running - Red and Green LEDs should be flashing");
  Serial.println("");
  // initialize digital pins (the Red & Green LEDs on the Starter Maker Kit) as outputs.
  pinMode(red_positive_pin, OUTPUT);
  pinMode(green_positive_pin, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  digitalWrite(red_positive_pin, HIGH);   // LED switched on by making the GPIO go HIGH
  digitalWrite(green_positive_pin, LOW);  // LED switched off by making the GPIO go LOW
  delay(500);                             // delay 0.5 seconds with it switched on
  digitalWrite(red_positive_pin, LOW);    // LED switched off by making the GPIO pin go LOW
  digitalWrite(green_positive_pin, HIGH); // LED switched on by making the GPIO go HIGH
  delay(500);                             // delay 0.5 seconds with it switched off before looping back
}
