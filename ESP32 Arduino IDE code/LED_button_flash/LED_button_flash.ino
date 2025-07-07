/*
  starter maker PCB Arduino IDE/ESP32 version of LED_button_flash.py that lights 
    a single LED 'on' for 3 secs and then 'off' when a button is pressed
*/

//  code developed and compiled using the Arduino IDE v1.8.13 on a Windows 10 PC
//  ESP32 Dev Module set as the Board in the IDE - using board "Espressif Systsems version 1.0.6
//   even though the board is probably the NodeMCU-32S i.e. 38 pin ESP32
//  Flash Size: 4MB
//  Upload speed: 921600
//  Partition Scheme set to: Default 4MB with spiffs (1.2 MB App / 1.5MB SPIFFS)
//   lots of other Board settings! but none experimented with

// this is the GPIO pin that the RED LED positive leg (via the resistor) is connected to
int red_pin = 25; 
int green_pin = 27; 

//  this is the GPIO pin that one side of the tactile button is connected to
int  button_pin = 12;

// the setup function runs once when you press reset or power the board
void setup() {

  Serial.begin(115200);
  delay(2000); // short pause for the serial connection to 'come up'
  // initialize digital pins for the LED and button as an output & input pulled HIGH.
  pinMode(red_pin, OUTPUT);
  pinMode(green_pin, OUTPUT);
  pinMode(button_pin, INPUT_PULLUP);

  digitalWrite(green_pin, HIGH); // LED switched on by making the GPIO go HIGH
  delay(2000);                   // delay 2 seconds with it switched on
  digitalWrite(green_pin, LOW);  // LED switched off by making the GPIO pin go LOW
    
  Serial.println("");
  Serial.println("program running - press the button to light the Red LED");
  Serial.println("");

}

// the loop function runs over and over again forever
void loop() {

  // check if the button GPIO goes LOW
  if ( digitalRead(button_pin) == LOW) {
    Serial.println("");
    Serial.println("**** button pressed ****");
    Serial.println("** red LED turned on ***");
    digitalWrite(red_pin, HIGH); // LED switched on by making the GPIO go HIGH
    delay(3000);                      // delay 3 seconds with it switched on
    digitalWrite(red_pin, LOW);  // LED switched off by making the GPIO pin go LOW
    Serial.println("** red LED turned off **");
    Serial.println("");
  
  }


}
