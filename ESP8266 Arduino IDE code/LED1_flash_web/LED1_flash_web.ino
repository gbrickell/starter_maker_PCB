/*
  starter maker PCB Arduino IDE/ESP8266 web interface to various electronic 'basics'
      that alternates on/off for two LEDs (red & green)
*/

//  code developed and compiled using the Arduino IDE v1.8.13 on a Windows 10 PC
//  NodeMCU 1.0 (ESP-12E Module) set as the Board in the IDE - using board "ESP8266 Community version 3.0.0"
//  Flash Size: 4MB (FS:2MB OTA:~1019kB)
//   additional Board settings available! but none experimented with
// 
// web variable usage
//  form name     handle suffix   python variable      URL link
//  ---------     -------------   ---------------      --------
//   ledontime     led_on          on_time             /ledontime
//   ledofftime    led_off         off_time            /ledofftime
//   cyclesled     led_cycle       led_cycles          /cyclesled
//    n/a          tune1, 2, 3       n/a               /playtunes

// the assigned IP address is displayed in the Serial Monitor and once noted should stay the same
// the IP address is generally used to access the browser interface but the use of mDNS
//   may allow the host name to be used??

#include <ESP8266WiFi.h>        // Include the Wi-Fi library
//#include <WiFiClient.h>
#include <ESP8266mDNS.h>        // Include the mDNS library
#include <ESP8266WebServer.h>
#include <FS.h>

#include "Arduino.h"
#include "FS.h"

// some WiFi variables set here to be global but the WiFi config is done in the
//  void loop so that it can be either SoftAP or connection to a local WiFi

// the default option is to use a local network WiFi i.e. 1 of 5 possibles set by the SPIFFS files
int wifi_mode = 2;  // 1: softAP web interface  2: local WiFi web interface

String version = "01";

// IP addresses for a **soft AP** operation option
int IPnum = 10;
IPAddress local_IP(10,0,5,IPnum);     // using a 10.x.x.x IP address space
IPAddress gateway(10,0,5,1);
IPAddress subnet(255,255,255,0);

// hostname as a char variable
const char* namehost = "ESPled01";

// softAP device ref
String softAPref = "ESP_soft01";

ESP8266WebServer server(80);   //instantiate the web server at port 80 (http port#)

// *******************************************
// set the various PCB component variables
// *******************************************
// these are the GPIO pins that the RED, AMBER and GREEN LED positive legs (via the resistor) are connected to
const int red_pin = 4; 
const int amber_pin = 5;
const int green_pin = 12; 

String on_time = "1000";   // default ms value for the RED LED on time
String off_time = "1000";  // default ms value for the RED LED off time
String led_cycles = "5";   // default value for the RED LED on/off cycles

//  this is the GPIO pin that one side of the tactile button is connected to
const int  button_pin = 14;

//  this is the GPIO pin that the +'ve pin of the buzzer is connected to
const int  buzzpin = 13;

// buzzer tunes parameters
String notes[110] = {};  // initialise the notes string array
int num_notes;
String str_notes;
String twinkle_melody[42] = {}; // initialise the twinkle_melody string array
String twinkle_tempo[42] = {};  // initialise the twinkle_tempo string array
int num_twinkle = 42;
String adventure_melody[44] = {}; // initialise the adventure_melody string array
String adventure_tempo[44] = {};  // initialise the adventure_tempo string array
int num_adventure = 44;

// network credentials to connect to local WiFi networks
//  these variables are simply initialised here since it is assumed that all the values have
//  already been 'written' to the appropriate SPIFFS files or will be populated via the web 
//  interface initially using the softAP option
// N.B. variables are all strings BUT these need to be converted to a char for use with the WiFi
String ssid_selected ="";
int NSSIDs = 5;   // number of local WiFi credentials that can be set up: the first one found is used
String ssid1 = " ";
String ssid2 = " ";
String ssid3 = " ";
String ssid4 = " ";
String ssid5 = " ";
String password1 = " ";
String password2 = " ";
String password3 = " ";
String password4 = " ";
String password5 = " ";

// variable to indicate whether either of the two WiFi options have been set up
// this is needed since the setup is different per switch option, so the set up
//   must be done within the "void loop()" and reset if the switch settings change
const char* WiFiup = "no";

String page_content = "";      // initialised global variable for web page content
String server_started = "no";  // logic flag so the server is not started until a WiFi connection has been set up

// ********************************************************
// String versions of the various integer variables
// - easier to deal with in SPIFFS and web pages! even 
//   though this creates overhead with various conversions
// ********************************************************
String str_NSSIDs = String(NSSIDs);

// *********************
// web page variables
// *********************
String header_content;
int web_state;

// *********************************************************************
// the setup function runs once when you press reset or power the board
// *********************************************************************

