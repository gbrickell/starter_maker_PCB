/*
  starter maker PCB Arduino IDE/ESP32 version of LED_button_buzzer.py that lights 
    a single LED on/off and buzzs for 3 secs  wh en a button is pressed
*/

//  code developed and compiled using the Arduino IDE v1.8.13 on a Windows 10 PC
//  ESP32 Dev Module set as the Board in the IDE - using board "Espressif Systsems version 1.0.6
//   even though the board is probably the NodeMCU-32S i.e. 38 pin ESP32
//  Flash Size: 4MB
//  Upload speed: 921600
//  Partition Scheme set to: Default 4MB with spiffs (1.2 MB App / 1.5MB SPIFFS)
//   lots of other Board settings! but none experimented with

// these are the GPIO pins that the RED and GREEN LED positive legs (via the resistor) are connected to
int red_pin = 25; 
int green_pin = 27; 

//  this is the GPIO pin that one side of the tactile button is connected to
int  button_pin = 12;

//  this is the GPIO pin that the +'ve pin of the buzzer is connected to
int  buzzpin = 14;

// the setup function runs once when you press reset or power the board
void setup() {

  Serial.begin(115200);
  delay(2000); // short pause for the serial connection to 'come up'
  // initialize digital pins for the LED and button as an output & input pulled HIGH.
  pinMode(red_pin, OUTPUT);
  pinMode(green_pin, OUTPUT);
  pinMode(buzzpin, OUTPUT);
  pinMode(button_pin, INPUT_PULLUP);

  digitalWrite(green_pin, HIGH); // LED switched on by making the GPIO go HIGH
  delay(2000);                   // delay 2 seconds with it switched on
  digitalWrite(green_pin, LOW);  // LED switched off by making the GPIO pin go LOW
    
  Serial.println("");
  Serial.println("program running - press the button to light the Red LED and buzz");
  Serial.println("");

}

// the loop function runs over and over again forever
void loop() {

  // check if the button GPIO goes LOW
  if ( digitalRead(button_pin) == LOW) {
    Serial.println("");
    Serial.println("******* button pressed ******");
    Serial.println("** red LED on and buzzing ***");
    digitalWrite(red_pin, HIGH); // LED switched on by making the GPIO go HIGH
    beep(3);                     // beep for 3 seconds with it switched on
    digitalWrite(red_pin, LOW);  // LED switched off by making the GPIO pin go LOW
    Serial.println("** red LED and buzzer off ***");
    Serial.println("");
  
  }


}


// *************************************************************************
// Function to 'sound' the passive buzzer with a specific frequency/duration
// *************************************************************************
int buzz(int frequency, int duration) {   
    // create the function "buzz" and feed it the note (e.g. DS6=1245Hz) and duration (length in ms))
    //Serial.print("Buzzing: pin ");
    //Serial.println(buzzpin);
    //Serial.print("Buzzing: frequency ");   // pitch/frequency of the note
    //Serial.println(frequency);
    //Serial.print("Buzzing: length (ms) "); // length/duration of the note in ms
    //Serial.println(duration);
    if (frequency == 0) {
        delay(duration);
        int buzzstat = 0;
        return buzzstat;
    }
    // from the frequency calculate the time between buzzer pin HIGH-LOW setting in microseconds
    //float period = 1.0 / frequency;       // in physics, the period (sec/cyc) is the inverse of the frequency (cyc/sec)
    int delayValue = (1000*1000/frequency)/2;  // calculate the time in microseconds for half of the wave
    int numCycles = int((duration * frequency)/1000);   // the number of waves to produce is the duration times the frequency
    //Serial.print("Number of cycles: ");
    //Serial.println(numCycles);
    //Serial.print("Hi-Low delay (microsecs): ");
    //Serial.println(delayValue);
    for (int i=0; i<=numCycles-1; i++) {  // start a loop from 0 to the variable "cycles" calculated above
        digitalWrite(buzzpin, HIGH);      // set buzzer pin to high
        delayMicroseconds(delayValue);    // wait with buzzer pin high
        digitalWrite(buzzpin, LOW);       // set buzzer pin to low
        delayMicroseconds(delayValue);    // wait with buzzer pin low
    }

}

// **********************
// simple beep function
// **********************
void beep(int beeptime) {
    // beeptime in seconds
    Serial.print("beeping buzzer at 900Hz for ");
    Serial.print(beeptime);
    Serial.println(" seconds");
    for (int j=0; j<=beeptime-1; j++) {
        // total duration of all the steps below to add up to 1 second
        buzz(900, 300);
        delay(200);
        buzz(900, 300);
        delay(200);
    }
}
