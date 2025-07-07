/*
  starter maker PCB Arduino IDE/ESP8266 version of LED_flash.py that flashs a LED on/off
   
*/

//  code developed and compiled using the Arduino IDE v1.8.13 on a Windows 10 PC
//  NodeMCU 1.0 (ESP-12E Module) set as the Board in the IDE - using board "ESP8266 Community version 3.0.0"
//  Flash Size: 4MB (FS:2MB OTA:~1019kB)
//   additional Board settings available! but none experimented with

//  code developed and compiled using the Arduino IDE v1.8.13 on a Windows 10 PC
//  NodeMCU 1.0 (ESP-12E Module) set as the Board in the IDE - using board "ESP8266 Community version 3.0.0"
//  Flash Size: 4MB (FS:2MB OTA:~1019kB)
//   additional Board settings available! but none experimented with

//  code developed and compiled using the Arduino IDE v1.8.13
//  ESP8266 NodeMCU 1.0 (ESP-12E Module) board version 3.0.0

// this is the GPIO pin that the RED LED positive leg (via the resistor) is connected to
int positive_pin = 4; 

// the setup function runs once when you press reset or power the board
void setup() {

  Serial.begin(115200);
  delay(1000); // short pause for the serial connection to 'come up'
  Serial.println("");
  Serial.println("program running - Red LED should be flashing");
  Serial.println("");
  // initialize digital pin positive_pin (the LED on the Starter Maker PCB) as an output.
  pinMode(positive_pin, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  digitalWrite(positive_pin, HIGH); // LED switched on by making the GPIO go HIGH
  delay(500);                       // delay 0.5 seconds with it switched on
  digitalWrite(positive_pin, LOW);  // LED switched off by making the GPIO pin go LOW
  delay(500);                       // delay 0.5 seconds with it switched off before looping back
}
