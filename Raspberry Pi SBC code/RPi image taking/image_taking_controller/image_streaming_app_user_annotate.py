#!/usr/bin/python

# Starter PCB image streaming Flash app
# Image taking USB camera Flask controller: python code as part of a Flask based web server system
#  - this version of the app is for use by any non-root user and uses the 8000 port
#    BUT it needs for a ram drive to have been previously set up by root
# 
#  - this version uses the USB camera class that annotates the image

# command to run: python3 ./starter_maker_PCB1/RPi_code/image_taking/image_taking_controller/image_streaming_app_user_annotate.py
# N.B.  browser URL should use port 8000 
#

# set defaults for some parameters
global setres
setres = "640x480"
global setresW
setresW = "640"
global setresH
setresH = "480"
global setrotate
setrotate = "None"
global setflip
setflip = "None"

global setres1
setres1 = "160x120"  # 160x120  default on
global setres2
setres2 = "None"  # 176x144
global setres3
setres3 = "320x240"  # 320x240  default on
global setres4
setres4 = "None"  # 352x288
global setres5
setres5 = "640x480"  # 640x480  default on
global setres6
setres6 = "None"  # 800x600
global setres7
setres7 = "None"  # 1280x720
global setres8
setres8 = "None"  # 1920x1080

# some more potential camera properties - although the camera may not be capable of setting them!
#    OR they might stop the camera from working!!!
#  use a value of 9999 to avoid them being set
global setbright
setbright = "9999"    # 9999 is the not to be used value - typical value is: 120
global setcontrast
setcontrast = "9999"    # 9999 is the not to be used value - typical value is: 50
global setsat
setsat = "9999"    # 9999 is the not to be used value - typical value is: 70
global sethue
sethue = "9999"    # 9999 is the not to be used value - typical value is: 13
global setgain
setgain = "9999"    # 9999 is the not to be used value - typical value is: 50
global setexp
setexp = "9999"    # 9999 is the not to be used value - typical value is: -3
global setwbal
setwbal = "9999"    # 9999 is the not to be used value - typical value is: 5000
global setfocus
setfocus = "9999"    # 9999 is the not to be used value - typical value is: 0 ??

#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# function to generate the video stream from the USB camera 
#
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
def gen(camera, imgwidth):       # added imgwidth as a passed parameter for image annotation logic
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame(imgwidth)   # added imgwidth as a passed parameter for possible image annotation logic
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# main code 
#
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

###  set up the ramdrive ###
# /etc/fstab should have been edited to set up a ram drive for the image streaming .jpg files
# it should be something like the text below so that both root and the user can read/write to the folder
# none    /mnt/ramimage    ramfs    noauto,user,size=2M,mode=0770    0    0
#   /mnt/ramimage is a mount point, where the ramfs filesystem will be mounted and this directory should already exist.
#   noauto option prevents this to be mounted automatically (e.g. at system's boot up)
#   user makes this mountable by individual regular users
#   size sets this "ramdisk's" size
#   mode is very important, with the octal code 0770 only root and the user who mounted this filesystem, will be able to 
#    read and write to the drive, not the others 
#   PLEASE NOTE only one user can use the ram drive at any one time!
import os
os.system('mount /mnt/ramimage')    # mount the ramdrive in the target folder that must already exist

import time          # import the time library 

# import the various Flask libraries that are needed
from flask import Flask, render_template
from flask import request
from flask import Response  # used as a custom Response for the video streamimg

# import the custom openCV USB camera class that uses the ram drive and annotates the image
from image_camera_usb_opencv_annotate import Camera   


make_image_app01 = Flask(__name__)  # creates a Flask object called make_image_app01

################################################################################
# this route goes to the selection mode routine when the URL root is selected
################################################################################
@make_image_app01.route("/") # run the code below this function when the URL root is accessed
def start():
    select_mode = "selection routine",
    # update time now
    timenow = time.strftime('%H:%M %Z')

    template_data = {
        'title' : "mode selection",         # this sets the browser title template parameter
        'time_now' : timenow,               # this sets the current time template parameter
    }

    return render_template('select_mode.html', **template_data)


