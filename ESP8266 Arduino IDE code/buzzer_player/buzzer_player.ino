/*
  starter maker PCB Arduino IDE/ESP8266 version of buzzer_player.py that plays tunes
   the tune data is loaded into SPIFFS and then read by the program
*/

//  code developed and compiled using the Arduino IDE v1.8.13 on a Windows 10 PC
//  NodeMCU 1.0 (ESP-12E Module) set as the Board in the IDE - using board "ESP8266 Community version 3.0.0"
//  Flash Size: 4MB (FS:2MB OTA:~1019kB)
//   additional Board settings available! but none experimented with


#include <FS.h>

String notes[110] = {};  // initialise the notes string array
int num_notes;
String str_notes;

String twinkle_melody[42] = {}; // initialise the twinkle_melody string array
String twinkle_tempo[42] = {};  // initialise the twinkle_tempo string array
int num_twinkle = 42;

String adventure_melody[44] = {}; // initialise the adventure_melody string array
String adventure_tempo[44] = {};  // initialise the adventure_tempo string array
int num_adventure = 44;

int green_pin = 12; 

//  this is the GPIO pin that the +'ve pin of the buzzer is connected to
int  buzzpin = 13;

//  this is the GPIO pin that one side of the tactile button is connected to
int  button_pin = 14;

int dispmsg = 0;   // flag to show if the 'press button' message has been displayed

void setup() {
  Serial.begin(115200);
  delay(1500); // short delay to set up the monitor

  pinMode(buzzpin, OUTPUT);
  pinMode(green_pin, OUTPUT);
  pinMode(button_pin, INPUT_PULLUP); 

  digitalWrite(green_pin, HIGH); // LED switched on by making the GPIO go HIGH
  delay(2000);                   // delay 2 seconds with it switched on
  digitalWrite(green_pin, LOW);  // LED switched off by making the GPIO pin go LOW
  // short visual indicator above that the program is running
  Serial.println("");
  Serial.println("program running - press the button to play some tunes");
  Serial.println("");



  // ********************************
  // start the SPI Flash File System
  // ********************************
  if (!SPIFFS.begin())
  {
    // Serious problem
    Serial.println("SPIFFS mount failed");
  } else {
    Serial.println("SPIFFS mounted OK");
  }

  // ************************************
  // List all the files in SPIFFS
  // ************************************
  String filestr = "";
  Dir dir = SPIFFS.openDir("/");
  while (dir.next()) {
    filestr += dir.fileName();
    filestr += " / ";
    filestr += dir.fileSize();
    filestr += "\r\n";
  }
  Serial.println("SPIFFS file listing start:");
  Serial.print(filestr);
  Serial.println("SPIFFS file listing end:");
  Serial.println("  ");

  // *****************************************
  // List all the SPIFFS system info (FSinfo)
  // *****************************************

  FSInfo fs_info;
  SPIFFS.info(fs_info);
  printf("SPIFFS: %lu of %lu bytes used.\n",
    fs_info.usedBytes, fs_info.totalBytes);
  printf("SPIFFS blockSize: %lu \n",
    fs_info.blockSize);
  printf("SPIFFS pageSize: %lu \n",
    fs_info.pageSize);
  printf("SPIFFS maxOpenFiles: %lu \n",
    fs_info.maxOpenFiles);
  printf("SPIFFS maxPathLength: %lu \n",
    fs_info.maxPathLength);

  // test SPIFFS with reference/test file
  //File file = SPIFFS.open("/test.txt", "r");
  //if(!file){
  //  Serial.println("Failed to open file for reading");
  //  return;
  //}
  //Serial.println("Test/reference file content:");
  //while(file.available()){
  //Serial.write(file.read());
  //}
  //file.close();

  // **************************************************************
  // read all the default setting data from the SPIFFS text files   
  // **************************************************************
  str_notes = read_text("/numnotes.txt");


  // ********************************************************************
  // convert the integer and float strings back into integers and floats
  // ********************************************************************
  num_notes = str_notes.toInt();

  // read notes from file
  File notesfile = SPIFFS.open("/notes.txt", "r");
  if(!notesfile){
    Serial.println("Failed to open notesfile for reading");
    return;
  }
  read_strings("/notes.txt", notes, num_notes);
  Serial.println("-------------------------------");
  Serial.println("reprint read notes");
  for (int i=0; i<=num_notes-1; i++){
    Serial.print(i);
    Serial.print(" - ");
    Serial.print(notes[i].length());
    Serial.print(" - ");
    Serial.print(notes[i]);
    Serial.print(" - ");
    Serial.print(notes[i].substring(0,3)); // 1st # is inclusive - 2nd # is exclusive
    Serial.print(":");
    Serial.println(notes[i].substring(5)); // omitting the 2nd # shows to the end of the string
  }

  // load song melodies and tempos from SPIFFS
  read_strings("/twinkle_twinkle_melody.txt", twinkle_melody, num_twinkle);
  read_strings("/twinkle_twinkle_tempo.txt", twinkle_tempo, num_twinkle);

  read_strings("/adventure_time_melody.txt", adventure_melody, num_adventure);
  read_strings("/adventure_time_tempo.txt", adventure_tempo, num_adventure);

  Serial.println ("Song melodies and tempos loaded from SPIFFS");
}

