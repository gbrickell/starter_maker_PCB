****************************************************************************************************
starter_maker_pcb_imgPi_readme.txt - version control details for the Starter Maker PCB: Image Taking
****************************************************************************************************

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

  ** documentation ** 
    starter_maker_pcb_imgPi_readme.txt - this document which is updated whenever a new version is released
    starter_maker_pcb_getting_started_v2.0.pdf - Starter Maker PCB getting started leaflet v2.0 September 2024
    starter_maker_pcb_usage_documentation_v2-1.pdf - Starter Maker PCB detailed usage documentation v2.1 September 2024


  ** Python and other software files **
  
  * Raspberry Pi single board computer (SBC) code:

  image taking
  ------------
  Python - button_led_take_image.py
         - button_led_take_video.py
		 - button_take_image.py
	     - button_take_video.py
		 - button_timer_take_image.py
		 - button_timer_take_video.py
		 - sort_number_symlink_files.py
		 - timelapse_cron_take_annotated_image.py
		 - timelapse_cron_take_image.py
  web code      - image_camera_usb_opencv_annotate.py
                - image_streaming_app_root_annotate.py
				- image_streaming_app_user_annotate.py
  web css       - normalize_advanced.css	
                - skeleton_advanced.css
  web images    - favicon.png
                - Starter_kit_PCB01_20210518_132528401_900w.jpg
			    - Starter_kit_PCB01_front_image.png
  web templates - cam_options_setup.html
                - cam_setup_mode.html
				- header_insert.html
				- layout.html
				- select_mode.html
				- stream_video_mode.html


copyright 2021-2024 Geoff Brickell