void setup() {

    Serial.begin(115200);
    delay(2000); // short pause for the serial connection to 'come up'

    Serial.println("program started ......."); 
    
    // initialize digital pins for the LED and button as an output & input pulled HIGH.
    pinMode(red_pin, OUTPUT);
    pinMode(amber_pin, OUTPUT);
    pinMode(green_pin, OUTPUT);
    pinMode(buzzpin, OUTPUT);
    pinMode(button_pin, INPUT_PULLUP);

    digitalWrite(red_pin, LOW);
    digitalWrite(amber_pin, LOW);
    digitalWrite(green_pin, LOW);
    Serial.println("all LEDs turned OFF ...."); 

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

    // *******************************************
    // read and prepare all the tune parameters
    // *******************************************
    str_notes = read_text("/numnotes.txt");
    num_notes = str_notes.toInt();

    // read notes from file
    File notesfile = SPIFFS.open("/notes.txt", "r");
    if(!notesfile){
        Serial.println("Failed to open notesfile for reading");
        return;
    }
    read_strings("/notes.txt", notes, num_notes);

    // load song melodies and tempos from SPIFFS
    read_strings("/twinkle_twinkle_melody.txt", twinkle_melody, num_twinkle);
    read_strings("/twinkle_twinkle_tempo.txt", twinkle_tempo, num_twinkle);
    read_strings("/adventure_time_melody.txt", adventure_melody, num_adventure);
    read_strings("/adventure_time_tempo.txt", adventure_tempo, num_adventure);
    Serial.println ("Song melodies and tempos loaded from SPIFFS");

    // **************************************************************
    // read all the default setting data from the SPIFFS text files
    //  further code versions could make this more robust !    
    // **************************************************************
    str_NSSIDs = read_text("/str_NSSIDs.txt");
    Serial.println("-------------------------------");
    ssid1 = read_text("/ssid1.txt");
    ssid2 = read_text("/ssid2.txt");
    ssid3 = read_text("/ssid3.txt");
    ssid4 = read_text("/ssid4.txt");
    ssid5 = read_text("/ssid5.txt");
    Serial.println("-------------------------------");
    password1 = read_text("/password1.txt");
    password2 = read_text("/password2.txt");
    password3 = read_text("/password3.txt");
    password4 = read_text("/password4.txt");
    password5 = read_text("/password5.txt");
    Serial.println("-------------------------------");

    // ************************************************************************
    // interrupt 'handlers' triggered by various Web server requests:
    //  each specific URL that is detected by the web server invokes a 
    //  designated function that does something and then refreshes the web page
    // ************************************************************************
    // ** do this if web root i.e. / is requested
    server.on("/", handle_root);

    // ****** main selection actions ******
    // ** do this if /led_control is requested
    server.on("/led_control", handle_led_control);
    // ** do this if /led_setup is requested
    server.on("/led_setup", handle_led_setup);
    // ** do this if /WiFi_params is requested
    server.on("/WiFi_params", handle_WiFi_params);
    // ** do this if /sysinfo is requested
    server.on("/sysinfo", handle_sysinfo);
    // ** do this if /playtunes is requested
    server.on("/playtunes", handle_playtunes);

    // ****** detailed tune playing actions ******
    // ** do this if /tune1 is requested
    server.on("/tune1", handle_tune1);
    // ** do this if /tune2 is requested
    server.on("/tune2", handle_tune2);
    // ** do this if /tune3 is requested
    server.on("/tune3", handle_tune3);

    // ****** detailed LED set up update submission actions ******
    // ** do this if /setup_leds is requested
    server.on("/setup_leds", handle_setup_leds);

    // ****** detailed LED control actions ******
    // ** do this if /led_on is requested
    server.on("/led_on", handle_led_on);
    // ** do this if /led_off is requested
    server.on("/led_off", handle_led_off);
    // ** do this if /led_cycle is requested
    server.on("/led_cycle", handle_led_cycle);

    // ****** detailed WiFi parameter update submission actions ******
    // ** do this if /WiFi_updates1 is requested
    server.on("/WiFi_updates1", handle_WiFi_updates1);
    // ** do this if /WiFi_updates2 is requested
    server.on("/WiFi_updates2", handle_WiFi_updates2);
    // ** do this if /WiFi_updates3 is requested
    server.on("/WiFi_updates3", handle_WiFi_updates3);
    // ** do this if /WiFi_updates4 is requested
    server.on("/WiFi_updates4", handle_WiFi_updates4);
    // ** do this if /WiFi_updates5 is requested
    server.on("/WiFi_updates5", handle_WiFi_updates5);

    Serial.println();
    Serial.println("all interrupt handlers set up");

    // web server not started here as its needs the WiFi to be 'up'
    //  and this is only done when wifi_mode = 2 
 
    // ** do a one-time population of the common header HTML used in all web pages
    header_content = HTMLheader();

    // amber LED switched ON/OFF & short beep to signify completion of the initial set up
    for (int io=0; io<=10; io++) { 
        digitalWrite(amber_pin, HIGH); // Amber LED switched on by making the GPIO go HIGH
        delay(200);
        digitalWrite(amber_pin, LOW);  // Amber LED switched off by making the GPIO go LOW
        delay(200);
    }
    beep(2);

}


// ***************************************************
// the loop function runs over and over again forever
// ***************************************************
void loop() {
    // ##############################################################
    // ##    wifi_mode=1: run web server with the softAP option    ##
    // ##############################################################
    if (wifi_mode == 1) {
        if (WiFiup == "no") {
            setupSoftAP();
        }
        server.handleClient();  // look for an HTTP request from a browser
    }
    // ##############################################################
    // ##    wifi_mode=1: run web server with the softAP option    ##
    // ##############################################################
    else if (wifi_mode == 2) {
        if (WiFiup == "no") {
            setuplocalWiFi();
        }
        server.handleClient();  // look for an HTTP request from a browser
    }
// ** end of main loop **
}


// *****************************************************************
// ***  this section is for all the browser response 'handlers'  ***
// *****************************************************************

void handle_root() {
    // ** do this if web root i.e. / is requested
    Serial.println("web root - electronic basics main web page");
    server.send(200, "text/html", HTMLmain()); 
}