void loop() {

  if (dispmsg == 0) {
    Serial.println("");
    Serial.println("press the button to play some tunes");
    Serial.println("");
    dispmsg = 1;  // set the flag so that the 'press button' message is not repeatedly shown
  }

  // check if the button GPIO goes LOW
  if ( digitalRead(button_pin) == LOW) {

    Serial.println ("  ");
    Serial.println ("********************************************");
    Serial.println ("Playing Twinkle, Twinkle, Little Star Melody");
    Serial.println ("********************************************");
    //play(notes, num_twinkle, num_notes, twinkle_melody, twinkle_tempo, 0.50, 1.500);
    play(notes, num_twinkle, num_notes, twinkle_melody, twinkle_tempo, 0.50, 1.000);

    Serial.println ("  ");
    Serial.println ("********************************************");
    Serial.println ("Playing Adventure Time Melody");
    Serial.println ("********************************************");
    //play(notes, num_adventure, num_notes, adventure_melody, adventure_tempo, 1.3, 1.500);
    play(notes, num_adventure, num_notes, adventure_melody, adventure_tempo, 1.3, 1.500);

    dispmsg = 0;  // reset the flag so that the 'press button' message is reshown

  }

}


// ********** Functions *******************

// **********************************************************
// Function to read a single string from a written text file
// **********************************************************
String read_text(String rfile) {
    int i;
    String str_read;
    //open the file for reading
    File f = SPIFFS.open(rfile, "r");
  
    if (!f) {
        str_read = "file open failed";
        Serial.println(str_read);
    }
    else
    {
        Serial.print("Reading Text Data from File: ");
        //read string from file
        str_read = f.readStringUntil('\n');
        if (rfile.substring(1,5) == "pass") {
            Serial.println("password not shown");
        } else {
            Serial.println(str_read);
        }
        f.close();  //Close file
        Serial.println("File Closed");
    }
    return str_read;

}


// *****************************************************************************************
// Function to read an existing multiple string file and extract the strings from it
// the local variables: 'rfile' is passed the file name, 'strarray' the string array
//  'pointed' to by reference and int num is the number of string array elements to be read
// *****************************************************************************************
void read_strings(String rfile, String strarray[], int num) {
    String tempstr;
    //r=Read Open file for reading
    File SPIfileStr = SPIFFS.open(rfile, "r");
  
    if (!SPIfileStr) {
        Serial.println("multiple string file open failed");
        strarray[0] = "multiple string file open failed";

    }
    else
    {
        //Read string data from file looking for the LF's that separate each string
        Serial.println("  ");
        Serial.println("Function read_strings: reading 'num' strings from file");
        for (int i=0; i<=num-1; i++){                     // loop thru the 'num' strings in the file
            tempstr=SPIfileStr.readStringUntil('\n'); // [i] string read upto the \n terminator
                               //  the terminator is discarded from the stream but adds a space
            // hmm looks like ESP32 SPIFFS doesn't need the last character removed so comment out for now
            //if (tempstr.length() > 2) {
            //    tempstr.remove(tempstr.length()-1,1);
            //}
            strarray[i] = tempstr;
            // debug only display of each read item
            //Serial.print(i);
            //Serial.print(": ");
            //Serial.println(strarray[i]);
        }
        SPIfileStr.close();  //Close file
        Serial.print("Function read_strings: string reading complete for file: ");
        Serial.println(rfile);

    }
}


