#!/bin/bash

LANGUAGE=en-us
KEY=AIzaSyAf35kTcgYzh1OVSQzSP2Di_EzQ2c0LtmI         
OUTPUT=json

echo "Hitting the Google API..."
wget -q -U "Mozilla/5.0" --post-file out.flac --header "Content-Type: audio/x-flac; rate=16000" -O - "http://www.google.com/speech-api/v2/recognize?lang=${LANGUAGE}&key=${KEY}" > out.json

echo -n "You Said: "
cat out.json