// **********************************
// *** main selection 'handlers' ****
// **********************************
void handle_led_control() {
    // ** do this if /led_control is requested
    web_state = 1;
    Serial.println("selecting LED control");
    server.send(200, "text/html", HTMLled_control()); 
}
void handle_led_setup() {
    // ** do this if /led_setup is requested
    web_state = 1;
    Serial.println("selecting LED setup");
    server.send(200, "text/html", HTMLled_setup()); 
}
void handle_WiFi_params() {
    // ** do this if /WiFi_params is requested
    web_state = 51;
    Serial.println("selecting WiFi updates");
    server.send(200, "text/html", HTMLWiFi_params()); 
}
void handle_sysinfo() {
    // ** do this if /sysinfo is requested
    web_state = 6;
    Serial.println("selecting system information display");
    server.send(200, "text/html", HTMLsysinfo()); 
}
void handle_playtunes() {
    // ** do this if /playtunes is requested
    web_state = 6;
    Serial.println("selecting tune playing");
    server.send(200, "text/html", HTMLtunes()); 
}


// ***************************************************
// ******     detailed tune playing actions     ******
// ***************************************************
void handle_tune1() {
    // ** do this if /tune1 is requested
    playtune(1);
    server.send(200, "text/html", HTMLtunes());
}
void handle_tune2() {
    // ** do this if /tune2 is requested
    playtune(2);
    server.send(200, "text/html", HTMLtunes());
}
void handle_tune3() {
    // ** do this if /tune3 is requested
    playtune(3);
    server.send(200, "text/html", HTMLtunes());
}


// ***************************************************
// ******     detailed LED control actions      ******
// ***************************************************
void handle_led_on() {
    // ** do this if /led_on is requested
    digitalWrite(red_pin, HIGH); // Red LED switched on by making the GPIO go HIGH
    server.send(200, "text/html", HTMLled_control());
}
void handle_led_off() {
    // ** do this if /led_off is requested
    digitalWrite(red_pin, LOW); // Red LED switched off by making the GPIO go LOW
    server.send(200, "text/html", HTMLled_control());
}
void handle_led_cycle() {
    // ** do this if /led_cycle is requested
    Serial.print("on time ms: ");
    Serial.println(on_time.toInt());
    Serial.print("off time ms: ");
    Serial.println(off_time.toInt()); 
    Serial.print("number of cycles: ");
    Serial.println(led_cycles.toInt());   
    for (int i=0; i<=led_cycles.toInt()-1; i++) { 
        digitalWrite(red_pin, HIGH); // Red LED switched on by making the GPIO go HIGH
        delay(on_time.toInt());
        digitalWrite(red_pin, LOW);  // Red LED switched off by making the GPIO go LOW
        delay(off_time.toInt());
    }
    server.send(200, "text/html", HTMLled_control());
}


// ***************************************************
// ****** detailed LED setup submission actions ******
// ***************************************************
void handle_setup_leds() {
    // ** do this if /setup_leds is requested
    on_time = server.arg("ledontime");      // get string from 'name' in the browser response
    off_time = server.arg("ledofftime");    // get string from 'name' in the browser response
    led_cycles = server.arg("cyclesled");   // get string from 'name' in the browser response

    server.send(200, "text/html", HTMLled_setup());
}


// ****** detailed WiFi parameter update submission actions ******
// *** WiFi update input 'handlers' ***
// -----------------------------------
void handle_WiFi_updates1() {
    // ** do this if /WiFi_updates1 is requested
    web_state = 51;
    Serial.println("WiFi SSID1 settings update");
    ssid1 = server.arg("ssid_1");          // get string from browser response
    password1 = server.arg("password_1");  // get string from browser response
    // resave the WiFi SSID and its password
    write_text("/ssid1.txt", ssid1);
    write_text("/password1.txt", password1);
    server.send(200, "text/html", HTMLWiFi_params());
}

void handle_WiFi_updates2() {
    // ** do this if /WiFi_updates2 is requested
    web_state = 51;
    Serial.println("WiFi SSID2 settings update");
    ssid2 = server.arg("ssid_2");          // get string from browser response
    password2 = server.arg("password_2");  // get string from browser response
    // resave the WiFi SSID and its password
    write_text("/ssid2.txt", ssid2);
    write_text("/password2.txt", password2);
    server.send(200, "text/html", HTMLWiFi_params());
}

void handle_WiFi_updates3() {
    // ** do this if /WiFi_updates3 is requested
    web_state = 51;
    Serial.println("WiFi SSID3 settings update");
    ssid3 = server.arg("ssid_3");          // get string from browser response
    password3 = server.arg("password_3");  // get string from browser response
    // resave the WiFi SSID and its password
    write_text("/ssid3.txt", ssid3);
    write_text("/password3.txt", password3);
    server.send(200, "text/html", HTMLWiFi_params());
}

void handle_WiFi_updates4() {
    // ** do this if /WiFi_updates4 is requested
    web_state = 51;
    Serial.println("WiFi SSID4 settings update");
    ssid4 = server.arg("ssid_4");          // get string from browser response
    password4 = server.arg("password_4");  // get string from browser response
    // resave the WiFi SSID and its password
    write_text("/ssid4.txt", ssid4);
    write_text("/password4.txt", password4);
    server.send(200, "text/html", HTMLWiFi_params());
}

void handle_WiFi_updates5() {
    // ** do this if /WiFi_updates5 is requested
    web_state = 51;
    Serial.println("WiFi SSID5 settings update");
    ssid5 = server.arg("ssid_5");          // get string from browser response
    password5 = server.arg("password_5");  // get string from browser response
    // resave the WiFi SSID and its password
    write_text("/ssid5.txt", ssid5);
    write_text("/password5.txt", password5);
    server.send(200, "text/html", HTMLWiFi_params());
}