// *************************************************************************
// Function to 'sound' the passive buzzer with a specific frequency/duration
// *************************************************************************
int buzz(int frequency, int duration) {   
    // create the function "buzz" and feed it the note (e.g. DS6=1245Hz) and duration (length in ms))
    int buzzstat;
    //Serial.print("Buzzing: pin ");
    //Serial.println(buzzpin);
    //Serial.print("Buzzing: frequency ");   // pitch/frequency of the note
    //Serial.println(frequency);
    //Serial.print("Buzzing: length (ms) "); // length/duration of the note in ms
    //Serial.println(duration);
    if (frequency == 0) {
        delay(duration);
        buzzstat = 0;   // status that is returned to the calling function (not used at present)
        return buzzstat;
    }
    // from the frequency calculate the time between buzzer pin HIGH-LOW setting in microseconds
    //   in physics, the period (sec/cyc) is the inverse of the frequency (cyc/sec)
    unsigned long timenow;  // variable used later to 'time' the delay using the micros() function instead of delayMicroseconds
    unsigned long delta;    // variable used later to 'time' the delay using the micros() function instead of delayMicroseconds
    unsigned long delayValue = (1000*1000/frequency)/2;  // calculate the time in microseconds for half of the wave
    int numCycles = int((duration * frequency)/1000);    // the number of waves to produce is the duration times the frequency
    //Serial.print("Number of cycles: ");
    //Serial.println(numCycles);
    //Serial.print("Hi-Low delay (microsecs): ");
    //Serial.println(delayValue);
    for (int icyc=0; icyc<=numCycles-1; icyc++) {  // start a loop from 0 to the variable "cycles" calculated above
        digitalWrite(buzzpin, HIGH);      // set buzzer pin to high
        // the process used below to use micros() to get the elapsed time since program start and 
        //  to then wait using a 'while loop' since using delayMicroseconds on the ESP8266 had problems
        timenow = micros();  // this is the number of microseconds since program start at this point
        delta = micros()-timenow;  // calculate an immediate amount of delay that has occured
        //Serial.print("cycle: ");
        //Serial.print(icyc);
        //Serial.print(" - ");
        //Serial.println(numCycles);
        // now wait for delayValue microseconds
        while (delta < delayValue)  { 
          delta = micros()-timenow;   // recalculate the delay that has occured
          //Serial.println(delta);
        }
        digitalWrite(buzzpin, LOW);       // set buzzer pin to low
        timenow = micros();  // this is the number of microseconds since program start at this point
        delta = micros()-timenow;  // calculate an immediate amount of delay that has occured
        // now wait for delayValue microseconds
        while (delta < delayValue)  { 
          delta = micros()-timenow;   // recalculate the delay that has occured
        }       
    }
    buzzstat = 1;  // status that  is returned to the calling function (not used at present)
    return buzzstat;
}

// **********************
// simple beep function
// **********************
void beep(int beeptime) {
    int buzzstatus;
    // beeptime in seconds
    Serial.print("beeping buzzer at 900Hz for ");
    Serial.print(beeptime);
    Serial.println(" seconds");
    for (int j=0; j<=beeptime-1; j++) {
        // total duration of all the steps below to add up to 1 second
        buzzstatus = buzz(900, 300);
        delay(200);
        buzzstatus = buzz(900, 300);
        delay(200);
    }
}


// ***********************************************************
// Function to 'play' a defined melody at its associated tempo
// ***********************************************************
void play(String allnotes[], int songnotes, int numnotes, String strmelody[], String strtempo[], float pause, float pace) { 
    // allnotes[]  - array of all the standard notes and their frequency
    // songnotes   - number of notes in the song
    // numnotes    - number of possible standard notes
    // strmelody[] - array of notes in the song
    // strtempo[]  - array of note lengths i.e. 1, 2, 4, 8 etc., where 8=quaver 4=semiquaver etc.
    // pause       - multiplier of the note duration as a pause between notes
    // pace        - used to calculate the note duration = pace/tempo
    float selfreq;
    Serial.print("Playing ");
    Serial.print(songnotes);
    Serial.println(" song notes");
    for (int i=0; i<=songnotes-1; i++) {        // Play strmelody[] song notes
      // loop thru all the possible notes to look for the associated frequency for the note to be played
      Serial.print("Playing song note: ");
      Serial.println(strmelody[i]);
      for (int j=0; j<=numnotes-1; j++) {
        String selectnote;
        if (strmelody[i].length() == 2) {
            selectnote = allnotes[j].substring(0,2);
        } else if (strmelody[i].length() == 3) {
            selectnote = allnotes[j].substring(0,3);
        } else {
            Serial.print(" funny number of characters in melody note"); 
        }
        //Serial.print("Is it this note: ");
        //Serial.println(selectnote);
        if (strmelody[i] == selectnote or strmelody[i] == "0") {
          // if here playnote found or freq = 0 - so use its frequency and play the note
          String tempo = strtempo[i];
          int noteDuration = 1000*pace/tempo.toInt();  // length or duration of the note in milliseconds
          if ( strmelody[i] == "0" ) {
            selfreq = 0.0;
            Serial.println("frequency set to zero");
          } else {
            String selfreqstr = allnotes[j].substring(5);
            Serial.print("associated frequency found: ");
            Serial.println(selfreqstr);
            selfreq = selfreqstr.toFloat();
            Serial.print("Playing frequency: ");
            Serial.println(selfreqstr);
          }
          int buzzstat = buzz(selfreq, noteDuration);      // Change the frequency along the song note  
          float pauseBetweenNotes = noteDuration * pause;
          Serial.print("pause betwen notes (ms): ");
          Serial.println(pauseBetweenNotes);
          delay(pauseBetweenNotes);          
          // now break out of the 'note finding' j for loop
          break;
        }
      }

      // now continue to loop through all the song notes
    }
}
