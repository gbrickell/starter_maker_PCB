#!/bin/sh

# this control script supports the electronic basics projects with Starter Maker PCB1 and any Raspberry Pi SBC
# - when run as shown in the PCB's documentation it will download various PDFs, Scratch & Python programs plus other material
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
scriptsize=$(stat --format=%s "/home/$uservarname/starter_PCB1_ePi.sh")
echo " downloaded script file size: " $scriptsize
if [ $scriptsize -gt 8200 ] && [ $scriptsize -lt 8400 ]
then

  echo " script size looks OK - executing all the commands"

# create the main PCB and code directories
echo " Creating the main PCB & code folders"
mkdir /home/$uservarname/starter_maker_PCB1
mkdir /home/$uservarname/starter_maker_PCB1/RPi_code

# download the documentation:
echo " Downloading the documentation"

# 1. download the readme01.txt file and store it in the designated folder on the Raspberry Pi
wget -O /home/$uservarname/starter_maker_PCB1/starter_maker_pcb_ePi_readme.txt https://onlinedevices.org.uk/dl1429

# 2. download the "Getting Started" PDF and store it in the designated folder on the Raspberry Pi
wget -O /home/$uservarname/starter_maker_PCB1/starter_maker_pcb_getting_started.pdf https://onlinedevices.org.uk/dl1432

# 3. download the "Starter Maker Kit Usage Documentation" PDF and store it in the designated folder on the Raspberry Pi
wget -O /home/$uservarname/starter_maker_PCB1/starter_maker_pcb_usage_documentation.pdf https://onlinedevices.org.uk/dl1433

# install all the libraries needed

# might need Flask although it is usually already installed
yes | pip3 install Flask
yes | pip3 install future

##############
# Electronics
##############

# create the Electronics directories
echo " Creating the Electronics folders"
mkdir /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics
# create the electronics Scratch code and web subfolders
echo " Creating the Scratch and web subfolders"
mkdir /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/scratch1.4
mkdir /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/scratch2
mkdir /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/scratch3
mkdir /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/starter_web_controller
mkdir /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/starter_web_controller/static
mkdir /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/starter_web_controller/static/css
mkdir /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/starter_web_controller/static/images
mkdir /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/starter_web_controller/templates

# download the Electronics software

echo " Downloading the Electronics Flask web files"
wget -O /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/starter_web_controller/static/css/normalize_advanced.css https://onlinedevices.org.uk/dl1447
wget -O /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/starter_web_controller/static/css/skeleton_advanced.css https://onlinedevices.org.uk/dl1448
wget -O /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/starter_web_controller/static/images/favicon.png https://onlinedevices.org.uk/dl1449
wget -O /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/starter_web_controller/static/images/Starter_kit_PCB01_20210518_132528401_900w.jpg https://onlinedevices.org.uk/dl1450
wget -O /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/starter_web_controller/static/images/Starter_kit_PCB01_front_image.png https://onlinedevices.org.uk/dl1451
wget -O /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/starter_web_controller/templates/electronics_header_insert.html https://onlinedevices.org.uk/dl1446
wget -O /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/starter_web_controller/templates/electronics_layout.html https://onlinedevices.org.uk/dl1445
wget -O /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/starter_web_controller/templates/electronics_select_mode1.html https://onlinedevices.org.uk/dl1444
wget -O /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/starter_web_controller/templates/led1_setup_mode.html https://onlinedevices.org.uk/dl1443
wget -O /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/starter_web_controller/templates/run_led1.html https://onlinedevices.org.uk/dl1442

echo " Downloading the Electronics Python code"
wget -O /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/starter_web_controller/LED1_flash_web_user.py https://onlinedevices.org.uk/dl1440
wget -O /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/starter_web_controller/LED1_flash_web_root.py https://onlinedevices.org.uk/dl1441
wget -O /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/buzzer_player.py https://onlinedevices.org.uk/dl1439
wget -O /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/LED_button_buzzer.py https://onlinedevices.org.uk/dl1438
wget -O /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/LED_button_flash.py https://onlinedevices.org.uk/dl1437
wget -O /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/LED_flash.py https://onlinedevices.org.uk/dl1436
wget -O /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/LED_red_amber_green_flash.py https://onlinedevices.org.uk/dl1435
wget -O /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/LED_red_green_flash.py https://onlinedevices.org.uk/dl1434

echo " Downloading the Scratch 1.4 code"
wget -O /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/scratch1.4/LED_button_buzzer.sb https://onlinedevices.org.uk/dl1452
wget -O /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/scratch1.4/LED_button_flash.sb https://onlinedevices.org.uk/dl1453
wget -O /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/scratch1.4/LED_flash.sb https://onlinedevices.org.uk/dl1454
wget -O /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/scratch1.4/LED_red_green_flash.sb https://onlinedevices.org.uk/dl1455

#echo " Downloading the Scratch 2 code"  # doesn't include button usage examples
#wget -O /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/scratch2/LED_button_buzzer.sb2 https://onlinedevices.org.uk/dl1456
#wget -O /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/scratch2/LED_button_flash.sb2 https://onlinedevices.org.uk/dl1457
#wget -O /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/scratch2/LED_flash.sb2 https://onlinedevices.org.uk/dl1462
#wget -O /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/scratch2/LED_red_green_flash.sb2 https://onlinedevices.org.uk/dl1459

echo " Downloading the Scratch 3 code"
wget -O /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/scratch3/LED_button_buzzer.sb3 https://onlinedevices.org.uk/dl1460
wget -O /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/scratch3/LED_button_flash.sb3 https://onlinedevices.org.uk/dl1461
wget -O /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/scratch3/LED_flash.sb3 https://onlinedevices.org.uk/dl1458
wget -O /home/$uservarname/starter_maker_PCB1/RPi_code/starter_ebasics/scratch3/LED_red_green_flash.sb3 https://onlinedevices.org.uk/dl1463

echo " All downloads are now complete."
echo " "
echo " Please read the downloaded starter_PCB1_ePi_readme.txt file to see the latest information regarding "
echo " this PCB plus its components and advice on how you can dispose of it, if or when you are finished with it."
echo " "
echo " "

# now remove the script so that it can be run again if necessary
rm starter_PCB1_ePi.sh


else

  echo " script size doesn't seem right - suggest you try downloading it again"

fi