// *****************************************************************
// **********     end of 'handlers' set up       *******************
// *****************************************************************



// ******************************************************
// ****          set up 'soft AP' WiFi               ****
// ******************************************************
void setupSoftAP()
{
    Serial.print("Setting soft-AP IP configuration ... ");
    Serial.println(WiFi.softAPConfig(local_IP, gateway, subnet) ? "Ready" : "Failed!");

    Serial.print("Setting soft-AP ssid and password ... ");
    String softAP_str = "ESPsoftAP" + softAPref;
    Serial.println(WiFi.softAP(softAP_str.c_str(), "pswd12345") ? "Ready" : "Failed!");

    Serial.print("Soft-AP IP address = ");
    Serial.println(WiFi.softAPIP());     // IP address shouldn't change so could be used in a browser

    Serial.printf("Soft-AP MAC address = %s\n", WiFi.softAPmacAddress().c_str());

    if (!MDNS.begin(namehost)) {        // Start the mDNS responder for namehost ....local
        Serial.println("Error setting up MDNS responder!");
    }
    Serial.print("mDNS responder started for domain: ");
    Serial.print(namehost);
    Serial.println(".local");    
    delay(2000);
    WiFiup = "yes";

    if (server_started == "no" ) {
        Serial.println();
        Serial.println("starting web server .........");
        // ** start web server
        server.begin();
        Serial.println("Web server started!");
        server_started = "yes";
    }


}


// ********************************************
// **** set up WiFi with host name as well ****
// ********************************************
void setuplocalWiFi()
{
    Serial.print("trying to connect to WiFi with hostname: ");

    Serial.println(namehost);
    //WiFi.hostname(namehost);

    // scan to find all the 'live' broadcast SSID's ....
    int n = WiFi.scanNetworks();
    Serial.print("Number of WiFi networks found: ");
    Serial.println(n);
    ssid_selected ="";

    Serial.print("trying to connect to: ");
    Serial.println(ssid1);
    // try to use ssid1 first
    for (int i = 0; i < n; ++i) {
        Serial.print("Trying SSID: ");
        Serial.println(WiFi.SSID(i));
        if (WiFi.SSID(i)== ssid1 ) {
            ssid_selected = ssid1;
            break;
        }
    }
    if (ssid_selected != "" ) {
        // make connection to selected WiFi
        connectWiFi();
        return;
    }

    // --------------------------------------------
    // now try ssid2 if ssid1 not already selected
    Serial.print("trying to connect to: ");
    Serial.println(ssid2);
    for (int i = 0; i < n; ++i) {
        Serial.print("Trying SSID: ");
        Serial.println(WiFi.SSID(i));
        if (WiFi.SSID(i)== ssid2 ) {
            ssid_selected = ssid2;
            break;
        }       
    }
    if (ssid_selected != "" ) {
        // make connection to selected WiFi
        connectWiFi();
        return;
    }

    // --------------------------------------------
    // now try ssid3 
    Serial.print("trying to connect to: ");
    Serial.println(ssid3);
    for (int i = 0; i < n; ++i) {
        Serial.print("Trying SSID: ");
        Serial.println(WiFi.SSID(i));
        if (WiFi.SSID(i)== ssid3 ) {
            ssid_selected = ssid3;
            break;
        }       
    }
    if (ssid_selected != "" ) {
        // make connection to selected WiFi
        connectWiFi();
        return;
    }

    // --------------------------------------------
    // now try ssid4
    Serial.print("trying to connect to: ");
    Serial.println(ssid4);
    for (int i = 0; i < n; ++i) {
        Serial.print("Trying SSID: ");
        Serial.println(WiFi.SSID(i));
        if (WiFi.SSID(i)== ssid4 ) {
            ssid_selected = ssid4;
            break;
        }       
    }
    if (ssid_selected != "" ) {
        // make connection to selected WiFi
        connectWiFi();
        return;
    }

    // --------------------------------------------
    // now try ssid5
    Serial.print("trying to connect to: ");
    Serial.println(ssid5);
    for (int i = 0; i < n; ++i) {
        Serial.print("Trying SSID: ");
        Serial.println(WiFi.SSID(i));
        if (WiFi.SSID(i)== ssid5 ) {
            ssid_selected = ssid5;
            break;
        }       
    }
    if (ssid_selected != "" ) {
        // make connection to selected WiFi
        connectWiFi();
        return;
    }

    // if here then no allowed local WiFi found 
    Serial.println(" No allowed WiFi found");


}

