#!/bin/bash

echo "Say a few words. Press Ctrl+C to finish."
arecord -q -t wav -d 5 -f S16_LE -r 16000 | flac - --force --best -s -o out.flac > /dev/null 2>&1