##################################################################################
# this route provides the video image streaming at various camera resolutions
##################################################################################
@make_image_app01.route('/video_feed/<int:pixwidth>/<int:pixheight>/<int:pbr>/<int:pcon>/<int:psat>/<int:phue>/<int:pgain>/<int:pexp>/<int:pwbal>/<int:pfocus>/', methods=['GET'])   
def video_feed(pixwidth,pixheight,pbr,pcon,psat,phue,pgain,pexp,pwbal,pfocus):  # pixwidth and pixheight & the exotic settings! passed from template
    """Video image streaming route - this is put in the src attribute of an img tag in the template"""
    time.sleep(0.0001) # pause for 0.1ms - produces a bit of lag - but give the Pi processor some time to do something else
    # now use the USB camera class installed as 'Camera' to get a single frame image from the camera
    #  - added the extra pixwidth passed parameter to support the image annotation logic for text positioning
    return Response(gen(Camera(pixwidth,pixheight,pbr,pcon,psat,phue,pgain,pexp,pwbal,pfocus), pixwidth), mimetype='multipart/x-mixed-replace; boundary=frame')


##########################################################################################
# this route defines the actions selected when the USB camera is in the selection mode
##########################################################################################
@make_image_app01.route("/<choice_mode>")  # run the code below this function when URL /<choice_mode> is accessed from select_mode.html where choice_mode is a variable
def mode_selection(choice_mode=None):
    global setres
    global setresW
    global setresH
    global setrotate
    global setflip

    global setres1
    global setres2
    global setres3 
    global setres4
    global setres5
    global setres6
    global setres7
    global setres8 
 
    global setbright
    global setcontrast
    global setsat
    global sethue
    global setgain
    global setexp
    global setwbal
    global setfocus

    none_selected = "no mode selected"
    
    if choice_mode == 'streamvid':   # run this section of code if 'streamvid' is selected at the template

        # update time now
        timenow = time.strftime('%H:%M %Z')

        # template data: individual parameters that are passed for use in the template to render the browser display
        template_data = {
            'title' : "streaming video",        # this sets the browser title template parameter
            'time_now' : timenow,               # this sets the current time template parameter
            'set_res' : setres,                 # this sets the camera resolution template parameter
            'set_resW' : setresW,               # this sets the camera resolution width parameter
            'set_resH' : setresH,               # this sets the camera resolution height parameter
            'set_rotate' : setrotate,           # this sets the display rotation template parameter
            'set_flip' : setflip,               # this sets the display flipping template parameter
            'set_bright' : setbright,     # the rest of these parameters are not yet used: future version possibility
            'set_contrast' : setcontrast,
            'set_sat' : setsat,
            'set_hue' : sethue,
            'set_gain' : setgain,
            'set_exp' : setexp,
            'set_wbal' : setwbal,
            'set_focus' : setfocus,

        }

        # echo the values of the key camera parameters to the screen
        print ("set_res value: " + setres)
        print ("set_rotate value: " + setrotate)
        print ("set_flip value: " + setflip)

        return render_template('stream_video_mode.html', **template_data)   # run the 'stream_video_mode.html' template

    elif choice_mode == 'camsetup':   # run this section of code if 'camsetup' is selected at the template

        # update time now
        timenow = time.strftime('%H:%M %Z')

        # template data: individual parameters that are passed for use in the template to render the browser display
        template_data = {
            'title' : "camera set up",          # this sets the browser title template parameter
            'time_now' : timenow,               # this sets the current time template parameter
            'set_res' : setres,                 # this sets the camera resolution template parameter
            'set_resW' : setresW,               # this sets the camera resolution width parameter
            'set_resH' : setresH,               # this sets the camera resolution height parameter
            'set_rotate' : setrotate,           # this sets the display rotation template parameter
            'set_flip' : setflip,               # this sets the display flipping template parameter
            'set_res1' : setres1,               # 160x120 - all the following set the available camera resolutions
            'set_res2' : setres2,               # 176x144
            'set_res3' : setres3,               # 320x240
            'set_res4' : setres4,               # 352x288
            'set_res5' : setres5,               # 640x480
            'set_res6' : setres6,               # 800x600
            'set_res7' : setres7,               # 1280x720
            'set_res8' : setres8,               # 1920x1080
            'set_bright' : setbright,  # this and the rest of these parameters are a bit exotic and may have unpredictable effects
            'set_contrast' : setcontrast,
            'set_sat' : setsat,
            'set_hue' : sethue,
            'set_gain' : setgain,
            'set_exp' : setexp,
            'set_wbal' : setwbal,
            'set_focus' : setfocus,

        }

        # echo the values of the key camera parameters to the screen
        print ("set_res value: " + setres)
        print ("set_rotate value: " + setrotate)
        print ("set_flip value: " + setflip)

        return render_template('cam_setup_mode.html', **template_data)    # run the 'cam_setup_mode.html' template

    elif choice_mode == 'camoptions':   # run this section of code if 'camoptions' is selected at the template

        # update time now
        timenow = time.strftime('%H:%M %Z')

        # template data: individual parameters that are passed for use in the template to render the browser display
        template_data = {
            'title' : "camera options",         # this sets the browser title template parameter
            'time_now' : timenow,               # this sets the current time template parameter
            'set_res' : setres,                 # this sets the camera resolution template parameter
            'set_res1' : setres1,               # 160x120 - all the following set the available camera resolutions
            'set_res2' : setres2,               # 176x144
            'set_res3' : setres3,               # 320x240
            'set_res4' : setres4,               # 352x288
            'set_res5' : setres5,               # 640x480
            'set_res6' : setres6,               # 800x600
            'set_res7' : setres7,               # 1280x720
            'set_res8' : setres8,               # 1920x1080
            'set_resW' : setresW,               # this sets the camera resolution width parameter
            'set_resH' : setresH,               # this sets the camera resolution height parameter
            'set_rotate' : setrotate,           # this sets the display rotation template parameter
            'set_flip' : setflip,               # this sets the display flipping template parameter
            'set_bright' : setbright,  # this and the rest of these parameters are a bit exotic and may have unpredictable effects
            'set_contrast' : setcontrast,
            'set_sat' : setsat,
            'set_hue' : sethue,
            'set_gain' : setgain,
            'set_exp' : setexp,
            'set_wbal' : setwbal,
            'set_focus' : setfocus,

        }

        # echo the values of the key camera parameters to the screen
        print ("set_res value: " + setres)
        print ("set_rotate value: " + setrotate)
        print ("set_flip value: " + setflip)

        return render_template('cam_options_setup.html', **template_data)    # run the 'cam_options_setup.html' template

    else:         # shouldn't ever arrive here but run this section of code if  'streamvid', nor 'camsetup', nor camoptions are selected at the template
        template_data = {
            'title' : "mode selection",
        }
        return render_template('select_mode.html', **template_data)


