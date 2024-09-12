#!/bin/sh

# this control script supports the image taking projects with Starter Maker Kit1 and any Raspberry Pi SBC
# - when run as shown in the kit's documentation it will download various PDFs, Scratch & Python programs plus other material
# output a message about 'activating' a virtual environment for using Python
echo "**********************************************"
echo " please note that you should have activated"
echo " a virtual environment so that Python modules"
echo "  are installed by this script correctly"
echo "**********************************************"

# ask for Raspberry Pi user name
echo "Hello - please input the Raspberry Pi user name where everything will be stored:"
read uservarname

# check the script file size is correct as a simple check that the download was OK: size to be updated whenever the script changes
scriptsize=$(stat --format=%s "/home/$uservarname/starter_kit1_imgPi.sh")
echo " downloaded script file size: " $scriptsize
if [ $scriptsize -gt 8100 ] && [ $scriptsize -lt 8300 ]
then

  echo " script size looks OK - executing all the commands"

# create the main kit and code directories
echo " Creating the main kit & code folders"
mkdir /home/$uservarname/starter_maker_kit1
mkdir /home/$uservarname/starter_maker_kit1/RPi_code

# download the documentation:
echo " Downloading the documentation"

# 1. download the readme01.txt file and store it in the designated folder on the Raspberry Pi
wget -O /home/$uservarname/starter_maker_kit1/starter_kit1_imgPi_readme.txt https://onlinedevices.org.uk/dl1431

# 2. download the "Getting Started" PDF and store it in the designated folder on the Raspberry Pi
wget -O /home/$uservarname/starter_maker_kit1/starter_maker_kit1_getting_started.pdf https://onlinedevices.org.uk/dl1432

# 3. download the "Starter Maker Kit Usage Documentation" PDF and store it in the designated folder on the Raspberry Pi
wget -O /home/$uservarname/starter_maker_kit1/starter_maker_kit1_usage _documentation.pdf https://onlinedevices.org.uk/dl1433

# install all the libraries needed

# image taking
# might need Flask although it is usually already installed
yes | pip3 install Flask  
yes | pip3 install future
yes | sudo apt-get install fswebcam
yes | sudo apt install python3-opencv
yes | sudo apt-get install libav-tools
yes | sudo apt-get install feh
yes | sudo apt-get install imagemagick
yes | pip3 install pyautogui

###############
# Image Taking 
###############

# create the Image Taking directories
echo " Creating the Image Taking folders"
mkdir /home/$uservarname/starter_maker_kit1/RPi_code/image_taking

# create the Image Taking web subfolders
echo " Creating the Image Taking web subfolders"
mkdir /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/image_taking_controller
mkdir /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/image_taking_controller/static
mkdir /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/image_taking_controller/static/css
mkdir /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/image_taking_controller/static/images
mkdir /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/image_taking_controller/templates
mkdir /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/button_video_folder
mkdir /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/button_video_led_folder
mkdir /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/button_video_timer_folder
mkdir /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/single_image_folder
mkdir /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/single_image_led_folder
mkdir /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/single_image_timer_folder
mkdir /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/stop_motion_test01
mkdir /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/stopmotion_video_folder
mkdir /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/timelapse_image_folder
mkdir /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/image_timelapse_video_folder
mkdir /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/image_video_clip_folder

# download the Image Taking software

echo " Downloading the Image Taking Flask web files"
wget -O /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/image_taking_controller/static/css/normalize_advanced.css https://onlinedevices.org.uk/dl1447
wget -O /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/image_taking_controller/static/css/skeleton_advanced.css https://onlinedevices.org.uk/dl1448
wget -O /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/image_taking_controller/static/images/favicon.png https://onlinedevices.org.uk/dl1449
wget -O /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/image_taking_controller/static/images/Starter_kit_PCB01_20210518_132528401_900w.jpg https://onlinedevices.org.uk/dl1450
wget -O /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/image_taking_controller/static/images/Starter_kit_PCB01_front_image.png https://onlinedevices.org.uk/dl1451
wget -O /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/image_taking_controller/templates/cam_options_setup.html https://onlinedevices.org.uk/dl1473
wget -O /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/image_taking_controller/templates/cam_setup_mode.html https://onlinedevices.org.uk/dl1474
wget -O /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/image_taking_controller/templates/header_insert.html https://onlinedevices.org.uk/dl1475
wget -O /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/image_taking_controller/templates/layout.html https://onlinedevices.org.uk/dl1476
wget -O /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/image_taking_controller/templates/select_mode.html https://onlinedevices.org.uk/dl1477
wget -O /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/image_taking_controller/templates/stream_video_mode.html https://onlinedevices.org.uk/dl1478

echo " Downloading the Image Taking Python files"
wget -O /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/image_taking_controller/image_camera_usb_opencv_annotate.py https://onlinedevices.org.uk/dl1470
wget -O /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/image_taking_controller/image_streaming_app_root_annotate.py https://onlinedevices.org.uk/dl1471
wget -O /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/image_taking_controller/image_streaming_app_user_annotate.py https://onlinedevices.org.uk/dl1472
wget -O /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/button_led_take_image.py https://onlinedevices.org.uk/dl1479
wget -O /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/button_led_take_video.py https://onlinedevices.org.uk/dl1480
wget -O /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/button_take_image.py https://onlinedevices.org.uk/dl1481
wget -O /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/button_take_video.py https://onlinedevices.org.uk/dl1482
wget -O /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/button_timer_take_image.py https://onlinedevices.org.uk/dl1483
wget -O /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/button_timer_take_video.py https://onlinedevices.org.uk/dl1484
wget -O /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/sort_number_symlink_files.py https://onlinedevices.org.uk/dl1485
wget -O /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/timelapse_cron_take_annotated_image.py https://onlinedevices.org.uk/dl1486
wget -O /home/$uservarname/starter_maker_kit1/RPi_code/image_taking/timelapse_cron_take_image.py https://onlinedevices.org.uk/dl1487


echo " All downloads are now complete."
echo " "
echo " Please read the downloaded maker_kit3_readme01.txt file to see the latest information regarding "
echo " this kit and advice on how you can dispose of it, if or when you are finished with it."
echo " "
echo " "

# now remove the script so that it can be run again if necessary
rm starter_kit1_imgPi.sh


else

  echo " script size doesn't seem right - suggest you try downloading it again"

fi



