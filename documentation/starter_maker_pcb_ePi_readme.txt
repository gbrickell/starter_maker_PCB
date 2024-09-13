*******************************************************************************************************
starter_maker_pcb_ePi_readme.txt - version control details for the Starter Maker PCB: Electronic Basics
*******************************************************************************************************

required components version 2.0 September 2024
----------------------------------------------
  required components for use with the v1.0 PCB are listed in the starter_maker_pcb_getting_started.pdf
  and starter_maker_pcb_usage _documentation.pdf documents
 
  
  please note:
  ------------
  all electronic and electrical components need to be carefully recycled 
  but we would much prefer for you to pass this equipemnt on to another 
  user if you have no further use for it. 

*******************************************************************	
software & documentation version 2.0  September 2024
-------------------------------------------------------------------
  description: updated version with content to support usage with Raspberry Pi SBCs using the Bookworm OS 
               plus Raspberry Pi Pico, ESP32 and ESP8266 microcontrollers

  ** documentation ** 
    starter_maker_pcb_ePi_readme.txt - this document which is updated whenever a new version is released
    starter_maker_pcb_getting_started_v2.0.pdf - Starter Maker PCB getting started leaflet v2.0 September 2024
    starter_maker_pcb_usage_documentation_v2-1.pdf - Starter Maker PCB detailed usage documentation v2.1 September 2024
	Starter_Maker_PCB_Pico_Csoftware_usage_v2-0.pdf - Starter Maker PCB Raspberry Pi Pico microcontroller C/C++ usage notes v2.0 September 2024
	Starter_Maker_PCB_Pico_MPsoftware_usage_v2-0.pdf - Starter Maker PCB Raspberry Pi Pico microcontroller MicroPython usage notes v2.0 September 2024
	Starter_Maker_PCB_ESP32_Csoftware_usage_v2-0.pdf - Starter Maker PCB ESP32 microcontroller C/C++ usage notes v2.0 September 2024
	Starter_Maker_PCB_ESP8266_Csoftware_usage_v2-0.pdf - Starter Maker PCB ESP8266 microcontroller C/C++ usage notes v2.0 September 2024


  ** Scratch, Python and other software files **
  
  * Raspberry Pi single board computer (SBC) code:
  ebasics
  -------
  Scratch 1.4 - LED_button_buzzer.sb
              - LED_button_flash.sb
			  - LED_flash.sb
			  - LED_red_green_flash.sb
  Scratch 2   - LED_button_buzzer.sb2
              - LED_button_flash.sb2
			  - LED_flash.sb2
			  - LED_red_green_flash.sb2 
  Scratch 3   - LED_button_buzzer.sb3
              - LED_button_flash.sb3
			  - LED_flash.sb3
			  - LED_red_green_flash.sb3 
  Python - LED_flash.py
	     - LED_red_green_flash.py
		 - LED_red_amber_green_flash.py
	     - LED_button_flash.py
	     - LED_button_buzzer.py
		 - buzzer_player.py
  web code      - LED1_flash_web_user.py
                - LED1_flash_web_root.py
  web css       - normalize_advanced.css	
                - skeleton_advanced.css
  web images    - favicon.png
                - Starter_kit_PCB01_20210518_132528401_900w.jpg
			    - Starter_kit_PCB01_front_image.png
  web templates - electronics_header_insert.html
                - electronics_layout.html
				- electronics_select_mode1.html
				- led1_setup_mode.html
				- run_led1.html
  
 
  * Raspberry Pi Pico microcontroller code:
  MicroPython - LED_flash.py
	          - LED_red_green_flash.py
			  - LED_red_amber_green_flash.py
	          - LED_button_flash.py
	          - LED_button_buzzer.py
		      - buzzer_player.py 
			  - onboard_LED_flash.py
  C/C++       - LED_flash.ino
	          - LED_red_green_flash.ino
			  - LED_red_amber_green_flash.ino
	          - LED_button_flash.ino
	          - LED_button_buzzer.ino

  * ESP32 microcontroller code:
  C/C++ - LED_flash.ino
	    - LED_red_green_flash.ino
	    - LED_red_amber_green_flash.ino
	    - LED_button_flash.ino
	    - LED_button_buzzer.ino
		- buzzer_player.ino
		- LED1_flash_web.ino

  * ESP8266 microcontroller code:
  C/C++ - LED_flash.ino
	    - LED_red_green_flash.ino
	    - LED_red_amber_green_flash.ino
	    - LED_button_flash.ino
	    - LED_button_buzzer.ino
		- buzzer_player.ino
		- LED1_flash_web.ino
		- LED1_flash_webcss
		- LED1_flash_webfixed


copyright 2021-2024 Geoff Brickell