// ******************************
// **** make WiFi connection ****
// ******************************
void connectWiFi()
{

    Serial.print(ssid_selected);
    Serial.println(" selected - now trying to connect");
	
	  if (ssid_selected == ssid1 ) {
            // convert the selected ssid and password to the char variables
            WiFi.begin(ssid1.c_str(), password1.c_str());    //initiate connection to ssid1
            Serial.print("SSID: ");
            Serial.println(ssid1);

    } else if (ssid_selected == ssid2 ) {
           // convert the selected ssid and password to the char variables
            WiFi.begin(ssid2.c_str(), password2.c_str());    //initiate connection to ssid2
            Serial.print("SSID: ");
            Serial.println(ssid2);

    } else if (ssid_selected == ssid3 ) {
            // convert the selected ssid and password to the char variables
            WiFi.begin(ssid3.c_str(), password3.c_str());    //initiate connection to ssid3
            Serial.print("SSID: ");
            Serial.println(ssid3);

    } else if (ssid_selected == ssid4 ) {
            // convert the selected ssid and password to the char variables
            WiFi.begin(ssid4.c_str(), password4.c_str());    //initiate connection to ssid4
            Serial.print("SSID: ");
            Serial.println(ssid4);

    } else if (ssid_selected == ssid5 ) {
            // convert the selected ssid and password to the char variables
            WiFi.begin(ssid5.c_str(), password5.c_str());    //initiate connection to ssid5
            Serial.print("SSID: ");
            Serial.println(ssid5);

    }
    Serial.println("");
    // Wait for connection
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    // Connected to the first available/defined WiFi Access Point
    Serial.println("");
    Serial.print("Connected to ");
    Serial.println(ssid_selected);
    Serial.print("IP address: ");
    delay(500);
    Serial.println(WiFi.localIP());
    Serial.print("MAC address: ");
    delay(500);
    Serial.println(WiFi.macAddress());
    delay(1000);
    
    if (!MDNS.begin(namehost)) {        // Start the mDNS responder for namehost ....local
        Serial.println("Error setting up MDNS responder!");
    }
    Serial.print("mDNS responder started for domain: ");
    Serial.print(namehost);
    Serial.println(".local");    
    delay(2000);
    
    WiFi.setHostname(namehost);
    delay(1500);
    Serial.print("updated hostname: ");
    Serial.println(WiFi.getHostname());

    WiFiup = "yes";

    if (server_started == "no" ) {
        Serial.println();
        Serial.println("starting web server .........");
        // ** start web server
        server.begin();
        Serial.println("Web server started!");
        server_started = "yes";
    }

}


// **********************************************************************
// Function to create/open an existing file and write a single string to 
//  it - the file name and text are passed strings to the function 
// **********************************************************************
void write_text(String wfile, String wtext) {
    //w=Write Open file for writing
    File SPIfile = SPIFFS.open(wfile, "w");
  
    if (!SPIfile) {
        Serial.println("file open failed");
    }
    else
    {
        //Write data to file
        Serial.print("Writing Data to File: ");
        Serial.println(wtext);
        SPIfile.print(wtext);
        SPIfile.close();  //Close file

    }
}


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
        Serial.print("Reading Text Data from File ");
        Serial.print(rfile);
        //read string from file
        str_read = f.readStringUntil('\n');
        if (rfile.substring(1,5) == "pass") {
            Serial.println("password not shown");
        } else {
            Serial.print(": ");
            Serial.println(str_read);
        }
        f.close();  //Close file
        Serial.println("File Closed");
    }
    return str_read;

}


// ************************************************************************************
// Function to create/open an existing multiple string file and write data to it
// the local variables: 'wfile' is passed the file name, 'strarray' the string array
//  to be written to the file and int num is the number of array elements to be written
// ************************************************************************************
void write_strings(String wfile, String strarray[], int num) {
    //w=Write: open file for writing from the beginning overwriting whatever is already there
    File SPIfileStr = SPIFFS.open(wfile, "w");
  
    if (!SPIfileStr) {
        Serial.println("file open failed");
    }
    else
    {
        //Write string array data to file
        Serial.println("  ");
        Serial.println("Writing String array data to the file");
        for (int i=0; i<=num-1; i++){
            SPIfileStr.println(strarray[i]);    // writes an individual string with a LF at the end
        }
        SPIfileStr.close();  //Close file
        Serial.println("String array writing complete ");
    }
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
            //if (tempstr.length() > 2) {
            //    tempstr.remove(tempstr.length()-1,1);
            //}
            strarray[i] = tempstr;
            //Serial.print(i);
            //Serial.print(": ");
            //Serial.println(strarray[i]);
        }
        SPIfileStr.close();  //Close file
        Serial.println("Function read_strings: string reading complete ");

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

// **********************************************************************************
// Function to play a specific tune/sound depending upon the passed reference number
// **********************************************************************************
void playtune(int tune) {
    // use the tune number to select what is played
    if (tune == 1) {
        Serial.println("beeping buzzer at 900Hz for 5 seconds");
        for (int j=0; j<=4; j++) {
            buzz(900, 500);
            delay(500);
        }
     } else if (tune == 2) {
        Serial.println("playing twinkle twinkle little star");
        play(notes, num_twinkle, num_notes, twinkle_melody, twinkle_tempo, 0.50, 1.000);
     } else if (tune == 3) {
        Serial.println("playing adventure time");
        play(notes, num_adventure, num_notes, adventure_melody, adventure_tempo, 1.3, 1.500);
     } else {
        Serial.println("tune number not valid");
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
      //esp_task_wdt_reset();  // reset the watchdog timer just in case
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
            //Serial.print("associated frequency found: ");
            //Serial.println(selfreqstr);
            selfreq = selfreqstr.toFloat();
            //Serial.print("Playing frequency: ");
            //Serial.println(selfreqstr);
          }
          int buzzstat = buzz(selfreq, noteDuration);      // Change the frequency along the song note  
          float pauseBetweenNotes = noteDuration * pause;
          //Serial.print("pause betwen notes (ms): ");
          //Serial.println(pauseBetweenNotes);
          delay(pauseBetweenNotes);          
          // now break out of the 'note finding' j for loop
          break;
        }
      }

      // now continue to loop through all the song notes
    }
}


// ****************************************************************
// ******  create the various web pages that are being used  ******
// ****     this longer/internal method is preferred to        ****
// ****     using separate HTML files stored in SPIFFS so      ****
// ****     that additional logic can be embedded              ****
// ****************************************************************

