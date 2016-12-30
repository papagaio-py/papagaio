#!/bin/bash

#################   Requires   ####################
#	Jq - to parse JSON file received          #
#	     https://stedolan.github.io/jq/       #
#						  #
###################################################

################# DEFINITIONS  ####################
LANGUAGE=en-us
KEY=AIzaSyAf35kTcgYzh1OVSQzSP2Di_EzQ2c0LtmI         
TEXT_OUTPUT=out.json
AUDIO_FILE=out.flac
FILE_WORK_DIR=/home/pi/Projects/Papagaio/Test_Files

################ /DEFINITION  ######################

echo "Hitting the Google API..."
wget -q -U "Mozilla/5.0" --post-file $FILE_WORK_DIR/$AUDIO_FILE \
--header "Content-Type: audio/x-flac; rate=44100" -O - \
"http://www.google.com/speech-api/v2/recognize?lang=${LANGUAGE}&key=${KEY}" \
> $FILE_WORK_DIR/$TEXT_OUTPUT

echo -n "You Said: "
#cat $FILE_WORK_DIR/$TEXT_OUTPUT
jq '.result[0] .alternative[0]' $FILE_WORK_DIR/$TEXT_OUTPUT
