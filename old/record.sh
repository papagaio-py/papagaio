#!/bin/bash


########################################################
#    Requires  SoX − Sound eXchange                    #
#                                                      #
#                                                      #
########################################################

###################  Definitions  #####################
AUDIO_FILE=out.flac
FILE_WORK_DIR=/home/pi/Projects/Papagaio/Test_Files
#						      #
#######################################################

#Little housekeeping
	if [ -f $AUDIO_FILE ] ; then
 		rm $AUDIO_FILE
	fi

#Now let's  capture the file
echo "Say a few words in 5s or press Ctrl+C to finish."
rec -q -t flac -r 44100 $FILE_WORK_DIR/$AUDIO_FILE trim 0 5
############## FILE FORMAT  #############################
#   -t <type> - flac                                    #
#   -r <int>  - 44100 - Sample Frequency                #
#   current card doesn't support <44100 Hz              #
#   trim 0 5 - Defines maximum time, can be improved    #
#              using - silence 1 0.50 0.1% 1 10:00 0.1% #
#   -q Quiet                                            #
#########################################################
