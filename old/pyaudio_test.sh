#!/bin/bash

python -c "import pyaudio;audio=pyaudio.PyAudio();print([audio.get_device_info_by_index(i) for i in range(audio.get_device_count())])"