// --------------------------------------------------------------------------------
// create the header area used in all the web pages - done once in the setup stage
// --------------------------------------------------------------------------------
String HTMLheader() {
    String h_content = "<!DOCTYPE html> <html>\n";
    h_content +="<head><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0, user-scalable=yes\">\n";
    h_content +="<title>Electronic Basics</title>\n";
	
    // style content in the page header ( but could be replaced by a css file eventually )
    h_content +="<style>\n";
    h_content +="html{font-family: Verdana; display: inline-block; margin: 0px auto; text-align: center; font-size: 15px;}\n";
    h_content +="body{margin-top: 50px;} h1 {color: #444444; margin: 10px auto 10px; font-size: 32px;}\n"; 
    h_content +="h3{color: #444444; margin: 10px auto 10px; font-size: 24px;}\n";
    h_content +="h4{color: #444444; margin: 10px auto 10px; font-size: 18px;}\n";
    h_content +=".button {display: block; width: 100px; background-color: #1abc9c; border: none; \n"; 
    h_content +="color: white; padding: 10px 10px 10px 10px; text-decoration: none; font-size: 28px; \n";
    h_content +="margin: 5px auto 5px; cursor: pointer; border-radius: 4px;}\n";
    h_content +=".btninline {display: inline-block; }\n";
    h_content +=".button-on {background-color: #1abc9c;}\n";
    h_content +=".button-on:active {background-color: #16a085;}\n";
    h_content +=".button-off {background-color: #34495e;}\n";
    h_content +=".button-off:active {background-color: #2c3e50;}\n";
    h_content +=".button-red {background-color: #f51031;}\n";
    h_content +=".button-red:active {background-color: #d20e2a;}\n";
    h_content +="p {font-size: 18px;color: #888; margin: 5px;}\n";
    h_content +="</style>\n";
    h_content +="</head>\n";
    return h_content;
}

// -----------------------------------------
// create the main selection web page
// -----------------------------------------
String HTMLmain(){
    String page_content = header_content;
    // start of main selection web page content
    page_content +="<body>\n";
    page_content +="<h1>ESP8266 Server</h1>\n";
    page_content +="<h1>Electronic Basics</h1>\n";
    page_content +="<h3>main selections</h1>\n";
    page_content +="<p><a class=\"button btninline button-off\" href=\"led_control\"><button>LED control</button></a>&nbsp; &nbsp; &nbsp;";
    page_content +="<a class=\"button btninline button-off\" href=\"led_setup\"><button>LED set up</button></a></p>\n";
    page_content +="<p><a class=\"button btninline button-off\" href=\"WiFi_params\"><button>Update WiFi parameters</button></a>&nbsp; &nbsp; &nbsp;";
    page_content +="<a class=\"button btninline button-off\" href=\"sysinfo\"><button>System information</button></a></p>\n";
    page_content +="<p><a class=\"button btninline button-off\" href=\"playtunes\"><button>Play tunes</button></a></p>\n";

    page_content +="<p>&nbsp;</p>\n";
    page_content +="<p>&nbsp;</p>\n";

    page_content +="</body>\n";
    page_content +="</html>\n";
    return page_content;

}

// -----------------------------------------
// create the tune playing web page
// -----------------------------------------
String HTMLtunes(){
    String page_content = header_content;
    // start of main selection web page content
    page_content +="<body>\n";
    page_content +="<h1>ESP8266 Server</h1>\n";
    page_content +="<h1>Electronic Basics</h1>\n";
    page_content +="<h3>Play tunes</h1>\n";
    page_content +="<p><a class=\"button btninline button-off\" href=\"tune1\"><button>Beep buzzer at 900Hz for 5 seconds</button></a></p>\n";
    page_content +="<p><a class=\"button btninline button-off\" href=\"tune2\"><button>Play Twinkle Twinkle Little Star</button></a></p>\n";
    page_content +="<p><a class=\"button btninline button-off\" href=\"tune3\"><button>Play Adventure Time</button></a></p>\n";

    page_content +="<p>&nbsp;</p>\n";

    page_content +="<p><a class=\"button button-off\" href=\"/\"><button>back to main selection</button></a></p>\n";
    page_content +="<p>&nbsp;</p>\n";

    page_content +="</body>\n";
    page_content +="</html>\n";
    return page_content;

}

// -----------------------------------------
// create the LED control web page
// -----------------------------------------
String HTMLled_control(){
    String page_content = header_content;
    // start of main selection web page content
    page_content +="<body>\n";
    page_content +="<h1>ESP8266 Server</h1>\n";
    page_content +="<h1>Electronic Basics</h1>\n";
    page_content +="<h3>ESP8266 LED control</h1>\n";
    page_content +="<p><a class=\"button btninline button-off\" href=\"led_on\"><button>switch the RED LED on</button></a></p>\n";
    page_content +="<a class=\"button btninline button-off\" href=\"led_off\"><button>switch the RED LED off</button></a></p>\n";
    page_content +="<p><a class=\"button btninline button-off\" href=\"led_cycle\"><button>cycle the RED LED on/off n time</button></a></p>\n";

    page_content +="<p>&nbsp;</p>\n";

    page_content +="<p><a class=\"button button-off\" href=\"/\"><button>back to main selection</button></a></p>\n";
    page_content +="<p>&nbsp;</p>\n";

    page_content +="</body>\n";
    page_content +="</html>\n";
    return page_content;

}