##################################################################################################################
# this route defines the actions selected when the USB camera is in set up mode
##################################################################################################################
@make_image_app01.route("/camsetup/<setup_command>")  # run the code below this function when URL /camsetup/<setup_command> is accessed where <setup_command> is a variable
def update_camsettings(setup_command=None):
    global setres
    global setresW
    global setresH
    global setrotate
    global setflip

    global setres1
    global setres2
    global setres3 
    global setres4
    global setres5
    global setres6
    global setres7
    global setres8 
 
    global setbright
    global setcontrast
    global setsat
    global sethue
    global setgain
    global setexp
    global setwbal
    global setfocus

    none_selected = "no mode selected"

    # update time now
    timenow = time.strftime('%H:%M %Z')

    if setup_command == 'update_settings':
        # execute this set of code to update the camera resolution setting

        print ("request method: " + str(request.method))
        print ("new resolution value: " + str(request.args.get('resolution')))
        setres = str(request.args.get('resolution'))
        xfind = setres.find('x')
        setresW = setres[:xfind]
        setresH = setres[xfind+1:]
        print ("parsed W and H: " + str(setresW) + " - " + str(setresH))
        print ("new rotation value: " + str(request.args.get('rotation')))
        setrotate = str(request.args.get('rotation'))
        print ("new flipping value: " + str(request.args.get('flipping')))
        setflip = str(request.args.get('flipping'))

        # template data: individual parameters that are passed for use in the template to render the browser display
        template_data = {
            'title' : "streaming video",        # this sets the browser title template parameter
            'time_now' : timenow,               # this sets the current time template parameter
            'set_res' : setres,                 # this sets the camera resolution template parameter
            'set_resW' : setresW,               # this sets the camera resolution width parameter
            'set_resH' : setresH,               # this sets the camera resolution height parameter
            'set_rotate' : setrotate,           # this sets the display rotation template parameter
            'set_flip' : setflip,               # this sets the display flipping template parameter
            'set_bright' : setbright,  # this and the rest of these parameters are a bit exotic and may have unpredictable effects
            'set_contrast' : setcontrast,
            'set_sat' : setsat,
            'set_hue' : sethue,
            'set_gain' : setgain,
            'set_exp' : setexp,
            'set_wbal' : setwbal,
            'set_focus' : setfocus,

        }

        # echo the values of the key camera parameters to the screen
        print ("set_res value: " + setres)
        print ("set_rotate value: " + setrotate)
        print ("set_flip value: " + setflip)

        return render_template('stream_video_mode.html', **template_data)    # run the 'stream_video_mode.html' template


    elif setup_command == 'select':
        template_data = {
            'title' : "mode selection",
        }
        print (" going back to select .....")

        return render_template('select_mode.html', **template_data)


