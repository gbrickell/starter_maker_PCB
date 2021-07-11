/*
  starter maker kit Arduino IDE/Pico version of LED_button_flash.py that lights 
    a single LED 'on' for 3 secs and then 'off' when a button is pressed
*/

// this is the GPIO pin that the RED LED positive leg (via the resistor) is connected to
int red_pin = 10; 
int green_pin = 12; 

//  this is the GPIO pin that one side of the tactile button is connected to
int  button_pin = 14;

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