// ---------------------------------------------
// create the LED set up web page
// ---------------------------------------------
String HTMLled_setup(){
    String page_content = header_content;
    // start of main selection web page content
    page_content +="<body>\n";
    page_content +="<h1>ESP8266 Server</h1>\n";
    page_content +="<h1>Electronic Basics</h1>\n";
    page_content +="<h3>ESP8266 LED use set up</h3>\n";

    // input sections of the web page
    page_content +="<form method=\"post\" action=\"/setup_leds\"> \n";

    page_content +="LED on cycle time (ms): \n";
    page_content +="<input type=\"text\" name=\"ledontime\" size=\"7\" value= ";
    page_content +=on_time;
    page_content +=" > \n";
    page_content +="<p>&nbsp;</p>\n";

    page_content +="LED off cycle time (ms): \n";
    page_content +="<input type=\"text\" name=\"ledofftime\" size=\"7\" value= ";
    page_content +=off_time;
    page_content +=" > \n";
    page_content +="<p>&nbsp;</p>\n";

    page_content +="LED number of cycles &nbsp;: \n";
    page_content +="<input type=\"text\" name=\"cyclesled\" size=\"7\" value= ";
    page_content +=led_cycles;
    page_content +=" > \n";
    page_content +="<p>&nbsp;</p>\n";

    page_content +="<input type=\"submit\" value=\"Submit\">\n";
    page_content +="<p>&nbsp;</p>\n";

    page_content +="</form>\n";

    page_content +="<p>&nbsp;</p>\n";

    page_content +="<p><a class=\"button button-off\" href=\"/\"><button>back to main selection</button></a></p>\n";
    page_content +="<p>&nbsp;</p>\n";

    page_content +="</body>\n";
    page_content +="</html>\n";
    return page_content;

}


// ---------------------------------------------
// create the WiFi parameter update web page
// ---------------------------------------------
String HTMLWiFi_params(){
    String page_content = header_content;
    // start of main selection web page content
    page_content +="<body>\n";
    page_content +="<h1>ESP8266 Server</h1>\n";
    page_content +="<h1>Electronic Basics</h1>\n";
    page_content +="<h3>WiFi parameter update</h3>\n";
    page_content +="<h3>input/update SSID name and WEP key</h3>\n";

    // input sections of the web page

    page_content +="<form method=\"post\" action=\"/WiFi_updates1\"> \n";
    page_content +="SSID1: \n";
    page_content +="<input type=\"text\" name=\"ssid_1\" size=\"12\" value= ";
    page_content +=ssid1;
    page_content += "> &nbsp; &nbsp; <input type=\"text\" name=\"password_1\"  ";
    page_content += " size=\"12\" placeholder=\"********\" > ";
    page_content +=" &nbsp; &nbsp; <input type=\"submit\" value=\"Submit\">\n";
    page_content +="</form>\n";

    page_content +="<p>&nbsp;</p>\n";

    page_content +="<form method=\"post\" action=\"/WiFi_updates2\"> \n";
    page_content +="SSID2: \n";
    page_content +="<input type=\"text\" name=\"ssid_2\" size=\"12\" value= ";
    page_content +=ssid2;
    page_content += "> &nbsp; &nbsp; <input type=\"text\" name=\"password_2\"  ";
    page_content += " size=\"12\" placeholder=\"********\" > ";
    page_content +=" &nbsp; &nbsp; <input type=\"submit\" value=\"Submit\">\n";
    page_content +="</form>\n";

    page_content +="<p>&nbsp;</p>\n";

    page_content +="<form method=\"post\" action=\"/WiFi_updates3\"> \n";
    page_content +="SSID3: \n";
    page_content +="<input type=\"text\" name=\"ssid_3\" size=\"12\" value= ";
    page_content +=ssid3;
    page_content += "> &nbsp; &nbsp; <input type=\"text\" name=\"password_3\"  ";
    page_content += " size=\"12\" placeholder=\"********\" > ";
    page_content +=" &nbsp; &nbsp; <input type=\"submit\" value=\"Submit\">\n";
    page_content +="</form>\n";

    page_content +="<p>&nbsp;</p>\n";

    page_content +="<form method=\"post\" action=\"/WiFi_updates4\"> \n";
    page_content +="SSID4: \n";
    page_content +="<input type=\"text\" name=\"ssid_4\" size=\"12\" value= ";
    page_content +=ssid4;
    page_content += "> &nbsp; &nbsp; <input type=\"text\" name=\"password_4\"  ";
    page_content += " size=\"12\" placeholder=\"********\" > ";
    page_content +=" &nbsp; &nbsp; <input type=\"submit\" value=\"Submit\">\n";
    page_content +="</form>\n";

    page_content +="<p>&nbsp;</p>\n";

    page_content +="<form method=\"post\" action=\"/WiFi_updates5\"> \n";
    page_content +="SSID5: \n";
    page_content +="<input type=\"text\" name=\"ssid_5\" size=\"12\" value= ";
    page_content +=ssid5;
    page_content += "> &nbsp; &nbsp; <input type=\"text\" name=\"password_5\"  ";
    page_content += " size=\"12\" placeholder=\"********\" > ";
    page_content +=" &nbsp; &nbsp; <input type=\"submit\" value=\"Submit\">\n";
    page_content +="</form>\n";

    page_content +="<p>&nbsp;</p>\n";

    page_content +="<p><a class=\"button button-off\" href=\"/\"><button>back to main selection</button></a></p>\n";
    page_content +="<p>&nbsp;</p>\n";

    page_content +="</body>\n";
    page_content +="</html>\n";
    return page_content;
}