##################################################################################################################
# this route defines the actions selected when the USB camera is in set up mode
##################################################################################################################
@make_image_app01.route("/camoptions/<setup_command>")  # run the code below this function when URL /camoptions/<setup_command> is accessed where <setup_command> is a variable
def update_camoptions(setup_command=None):
    global setres
    global setresW
    global setresH
    global setrotate
    global setflip

    global setres1
    global setres2
    global setres3 
    global setres4
    global setres5
    global setres6
    global setres7
    global setres8 
 
    global setbright
    global setcontrast
    global setsat
    global sethue
    global setgain
    global setexp
    global setwbal
    global setfocus

    none_selected = "no mode selected"

    # update time now
    timenow = time.strftime('%H:%M %Z')

    if setup_command == 'update_resolutions':
        # execute this set of code to update the camera resolution options that are available

        print ("request method: " + str(request.method))

        setres1 = str(request.args.get('res1'))
        setres2 = str(request.args.get('res2'))
        setres3 = str(request.args.get('res3'))
        setres4 = str(request.args.get('res4'))
        setres5 = str(request.args.get('res5'))
        setres6 = str(request.args.get('res6'))
        setres7 = str(request.args.get('res7'))
        setres8 = str(request.args.get('res8'))

        print ("new available res1 value: " + str(request.args.get('res1')))
        print ("new available res2 value: " + str(request.args.get('res2')))
        print ("new available res3 value: " + str(request.args.get('res3')))
        print ("new available res4 value: " + str(request.args.get('res4')))
        print ("new available res5 value: " + str(request.args.get('res5')))
        print ("new available res6 value: " + str(request.args.get('res6')))
        print ("new available res7 value: " + str(request.args.get('res7')))
        print ("new available res8 value: " + str(request.args.get('res8')))

        setres = str(request.args.get('resolution'))
        xfind = setres.find('x')
        setresW = setres[:xfind]
        setresH = setres[xfind+1:]
        print ("parsed W and H: " + str(setresW) + " - " + str(setresH))
        print ("new rotation value: " + str(request.args.get('rotation')))
        setrotate = str(request.args.get('rotation'))
        print ("new flipping value: " + str(request.args.get('flipping')))
        setflip = str(request.args.get('flipping'))

        # template data: individual parameters that are passed for use in the template to render the browser display
        template_data = {
            'title' : "camera options",        # this sets the browser title template parameter
            'time_now' : timenow,               # this sets the current time template parameter
            'set_res' : setres,                 # this sets the camera resolution template parameter
            'set_res1' : setres1,               # 160x120 - all the following set the available camera resolutions
            'set_res2' : setres2,               # 176x144
            'set_res3' : setres3,               # 320x240
            'set_res4' : setres4,               # 352x288
            'set_res5' : setres5,               # 640x480
            'set_res6' : setres6,               # 800x600
            'set_res7' : setres7,               # 1280x720
            'set_res8' : setres8,               # 1920x1080
            'set_resW' : setresW,               # this sets the camera resolution width parameter
            'set_resH' : setresH,               # this sets the camera resolution height parameter
            'set_rotate' : setrotate,           # this sets the display rotation template parameter
            'set_flip' : setflip,               # this sets the display flipping template parameter
            'set_bright' : setbright,  # this and the rest of these parameters are a bit exotic and may have unpredictable effects
            'set_contrast' : setcontrast,
            'set_sat' : setsat,
            'set_hue' : sethue,
            'set_gain' : setgain,
            'set_exp' : setexp,
            'set_wbal' : setwbal,
            'set_focus' : setfocus,

        }

        # echo the values of the key camera parameters to the screen
        print ("set_res value: " + setres)
        print ("set_rotate value: " + setrotate)
        print ("set_flip value: " + setflip)

        return render_template('cam_options_setup.html', **template_data)    # re-run the 'cam_options_setup.html' template

    elif setup_command == 'update_settings':
        # execute this set of code to update the camera 'exotic' settings that may be available

        print ("request method: " + str(request.method))

        setbright = str(request.args.get('br_set'))
        setcontrast = str(request.args.get('con_set'))
        setsat = str(request.args.get('sat_set'))
        sethue = str(request.args.get('hue_set'))
        setgain = str(request.args.get('gain_set'))
        setexp = str(request.args.get('exp_set'))
        setwbal = str(request.args.get('wbal_set'))
        setfocus = str(request.args.get('focus_set'))

        print ("new setbright value: " + str(request.args.get('br_set')))
        print ("new setcontrast value: " + str(request.args.get('con_set')))
        print ("new setsat value: " + str(request.args.get('sat_set')))
        print ("new sethue value: " + str(request.args.get('hue_set')))
        print ("new setgain value: " + str(request.args.get('gain_set')))
        print ("new setexp value: " + str(request.args.get('exp_set')))
        print ("new setwbal value: " + str(request.args.get('wbal_set')))
        print ("new setfocus value: " + str(request.args.get('focus_set')))

        # template data: individual parameters that are passed for use in the template to render the browser display
        template_data = {
            'title' : "camera options",        # this sets the browser title template parameter
            'time_now' : timenow,               # this sets the current time template parameter
            'set_res' : setres,                 # this sets the camera resolution template parameter
            'set_res1' : setres1,               # 160x120 - all the following set the available camera resolutions
            'set_res2' : setres2,               # 176x144
            'set_res3' : setres3,               # 320x240
            'set_res4' : setres4,               # 352x288
            'set_res5' : setres5,               # 640x480
            'set_res6' : setres6,               # 800x600
            'set_res7' : setres7,               # 1280x720
            'set_res8' : setres8,               # 1920x1080
            'set_resW' : setresW,               # this sets the camera resolution width parameter
            'set_resH' : setresH,               # this sets the camera resolution height parameter
            'set_rotate' : setrotate,           # this sets the display rotation template parameter
            'set_flip' : setflip,               # this sets the display flipping template parameter
            'set_bright' : setbright,   # this and the rest of these parameters are a bit exotic and may have unpredictable effects
            'set_contrast' : setcontrast,
            'set_sat' : setsat,
            'set_hue' : sethue,
            'set_gain' : setgain,
            'set_exp' : setexp,
            'set_wbal' : setwbal,
            'set_focus' : setfocus,

        }

        # echo the values of the key camera parameters to the screen
        print ("set_res value: " + setres)
        print ("set_rotate value: " + setrotate)
        print ("set_flip value: " + setflip)

        return render_template('cam_options_setup.html', **template_data)    # re-run the 'cam_options_setup.html' template

    elif setup_command == 'select':
        template_data = {
            'title' : "mode selection",
        }
        print (" going back to select .....")

        return render_template('select_mode.html', **template_data)



