import thread
import time

import pyaudio

import apiai

#CHUNK = 512
CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5

CLIENT_ACCESS_TOKEN = '8e639324ac2b431fbfdc2b05339d5ee3'


def input_thread(L):
    raw_input()
    L.append(None)


def main():
    resampler = apiai.Resampler(source_samplerate=RATE)

    vad = apiai.VAD()

    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    request = ai.voice_request()

    request.lang = 'en'  # optional, default value equal 'en'

    def callback(in_data, frame_count, time_info, status):
        frames, data = resampler.resample(in_data, frame_count)
        state = vad.processFrame(frames)
        request.send(data)

        if state == 1:
            return in_data, pyaudio.paContinue
        else:
            return in_data, pyaudio.paComplete

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=False,
                    frames_per_buffer=CHUNK,
                    stream_callback=callback)

    stream.start_stream()

    print ("Say! Press enter for stop audio recording.")

    try:
        L = []
        thread.start_new_thread(input_thread, (L,))

        while stream.is_active() and len(L) == 0:
            time.sleep(0.1)

    except Exception:
        raise
    except KeyboardInterrupt:
        pass

    stream.stop_stream()
    stream.close()
    p.terminate()

    print ("Wait for response...")
    response = request.getresponse()

    print (response.read())

if __name__ == '__main__':
    main()