// ---------------------------------------------
// create the system information display web page
// ---------------------------------------------
String HTMLsysinfo(){
    String page_content = header_content;
    FSInfo fs_info;
    SPIFFS.info(fs_info);

    // start of main selection web page content
    page_content +="<body>\n";
    page_content +="<h1>";
    if(wifi_mode == 2) {
        page_content += namehost;
    } else {
        page_content += "10.0.5.";
        page_content += IPnum;
    }
    page_content +="</h1>\n";
    page_content +="<h1>ESP8266 Robot Web Server</h1>\n";
    page_content +="<h3>System Information</h3>\n";

    // **** networking information ****
    page_content +="<div style=\" font-size: 18px; margin-bottom: 5px;\"><b>Networking:</b></div>\n";
    page_content +="<table border=\"1\" style=\"width: 450px; text-align: left;\" align=\"center\" cellpadding=\"3\" cellspacing=\"0\">\n";
    page_content +="<tr><td style=\"width: 225px; \">connected to WiFi SSID:</td><td>" ;
    if(wifi_mode == 2) {
        page_content +=ssid_selected;
    } else {
        page_content +="ESPsoftAP";
    }
    page_content +="</td></tr>\n";
    page_content +="<tr><td>host name:</td><td>" ;
    if(wifi_mode == 2) {
        page_content +=WiFi.hostname();
    } else {
        page_content +="esp8266";
    }
    page_content +="</td></tr>\n";
    page_content +="<tr><td>assigned IP address:</td><td>" ;
    if(wifi_mode == 2) {
        page_content +=WiFi.localIP().toString();
    } else {
        page_content +=WiFi.softAPIP().toString();
    }
    page_content +="</td></tr>\n";
    page_content +="<tr><td>WiFi MAC address:</td><td>" ;
    if(wifi_mode == 2) {
        page_content +=WiFi.macAddress().c_str();
    } else {
        page_content +=WiFi.softAPmacAddress().c_str();
    }
    page_content +="</td></tr>\n";
    page_content +="</table>\n";

    page_content +="<p>&nbsp;</p>\n";

    // **** file system (SPIFFS) ****
    page_content +="<div style=\" font-size: 18px; margin-bottom: 5px;\"><b>File System (SPI Flash File System):</b></div>\n";
    page_content +="<table border=\"1\" style=\"width: 450px; text-align: left;\" align=\"center\" cellpadding=\"3\" cellspacing=\"0\">\n";
    page_content +="<tr><td style=\"width: 225px; \">Total KB:</td><td>" ;
    page_content +=String((float)fs_info.totalBytes / 1024.0);
    page_content +="</td></tr>\n";
    page_content +="<tr><td style=\"width: 225px; \">Used KB:</td><td>" ;
    page_content +=String((float)fs_info.usedBytes / 1024.0);
    page_content +="</td></tr>\n";
    page_content +="</table>\n";

    page_content +="<p>&nbsp;</p>\n";

    // **** memory information ****
    page_content +="<div style=\" font-size: 18px; margin-bottom: 5px;\"><b>Memory information:</b></div>\n";
    page_content +="<table border=\"1\" style=\"width: 450px; text-align: left;\" align=\"center\" cellpadding=\"3\" cellspacing=\"0\">\n";

    page_content +="<tr><td style=\"width: 225px; \">free heap measure(1):</td><td>" ;
    page_content +=system_get_free_heap_size();
    page_content +="</td></tr>\n";

    page_content +="<tr><td style=\"width: 225px; \">free heap measure(2):</td><td>" ;
    page_content +=String(ESP.getFreeHeap());
    page_content +="</td></tr>\n";

    page_content +="<tr><td style=\"width: 225px; \">% heap fragmentation:</td><td>" ;
    page_content +=String(ESP.getHeapFragmentation());
    page_content +="</td></tr>\n";

    page_content +="<tr><td style=\"width: 225px; \">max allocatable ram block size:</td><td>" ;
    page_content +=String(ESP.getMaxFreeBlockSize());
    page_content +="</td></tr>\n";

    page_content +="<tr><td style=\"width: 225px; \">Sketch thinks Flash RAM (MB) is:</td><td>" ;
    page_content +=String((float)ESP.getFlashChipSize() / 1024.0 / 1024.0);
    page_content +="</td></tr>\n";

    page_content +="<tr><td style=\"width: 225px; \">Actual Flash RAM (MB):</td><td>" ;
    page_content +=String((float)ESP.getFlashChipRealSize() / 1024.0 / 1024.0);
    page_content +="</td></tr>\n";

    page_content +="</table>\n";

    page_content +="<p>&nbsp;</p>\n";

    // **** firmware information ****
    page_content +="<div style=\" font-size: 18px; margin-bottom: 5px;\"><b>Firmware:</b></div>\n";
    page_content +="<table border=\"1\" style=\"width: 450px; text-align: left;\" align=\"center\" cellpadding=\"3\" cellspacing=\"0\">\n";
    page_content +="<tr><td style=\"width: 225px; \">chip Id::</td><td>" ;
    page_content +=String(ESP.getChipId());
    page_content +="</td></tr>\n";
    page_content +="<tr><td>core version::</td><td>" ;
    page_content +=ESP.getCoreVersion();
    page_content +="</td></tr>\n";
    page_content +="<tr><td>SDK version::</td><td>" ;
    page_content +=String(ESP.getSdkVersion());
    page_content +="</td></tr>\n";
    page_content +="</table>\n";

    page_content +="<p>&nbsp;</p>\n";

    page_content +="<p><a class=\"button button-off\" href=\"/\"><button>back to main selection</button></a></p>\n";
    page_content +="</body>\n";
    page_content +="</html>\n";
    return page_content;
}