##################################################################################################################
# this route defines the actions selected when the USB camera is in video streaming mode
##################################################################################################################
@make_image_app01.route("/streamvid/<streamvid_command>")  # run the code below this function when URL /streamvid/<streamvid_command> is accessed where <streamvid_command> is a variable
def update_streamvid(streamvid_command=None):
    none_selected = "no mode selected"

    # update time now
    timenow = time.strftime('%H:%M %Z')

    # this should be the only option - i.e. to interrupt the streaming and return to select mode
    #   but it should be noted that this will produce an Exception notice and traceback echo to the 
    #   screen with a message about a 'Broken pipe' - this just means that the browser stream has 
    #   been unexpectedly interrupted and is to be expected
    #   - not found a way so far to suppress this message
    if streamvid_command == 'select':
        template_data = {
            'title' : "mode selection",
        }

        return render_template('select_mode.html', **template_data)


#####################################################
# the code below is the last code in the system
#####################################################

if __name__ == "__main__":
    make_image_app01.run(host='0.0.0.0', port=8000, debug=False, threaded=True) # 0.0.0.0 means any device on the network can access the web app
    # use port 8000 so that you do not have to run the app as root (ie use sudo) which is necessary if the 'production' port 80 is used

    # debug version
    #make_image_app01.run(host='0.0.0.0', port=8000, debug=True)   # 0.0.0.0 means any device on the network can access the web app

