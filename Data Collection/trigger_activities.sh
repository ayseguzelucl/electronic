#!/bin/bash


# Get date
DATE=`date "+%Y%m%d_%H%M%S"`

# Error function
function error() {
	echo "ERROR! -" $1 && exit 1
}

# Usage function
function usage() {
	echo "Script to run measurements"
}

# Directories
SOURCE=${BASH_SOURCE[0]}
CODEDIR=$(dirname $(realpath $SOURCE))
BASEDIR=$(dirname $CODEDIR)

# Load inputs
net_switch="false"
while [ "$#" -gt 0 ] ; do
  case "${1}" in
    (-c|--config_fpath)  CONFIG=$BASEDIR/code/logs/log_instructions/"${2}" ;;
	(-n|--net_switch) net_switch="true" ;;
	(-h|--help) usage && exit 0 ;;
  esac
  shift
done

# Check inputs
[ -z "$CONFIG" ]   && error "You must state the device using --config_fpath "
# Function to make phone wait for 5 seconds
function waitphone {
	while [ -z "$PHONE_FOUND" ]; do
		echo "Phone not found, waiting for $PHONE/$ANDROID_SERIAL"
		sleep 5
		PHONE_FOUND=`adb devices | grep $ANDROID_SERIAL | grep device`
	done
}

# Read config from file and assign variables
while IFS=";" read device plug interface exp_tag phone package sleep1 start_actions duration end_actions
do  
    # Ignore commented lines starting with # (spaces before # are allowed)
    [[ $device  =~ ^[[:space:]]*# ]] && continue
    # Ignore empty lines and lines with only spaces
    [[ $device  =~ ^[[:space:]]*$ ]] && continue

	# Check that phone ID is present in ID file
	if [ ! -f "$BASEDIR/code/phone_ids/$phone" ]; then
	    error "$phone does not exist at $BASEDIR/code/phone_ids!"
	else
	    export ANDROID_SERIAL=`cat "$BASEDIR/code/phone_ids/$phone"`
	    echo "Phone is: $phone/$ANDROID_SERIAL"
	    PHONE_FOUND=`adb devices | grep $ANDROID_SERIAL | grep device`
	    waitphone
	    echo "Phone ready, proceeding"
	fi


	# Write info to config file
	echo "Writing basic info to config file"
	echo "Device:" "$device" 
	echo "Phone:" "$phone" 
	echo "Interface:" "$interface"
	echo "Plug:" "$plug" 
	echo "Package:" "$package" 
	# Start controlling phone
	echo "Starting app for device" $name_dev
    waitphone
    adb shell -n monkey -p $package -c android.intent.category.LAUNCHER 1
    DATE=`date "+%Y%m%d_%H%M%S"`
    echo "Starting app time:" "$DATE" 
    sleep $sleep1

	# Perform device functionalities
    echo "Starting functionalities for device $name"
    DATE=`date "+%Y%m%d_%H%M%S"`
    echo "Starting functionalities time:" "$DATE" >> $EXPDIR/config
    [ -n "$start_actions" ] && ( waitphone; adb shell -n input $start_actions )
	echo "Waiting for duration $duration"
        #sudo adb shell screencap -p | sudo sed "s|\r$||" > "/log_screenshots/beginning_$DATE.png"
	sleep $duration
        #sudo adb shell screencap -p | sudo sed "s|\r$||" > "/log_screenshots/during_$DATE.png"
        #adb shell screencap test_screen.png
    [ -n "$end_actions" ] && ( waitphone; adb shell -n input $end_actions )
        #sudo adb shell screencap -p | sudo sed "s|\r$||" > "/log_screenshots/ending_$DATE.png"   
	sleep $sleep1

    waitphone
    adb shell -n am force-stop $package

done < $CONFIG
